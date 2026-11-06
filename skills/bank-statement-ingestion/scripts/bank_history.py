# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Create a history with create_history(path), then save accounts and statements.

Pass raw dates/formats, amount separators and debit/credit evidence. Supply
opening/closing balance records to reconcile; absent balances are reported as
reconciled=False. Printed totals can be passed as expected_debits/credits.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal, Mapping, Sequence
from uuid import uuid4


class HistoryError(ValueError):
    """The supplied date or amount cannot be saved."""


@dataclass(frozen=True)
class Evidence:
    quote: str
    location: str
    kind: Literal["header", "record", "user"]


@dataclass(frozen=True)
class Record:
    evidence: Evidence
    kind: Literal["transaction", "balance"] = "transaction"
    transaction_date: str | None = None
    posting_date: str | None = None
    amount: str | None = None
    currency: str | None = None
    description: str | None = None
    bank_reference: str | None = None
    reliable_reference: bool = False
    card_id: str | None = None
    status: Literal["pending", "posted"] | None = None
    balance_date: str | None = None
    balance_type: Literal["opening", "closing", "current", "ledger", "available"] | None = None
    raw_amount: str | None = None
    amount_location: str | None = None
    sign_evidence: Evidence | None = None
    date_locations: tuple[tuple[str, str], ...] = ()
    raw_dates: tuple[tuple[str, str], ...] = ()
    date_formats: tuple[tuple[str, str], ...] = ()
    amount_decimal_separator: str | None = None
    amount_group_separator: str | None = None


@dataclass(frozen=True)
class Statement:
    account_id: str
    records: tuple[Record, ...]
    scope: Literal["account", "card"] = "account"
    card_id: str | None = None
    start: str | None = None
    end: str | None = None
    start_evidence: Evidence | None = None
    end_evidence: Evidence | None = None
    date_basis: Literal["transaction", "posting"] | None = None
    expected_debits: str | None = None
    expected_credits: str | None = None


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _id() -> str:
    return uuid4().hex


def minor_units(value: str, precision: int) -> int:
    try:
        amount = Decimal(value) * (10 ** precision)
        if not amount.is_finite() or amount != amount.to_integral_value():
            raise HistoryError("The amount has more decimal places than the currency allows.")
        result = int(amount)
        if not -(2**63) <= result < 2**63:
            raise HistoryError("The amount exceeds the database integer range.")
        return result
    except HistoryError:
        raise
    except (InvalidOperation, TypeError, ValueError) as error:
        raise HistoryError("The amount does not convert with the supplied format.") from error


def _convert_date(value: str, date_format: str) -> str:
    try:
        return datetime.strptime(value, date_format).strftime("%Y-%m-%d")
    except (TypeError, ValueError) as error:
        raise HistoryError("The date does not convert with the supplied format.") from error


def _convert_amount(value: str, decimal_separator: str, group_separator: str, *,
                    account_type: str = "transaction", sign_evidence: Evidence | None = None) -> str:
    try:
        value = value.strip()
        suffix = re.search(r"\s*(CR|DR)$", value, re.IGNORECASE)
        direction = suffix[1].upper() if suffix else None
        if suffix:
            value = value[:suffix.start()].strip()
        if sign_evidence:
            directions = {"DR" if word.lower() in {"debit", "debits", "dr"} else "CR"
                          for word in re.findall(r"\b(debits?|credits?|DR|CR)\b", sign_evidence.quote, re.I)}
            if len(directions) != 1 or direction and direction not in directions:
                raise HistoryError("Supply one clear debit or credit direction.")
            direction = directions.pop()
        explicit = value.startswith(("+", "-", "−", "("))
        negative = value.startswith(("-", "−", "("))
        if value.startswith("(") and value.endswith(")"):
            value = "-" + value[1:-1]
        value = value.replace("−", "-").lstrip("$")
        if decimal_separator is None or group_separator is None or (
            decimal_separator and decimal_separator == group_separator
        ):
            raise HistoryError("Supply distinct decimal and group separators.")
        amount = value.replace(group_separator, "") if group_separator else value
        amount = amount.replace(decimal_separator, ".") if decimal_separator else amount
        number = Decimal(amount)
        if not number.is_finite():
            raise HistoryError("The amount must be finite.")
        if direction:
            positive = (direction == "DR") == (account_type in {"credit", "loan"})
            if explicit and number and negative == positive:
                raise HistoryError("The explicit sign conflicts with debit/credit evidence.")
            number = abs(number) if positive else -abs(number)
        elif number and not explicit:
            raise HistoryError("Unsigned amounts need debit/credit evidence.")
        return str(number)
    except HistoryError:
        raise
    except (InvalidOperation, AttributeError, TypeError, ValueError) as error:
        raise HistoryError("The amount does not convert with the supplied format.") from error


