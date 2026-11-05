# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Save statement rows in a local SQLite history."""

from __future__ import annotations

import hashlib
import json
import sqlite3
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


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _id() -> str:
    return uuid4().hex


def minor_units(value: str, precision: int) -> int:
    try:
        amount = Decimal(value) * (10 ** precision)
        if amount != amount.to_integral_value():
            raise HistoryError("The amount has more decimal places than the currency allows.")
        return int(amount)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise HistoryError("The amount does not convert with the supplied format.") from error


def _convert_date(value: str, date_format: str) -> str:
    try:
        return datetime.strptime(value, date_format).strftime("%Y-%m-%d")
    except (TypeError, ValueError) as error:
        raise HistoryError("The date does not convert with the supplied format.") from error


def _convert_amount(value: str, decimal_separator: str, group_separator: str) -> str:
    try:
        amount = value.replace(group_separator, "") if group_separator else value
        amount = amount.replace(decimal_separator, ".") if decimal_separator else amount
        Decimal(amount)
        return amount
    except (InvalidOperation, TypeError, ValueError) as error:
        raise HistoryError("The amount does not convert with the supplied format.") from error


def create_history(history: Path) -> None:
    """Create the tables used by statement import."""
    history = Path(history)
    history.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(history / "history.sqlite3") as connection:
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
    with sqlite3.connect(Path(history) / "history.sqlite3") as connection:
        connection.execute(
            "INSERT INTO accounts VALUES (?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
            "alias=excluded.alias, bank=excluded.bank, type=excluded.type, "
            "identity_evidence=excluded.identity_evidence, currency=excluded.currency, precision=excluded.precision",
            (account_id, fields["alias"], fields.get("bank"), fields.get("type"),
             evidence.quote, fields["currency"], fields["precision"]),
        )
    return account_id


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
    with sqlite3.connect(Path(history) / "history.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute(
            "INSERT OR IGNORE INTO files VALUES (?,?,?,?,?,?,?)",
            (_id(), digest, file_size, source.suffix.lower().lstrip("."), source.name, digest, "not_retained"),
        )
        file_id = connection.execute("SELECT id FROM files WHERE content_hash=?", (digest,)).fetchone()["id"]
        for section in sections:
            prior_ranges = connection.execute(
                "SELECT id, section, start, end FROM statements "
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
                results.append({"section": duplicate["section"], "statement_id": duplicate["id"],
                                "outcome": "already_imported", "added": 0, "skipped": len(section.records)})
                continue
            precision = connection.execute("SELECT precision FROM accounts WHERE id=?", (section.account_id,)).fetchone()[0]
            statement_id, section_id = _id(), _id()
            connection.execute(
                "INSERT INTO statements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (statement_id, file_id, section_id, section.account_id, section.scope, section.card_id,
                 section.start, section.end, _json(asdict(section.start_evidence)) if section.start_evidence else None,
                 _json(asdict(section.end_evidence)) if section.end_evidence else None,
                 section.date_basis, "llm input", "imported", "[]"),
            )
            added = skipped = 0
            for index, record in enumerate(section.records):
                raw_dates, formats = dict(record.raw_dates), dict(record.date_formats)
                dates = {
                    field: _convert_date(raw_dates[field], formats[field]) if field in raw_dates else getattr(record, field)
                    for field in ("transaction_date", "posting_date", "balance_date")
                }
                raw_amount = record.raw_amount if record.raw_amount is not None else record.amount
                amount_text = _convert_amount(raw_amount, record.amount_decimal_separator, record.amount_group_separator)
                amount = minor_units(amount_text, precision)
                record_date = (dates["balance_date"] if record.kind == "balance" else
                               dates["posting_date"] if section.date_basis == "posting" else
                               dates["transaction_date"])
                if record_date and any(row["start"] and row["end"]
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
            results.append({"section": section_id, "statement_id": statement_id,
                            "outcome": outcome, "added": added, "skipped": skipped})
    return results