def create_history(history: Path) -> None:
    """Create the tables used by statement import."""
    history = Path(history)
    history.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(history / "history.sqlite3")) as connection, connection:
        connection.executescript("""
        PRAGMA foreign_keys=ON;
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY, alias TEXT NOT NULL, bank TEXT, type TEXT,
            identity_evidence TEXT NOT NULL, currency TEXT NOT NULL, precision INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY, content_hash TEXT UNIQUE NOT NULL, size INTEGER NOT NULL,
            format TEXT NOT NULL, original_name TEXT NOT NULL, managed_path TEXT NOT NULL,
            copy_state TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS statements (
            id TEXT PRIMARY KEY, file_id TEXT NOT NULL REFERENCES files(id), section TEXT NOT NULL,
            account_id TEXT NOT NULL REFERENCES accounts(id), scope TEXT NOT NULL, card_id TEXT,
            start TEXT, end TEXT, start_evidence TEXT, end_evidence TEXT,
            date_basis TEXT, reader TEXT NOT NULL, outcome TEXT NOT NULL, questions TEXT NOT NULL,
            UNIQUE(file_id, section));
        CREATE TABLE IF NOT EXISTS statement_records (
            id TEXT PRIMARY KEY, statement_id TEXT NOT NULL REFERENCES statements(id),
            fingerprint TEXT NOT NULL, occurrence INTEGER NOT NULL, kind TEXT NOT NULL,
            source_location TEXT NOT NULL, source_quote TEXT NOT NULL, transaction_date TEXT,
            posting_date TEXT, amount_text TEXT, amount_minor INTEGER, currency TEXT,
            description TEXT, bank_reference TEXT, reliable_reference INTEGER NOT NULL,
            card_id TEXT, status TEXT, balance_date TEXT, balance_type TEXT,
            transaction_id TEXT, accepted INTEGER NOT NULL DEFAULT 1, superseded INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id), card_id TEXT,
            transaction_date TEXT, posting_date TEXT, amount INTEGER NOT NULL, currency TEXT NOT NULL,
            description TEXT, bank_reference TEXT, reliable_reference INTEGER NOT NULL,
            status TEXT NOT NULL, supporting_record TEXT NOT NULL REFERENCES statement_records(id),
            active INTEGER NOT NULL DEFAULT 1);
        """)


def save_account(
    history: Path,
    fields: Mapping[str, str | int | None],
    evidence: Evidence,
    *,
    account_id: str | None = None,
) -> str:
    """Save the account fields needed for statement import."""
    account_id = account_id or _id()
    database = (Path(history) / "history.sqlite3").resolve()
    with closing(sqlite3.connect(database.as_uri() + "?mode=rw", uri=True)) as connection, connection:
        connection.execute(
            "INSERT INTO accounts (id,alias,bank,type,identity_evidence,currency,precision) VALUES (?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
            "alias=excluded.alias, bank=excluded.bank, type=excluded.type, "
            "identity_evidence=excluded.identity_evidence, currency=excluded.currency, precision=excluded.precision",
            (account_id, fields["alias"], fields.get("bank"), fields.get("type"),
             evidence.quote, fields["currency"], fields["precision"]),
        )
    return account_id


def _prepare_statement(statement: Statement, account: sqlite3.Row) -> tuple[list, bool]:
    """Convert all supplied rows and reconcile before writing any of them."""
    if not statement.start or not statement.end or statement.start > statement.end:
        raise HistoryError("Supply ordered statement start and end dates.")
    for value in (statement.start, statement.end):
        datetime.strptime(value, "%Y-%m-%d")
    if statement.date_basis not in {None, "transaction", "posting"}:
        raise HistoryError("Unknown statement date basis.")
    rows, balances, movement, debit, credit = [], {}, 0, 0, 0
    liability = account["type"] in {"credit", "loan"}
    for record in statement.records:
        raw_dates, formats = dict(record.raw_dates), dict(record.date_formats)
        if raw_dates.keys() - formats.keys():
            raise HistoryError("Supply a format for each original date field.")
        dates = {field: _convert_date(raw_dates[field], formats[field]) if field in raw_dates else getattr(record, field)
                 for field in ("transaction_date", "posting_date", "balance_date")}
        raw = record.raw_amount if record.raw_amount is not None else record.amount
        amount = minor_units(_convert_amount(raw, record.amount_decimal_separator, record.amount_group_separator,
            account_type=account["type"], sign_evidence=record.sign_evidence), account["precision"])
        if record.currency != account["currency"]:
            raise HistoryError("Record currency differs from the account currency.")
        if record.kind == "transaction":
            basis = dates["posting_date"] if statement.date_basis == "posting" else dates["transaction_date"]
            if not basis or not statement.start <= basis <= statement.end or record.status != "posted":
                raise HistoryError("Supply a posted transaction within the statement period.")
            movement += amount
            if amount and (amount > 0) == liability:
                debit += abs(amount)
            else:
                credit += abs(amount)
        elif record.kind == "balance":
            if not dates["balance_date"] or not record.balance_type:
                raise HistoryError("Supply balance date and type.")
            if record.balance_type in {"opening", "closing"}:
                expected_date = statement.start if record.balance_type == "opening" else statement.end
                if dates["balance_date"] != expected_date or record.balance_type in balances:
                    raise HistoryError("Supply one balance of each type at the statement boundaries.")
                balances[record.balance_type] = amount
        else:
            raise HistoryError("Unknown record kind.")
        rows.append((record, dates, raw, amount))
    if balances and (set(balances) != {"opening", "closing"} or
                     balances["opening"] + movement != balances["closing"]):
        raise HistoryError("Opening balance plus movements does not match closing balance.")
    for label, actual, expected in (("debits", debit, statement.expected_debits),
                                    ("credits", credit, statement.expected_credits)):
        if expected is not None and (minor_units(expected, account["precision"]) != actual):
            raise HistoryError(f"Statement {label} do not match the supplied total.")
    return rows, bool(balances)


def save_statement(history: Path, source: Path, sections: Sequence[Statement]) -> list[dict[str, object]]:
    """Convert supplied fields and save their rows in one database transaction."""
    source = Path(source)
    file_hash = hashlib.sha256()
    file_size = 0
    with source.open("rb") as file_data:
        while block := file_data.read(1024 * 1024):
            file_hash.update(block)
            file_size += len(block)
    digest = file_hash.hexdigest()
    results = []
    database = (Path(history) / "history.sqlite3").resolve()
    with closing(sqlite3.connect(database.as_uri() + "?mode=rw", uri=True)) as connection, connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT OR IGNORE INTO files VALUES (?,?,?,?,?,?,?)",
            (_id(), digest, file_size, source.suffix.lower().lstrip("."), source.name, digest, "not_retained"),
        )
        file_id = connection.execute("SELECT id FROM files WHERE content_hash=?", (digest,)).fetchone()["id"]
        for section in sections:
            prior_ranges = connection.execute(
                "SELECT id, section, start, end, file_id, outcome, date_basis FROM statements "
                "WHERE account_id=? AND scope=? AND card_id IS ?",
                (section.account_id, section.scope, section.card_id),
            ).fetchall()
            duplicate = next((row for row in prior_ranges
                              if section.start and section.end
                              and row["start"] == section.start and row["end"] == section.end), None)
            if duplicate is None and not (section.start and section.end):
                duplicate = connection.execute(
                    "SELECT id, section FROM statements WHERE file_id=? AND account_id=? AND scope=? AND card_id IS ?",
                    (file_id, section.account_id, section.scope, section.card_id),
                ).fetchone()
            if duplicate:
                if duplicate["file_id"] != file_id or duplicate["date_basis"] != section.date_basis:
                    raise HistoryError("Saved period has different source or date basis; review a correction.")
                if duplicate["outcome"] == "imported":
                    results.append({"section": duplicate["section"], "statement_id": duplicate["id"],
                                    "outcome": "already_imported", "added": 0, "skipped": len(section.records)})
                    continue
                saved = connection.execute("SELECT accepted, transaction_id FROM statement_records WHERE statement_id=?",
                                           (duplicate["id"],)).fetchall()
                if duplicate["outcome"] not in {"partially_imported", "failed"} or any(
                    row["accepted"] or row["transaction_id"] for row in saved
                ):
                    raise HistoryError("Incomplete import contains accepted rows; review recovery before retrying.")
            account = connection.execute("SELECT * FROM accounts WHERE id=?", (section.account_id,)).fetchone()
            if account is None or account["type"] not in {"transaction", "savings", "credit", "loan"}:
                raise HistoryError("Select an existing account with a supported type.")
            prepared, reconciled = _prepare_statement(section, account)
            statement_id, section_id = (duplicate["id"], duplicate["section"]) if duplicate else (_id(), _id())
            if duplicate:
                connection.execute("DELETE FROM statement_records WHERE statement_id=?", (statement_id,))
                prior_ranges = [row for row in prior_ranges if row["id"] != statement_id]
            connection.execute(
                "INSERT INTO statements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
                "start_evidence=excluded.start_evidence,end_evidence=excluded.end_evidence,"
                "reader=excluded.reader,outcome=excluded.outcome,questions=excluded.questions",
                (statement_id, file_id, section_id, section.account_id, section.scope, section.card_id,
                 section.start, section.end, _json(asdict(section.start_evidence)) if section.start_evidence else None,
                 _json(asdict(section.end_evidence)) if section.end_evidence else None,
                 section.date_basis, "llm input", "imported", "[]"),
            )
            added = skipped = 0
            for index, (record, dates, raw_amount, amount) in enumerate(prepared):
                raw_dates, formats = dict(record.raw_dates), dict(record.date_formats)
                record_date = (dates["balance_date"] if record.kind == "balance" else
                               dates["posting_date"] if section.date_basis == "posting" else
                               dates["transaction_date"])
                if record_date and any(row["outcome"] == "imported" and row["start"] and row["end"]
                                       and row["start"] <= record_date <= row["end"] for row in prior_ranges):
                    skipped += 1
                    continue
                record_id = _id()
                transaction_id = _id() if record.kind == "transaction" else None
                source_location = {
                    "location": record.evidence.location,
                    "amount_location": record.amount_location,
                    "date_fields": {field: {"original_text": raw, "format": formats.get(field),
                     "location": dict(record.date_locations).get(field, record.evidence.location)} for field, raw in raw_dates.items()},
                    "amount_text": raw_amount,
                    "amount_format": {"decimal_separator": record.amount_decimal_separator,
                                      "group_separator": record.amount_group_separator},
                    "sign_evidence": asdict(record.sign_evidence) if record.sign_evidence else None,
                }
                connection.execute(
                    "INSERT INTO statement_records (id,statement_id,fingerprint,occurrence,kind,source_location,source_quote,transaction_date,posting_date,amount_text,amount_minor,currency,description,bank_reference,reliable_reference,card_id,status,balance_date,balance_type,transaction_id,accepted,superseded) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (record_id, statement_id, hashlib.sha256(f"{statement_id}:{index}".encode()).hexdigest(),
                     1, record.kind, _json(source_location), record.evidence.quote, dates["transaction_date"],
                     dates["posting_date"], raw_amount, amount, record.currency, record.description,
                     record.bank_reference, int(record.reliable_reference), record.card_id or section.card_id,
                     record.status or "posted", dates["balance_date"], record.balance_type,
                     transaction_id, 1, 0),
                )
                if transaction_id:
                    connection.execute(
                        "INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1)",
                        (transaction_id, section.account_id, record.card_id or section.card_id,
                         dates["transaction_date"], dates["posting_date"], amount, record.currency,
                         record.description, record.bank_reference, int(record.reliable_reference),
                         record.status or "posted", record_id),
                    )
                    added += 1
            outcome = "partially_imported" if skipped and added else "already_imported" if skipped else "imported"
            connection.execute("UPDATE statements SET outcome=? WHERE id=?", (outcome, statement_id))
            results.append({"section": section_id, "statement_id": statement_id,
                            "outcome": outcome, "added": added, "skipped": skipped,
                            "reconciled": reconciled})
    return results
