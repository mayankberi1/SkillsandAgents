# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Local statement history. Document reading and maintenance are separate steps."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import sqlite3
from collections import Counter
from contextlib import closing, contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Iterator, Literal, Mapping, Sequence
from uuid import uuid4

HELPER_VERSION = 1
DATABASE_FORMAT = 1


class HistoryError(ValueError):
    """The requested operation cannot safely change this history."""


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
    uncertainty: str | None = None
    raw_amount: str | None = None
    amount_location: str | None = None
    sign_evidence: Evidence | None = None
    date_locations: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Statement:
    section: str
    text: str
    account_id: str | None
    identity_evidence: Evidence
    records: tuple[Record, ...] = ()
    scope: Literal["account", "card"] | None = "account"
    card_id: str | None = None
    start: str | None = None
    end: str | None = None
    start_evidence: Evidence | None = None
    end_evidence: Evidence | None = None
    date_basis: Literal["transaction", "posting"] | None = None
    complete: bool = False
    reader: str = "agent-supplied evidence"
    outcome: Literal["failed", "unsupported"] | None = None


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _id() -> str:
    return uuid4().hex


def _date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except (ValueError, TypeError) as error:
        raise HistoryError("Use YYYY-MM-DD dates.") from error
    if parsed.isoformat() != value:
        raise HistoryError("Use YYYY-MM-DD dates.")
    return parsed


def minor_units(value: str, precision: int) -> int:
    """Convert explicit decimal text without rounding or binary floats."""
    if type(precision) is not int or not 0 <= precision <= 9:
        raise HistoryError("Confirm currency precision between 0 and 9.")
    if not isinstance(value, str) or len(value) > 100 or not re.fullmatch(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d{1,3})?", value, flags=re.ASCII):
        raise HistoryError("Use signed decimal text for money.")
    sign, digits, exponent = Decimal(value).as_tuple()
    coefficient = int("".join(str(digit) for digit in digits))
    scale = exponent + precision
    if scale < 0 and coefficient % 10 ** -scale:
        raise HistoryError("Money has excess precision; no rounding was applied.")
    if coefficient and len(str(coefficient)) + scale > 19:
        raise HistoryError("Money exceeds the supported integer range.")
    result = coefficient * 10 ** scale if scale >= 0 else coefficient // 10 ** -scale
    if sign:
        result = -result
    if not -(2**63) <= result < 2**63:
        raise HistoryError("Money exceeds the supported integer range.")
    return result


def _evidence(evidence: Evidence, text: str | None = None) -> None:
    if evidence.kind not in {"header", "record", "user"} or not evidence.quote.strip() or not evidence.location.strip():
        raise HistoryError("Evidence needs its kind, quotation and location.")
    if text is not None and evidence.kind != "user" and evidence.quote not in text:
        raise HistoryError("The evidence quotation is absent from the supplied source text.")


def _boundary(value: str | None, evidence: Evidence | None, text: str, *, period: bool = True) -> None:
    if value is None:
        return
    parsed = _date(value)
    if evidence is None or (period and evidence.kind not in {"header", "user"}):
        raise HistoryError("Statement dates need header evidence or an explicit user answer.")
    _evidence(evidence, text)
    forms = (value, parsed.strftime("%d/%m/%Y"), parsed.strftime("%m/%d/%Y"), parsed.strftime("%d %B %Y"), parsed.strftime("%d %b %Y"))
    found = [
        form for form in forms
        if re.search(r"(?<![\w/+-])" + re.escape(form) + r"(?![\w/-]|\.\d)", evidence.quote, re.IGNORECASE)
    ]
    if not found:
        raise HistoryError("The statement date is absent from its evidence.")
    if evidence.kind != "user" and parsed.day <= 12 and parsed.month != parsed.day and all("/" in form for form in found):
        raise HistoryError("The numeric header date is ambiguous; ask the user.")


def _check_copies(connection: sqlite3.Connection, history: Path) -> None:
    _, directory = _history_paths(history)
    for row in connection.execute("SELECT * FROM files WHERE copy_state='ready'"):
        path = _managed_source(directory, row)
        if path.is_symlink() or not path.is_file() or _hash_copy(path) != (row["content_hash"], row["size"]):
            raise HistoryError("A retained source is missing or changed; recover it before importing.")


def _change(connection: sqlite3.Connection, kind: str, affected: str, evidence: object) -> None:
    connection.execute("INSERT INTO changes VALUES (?, ?, ?, ?, ?)", (_id(), kind, affected, _json(evidence), datetime.now(timezone.utc).isoformat()))


def _private_path(path: Path) -> None:
    if os.name != 'posix' or path.stat().st_mode & 0o077:
        raise HistoryError(f"History access requires private owner-only permissions: {path}")


def _managed_source(directory: Path, row: Mapping[str, object]) -> Path:
    digest = row['content_hash']
    if not isinstance(digest, str) or re.fullmatch(r'[0-9a-f]{64}', digest) is None or row['managed_path'] != digest:
        raise HistoryError("A stored source hash or path is invalid; no source was accessed or deleted.")
    path = directory / digest
    if path.is_symlink() or path.resolve().parent != directory.resolve():
        raise HistoryError("A stored source path leaves its managed folder; no source was accessed or deleted.")
    return path


def _history_paths(history: Path) -> tuple[Path, Path]:
    history = Path(history).absolute()
    if any(path.is_symlink() for path in (history, *history.parents)):
        raise HistoryError("History paths must not use symbolic links.")
    database, sources = history / "history.sqlite3", history / "sources"
    if not database.is_file() or database.is_symlink() or not sources.is_dir() or sources.is_symlink():
        raise HistoryError("The selected history is unavailable; it was not created or reset.")
    for path in (history, database, sources):
        _private_path(path)
    for path in sources.iterdir():
        if path.is_symlink() or not path.is_file():
            raise HistoryError("The source folder contains an unsupported entry; review it before use.")
        _private_path(path)
    return database, sources


@contextmanager
def _connect(history: Path, *, write: bool = False) -> Iterator[sqlite3.Connection]:
    database, _ = _history_paths(history)
    connection = sqlite3.connect(database.as_uri() + "?mode=rw", uri=True, timeout=1)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        if connection.execute("PRAGMA user_version").fetchone()[0] != DATABASE_FORMAT:
            raise HistoryError("This database format is not supported.")
        if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise HistoryError("The history is damaged; do not reset it.")
        if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise HistoryError("History record links are damaged; do not reset it.")
        connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        _, sources = _history_paths(history)
        for row in connection.execute('SELECT content_hash, managed_path FROM files'):
            _managed_source(sources, row)
        yield connection
        connection.commit()
    except sqlite3.Error as error:
        connection.rollback()
        raise HistoryError("History is busy, damaged or unavailable; no successful save is claimed.") from error
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()


def create_history(history: Path) -> None:
    """Create only an explicitly selected, new directory."""
    history = Path(history).absolute()
    if any(path.is_symlink() for path in history.parents):
        raise HistoryError("History paths must not use symbolic links.")
    history.mkdir(mode=0o700)
    (history / "sources").mkdir(mode=0o700)
    database = history / "history.sqlite3"
    descriptor = os.open(database, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    connection = sqlite3.connect(database)
    try:
        connection.executescript("""
        PRAGMA foreign_keys=ON;
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY, alias TEXT NOT NULL, bank TEXT, type TEXT,
            identity_evidence TEXT NOT NULL, currency TEXT, precision INTEGER,
            expected INTEGER NOT NULL DEFAULT 1, active_start TEXT, active_end TEXT,
            target INTEGER, safety_buffer INTEGER);
        CREATE TABLE cards (
            id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id),
            alias TEXT NOT NULL, masked_suffix TEXT, active_start TEXT, active_end TEXT,
            identity_evidence TEXT NOT NULL);
        CREATE TABLE files (
            id TEXT PRIMARY KEY, content_hash TEXT UNIQUE NOT NULL, size INTEGER NOT NULL,
            format TEXT NOT NULL, original_name TEXT NOT NULL, managed_path TEXT NOT NULL,
            copy_state TEXT NOT NULL);
        CREATE TABLE statements (
            id TEXT PRIMARY KEY, file_id TEXT NOT NULL REFERENCES files(id), section TEXT NOT NULL,
            account_id TEXT REFERENCES accounts(id), scope TEXT, card_id TEXT REFERENCES cards(id),
            start TEXT, end TEXT, start_evidence TEXT, end_evidence TEXT,
            date_basis TEXT, reader TEXT NOT NULL, outcome TEXT NOT NULL, questions TEXT NOT NULL,
            UNIQUE(file_id, section));
        CREATE TABLE statement_records (
            id TEXT PRIMARY KEY, statement_id TEXT NOT NULL REFERENCES statements(id),
            fingerprint TEXT NOT NULL, occurrence INTEGER NOT NULL, kind TEXT NOT NULL,
            source_location TEXT NOT NULL, source_quote TEXT NOT NULL, transaction_date TEXT,
            posting_date TEXT, amount_text TEXT, amount_minor INTEGER, currency TEXT,
            description TEXT, bank_reference TEXT, reliable_reference INTEGER NOT NULL,
            card_id TEXT REFERENCES cards(id), status TEXT, balance_date TEXT, balance_type TEXT,
            uncertainty TEXT, transaction_id TEXT REFERENCES transactions(id),
            accepted INTEGER NOT NULL DEFAULT 0, superseded INTEGER NOT NULL DEFAULT 0,
            UNIQUE(statement_id, fingerprint, occurrence));
        CREATE TABLE transactions (
            id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id),
            card_id TEXT REFERENCES cards(id), transaction_date TEXT, posting_date TEXT,
            amount INTEGER NOT NULL, currency TEXT NOT NULL, description TEXT,
            bank_reference TEXT, reliable_reference INTEGER NOT NULL, status TEXT NOT NULL,
            supporting_record TEXT NOT NULL REFERENCES statement_records(id), active INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE periods (
            id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id), scope TEXT NOT NULL,
            card_id TEXT REFERENCES cards(id), start TEXT NOT NULL, end TEXT NOT NULL,
            kind TEXT NOT NULL, statement_id TEXT REFERENCES statements(id), evidence TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE changes (id TEXT PRIMARY KEY, kind TEXT NOT NULL, affected_id TEXT NOT NULL,
            evidence TEXT NOT NULL, time TEXT NOT NULL);
        PRAGMA user_version=1;
        """)
    finally:
        connection.close()


def save_account(history: Path, fields: Mapping[str, str | int | bool | None], evidence: Evidence, *, account_id: str | None = None) -> str:
    """Save explicitly supplied fields; leave existing settings unchanged."""
    allowed = {"alias", "bank", "type", "currency", "precision", "expected", "active_start", "active_end", "target", "safety_buffer"}
    if not isinstance(fields, Mapping) or not fields or set(fields) - allowed:
        raise HistoryError("Unknown or missing account fields.")
    _evidence(evidence)
    with _connect(history, write=True) as connection:
        old = connection.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
        if account_id is not None and old is None:
            raise HistoryError("Select an existing account or explicitly create a new one.")
        values = dict(old) if old else {"expected": 1}
        values.update(fields)
        if not values.get("alias") or values.get("type") not in {None, "savings", "transaction", "credit"}:
            raise HistoryError("Supply an account alias and a supported account type.")
        for name in ("alias", "bank"):
            if values.get(name) is not None and (not isinstance(values[name], str) or not values[name].strip()):
                raise HistoryError("Account names must be nonempty text.")
        if "expected" in fields and type(fields["expected"]) is not bool:
            raise HistoryError("Expected-account membership must be true or false.")
        currency, precision = values.get("currency"), values.get("precision")
        if (currency is None) != (precision is None):
            raise HistoryError("Confirm currency and precision together.")
        if currency is not None:
            if not isinstance(currency, str) or not re.fullmatch("[A-Z]{3}", currency):
                raise HistoryError("Use a confirmed three-letter currency code.")
            minor_units("0", precision)
            other = connection.execute("SELECT precision FROM accounts WHERE currency=? AND id IS NOT ? LIMIT 1", (currency, account_id)).fetchone()
            if other and other[0] != precision:
                raise HistoryError("Use one confirmed precision for each currency.")
        for name in ("active_start", "active_end"):
            if values.get(name) is not None:
                _date(values[name])
        if values.get("active_start") and values.get("active_end") and values["active_start"] > values["active_end"]:
            raise HistoryError("Account active dates are reversed.")
        for name in ("target", "safety_buffer"):
            if name in fields and fields[name] is not None:
                values[name] = minor_units(fields[name], precision)
        if old and any(name in fields and values.get(name) != old[name] for name in ("currency", "precision")):
            if connection.execute("SELECT 1 FROM statements WHERE account_id=? LIMIT 1", (account_id,)).fetchone():
                raise HistoryError("Use the correction process to change an imported account's currency.")
            if any(old[name] is not None and name not in fields for name in ("target", "safety_buffer")):
                raise HistoryError("Replace or clear each existing money setting when currency or precision changes.")
        account_id = account_id or _id()
        values["identity_evidence"] = evidence.quote
        if old:
            changed = {name: values[name] for name in (*fields, "identity_evidence")}
            connection.execute("UPDATE accounts SET " + ",".join(f"{name}=?" for name in changed) + " WHERE id=?", (*changed.values(), account_id))
        else:
            values["id"] = account_id
            connection.execute("INSERT INTO accounts (" + ",".join(values) + ") VALUES (" + ",".join("?" for _ in values) + ")", tuple(values.values()))
        _change(connection, "account", account_id, {"before": dict(old) if old else None, "fields": dict(fields), "evidence": asdict(evidence)})
        return account_id


def save_card(history: Path, account_id: str, alias: str, evidence: Evidence, *, card_id: str | None = None, masked_suffix: str | None = None, active_start: str | None = None, active_end: str | None = None) -> str:
    _evidence(evidence)
    if not alias.strip():
        raise HistoryError("Supply a card alias.")
    for value in (active_start, active_end):
        if value is not None:
            _date(value)
    if active_start and active_end and active_start > active_end:
        raise HistoryError("Card active dates are reversed.")
    with _connect(history, write=True) as connection:
        if not connection.execute("SELECT 1 FROM accounts WHERE id=?", (account_id,)).fetchone():
            raise HistoryError("Select an existing parent account.")
        old = connection.execute("SELECT * FROM cards WHERE id=?", (card_id,)).fetchone()
        if card_id and (not old or old["account_id"] != account_id):
            raise HistoryError("Do not silently move or merge a card.")
        card_id = card_id or _id()
        connection.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET alias=excluded.alias, masked_suffix=excluded.masked_suffix, active_start=excluded.active_start, active_end=excluded.active_end, identity_evidence=excluded.identity_evidence", (card_id, account_id, alias, masked_suffix, active_start, active_end, evidence.quote))
        _change(connection, "card", card_id, {"before": dict(old) if old else None, "evidence": asdict(evidence)})
        return card_id


def save_period_note(history: Path, account_id: str, start: str, end: str, kind: Literal["unavailable", "no_activity", "inactive"], evidence: Evidence, *, note_id: str | None = None, withdraw: bool = False) -> str:
    if type(withdraw) is not bool:
        raise HistoryError("The withdraw choice must be true or false.")
    if kind not in {"unavailable", "no_activity", "inactive"} or _date(start) > _date(end) or evidence.kind != "user":
        raise HistoryError("A period note needs ordered dates, a supported kind and a user answer.")
    _evidence(evidence)
    with _connect(history, write=True) as connection:
        if withdraw:
            row = connection.execute("SELECT * FROM periods WHERE id=? AND account_id=? AND kind!='verified'", (note_id, account_id)).fetchone()
            if not row:
                raise HistoryError("Select an existing user period note.")
            connection.execute("UPDATE periods SET active=0 WHERE id=?", (note_id,))
        else:
            if note_id is not None:
                raise HistoryError("Create a new note or explicitly withdraw one.")
            note_id = _id()
            connection.execute("INSERT INTO periods VALUES (?,?, 'account', NULL, ?,?,?,NULL,?,1)", (note_id, account_id, start, end, kind, evidence.quote))
        _change(connection, "period_note", note_id, {"withdraw": withdraw, "evidence": asdict(evidence)})
        return note_id


def _source(source: Path) -> tuple[str, int]:
    if source.is_symlink() or not source.is_file() or source.suffix.lower() not in {".pdf", ".csv", ".xlsx"}:
        raise HistoryError("Supply a regular PDF, CSV or XLSX file.")
    digest, size = hashlib.sha256(), 0
    with source.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            if size > 50 * 1024 * 1024:
                raise HistoryError("The source exceeds 50 MiB.")
            digest.update(block)
    return digest.hexdigest(), size


def _retain_source(history: Path, source: Path, digest: str, size: int) -> Path:
    _, directory = _history_paths(history)
    destination = directory / digest
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_file() or _hash_copy(destination) != (digest, size):
            raise HistoryError("The retained source is missing or changed; recovery is required.")
        return destination
    temporary = directory / (".pending-" + _id())
    try:
        with source.open("rb") as incoming, temporary.open("xb") as outgoing:
            os.chmod(temporary, 0o600)
            while block := incoming.read(1024 * 1024):
                outgoing.write(block)
                if outgoing.tell() > 50 * 1024 * 1024:
                    raise HistoryError("The source changed or exceeds 50 MiB.")
            outgoing.flush()
            os.fsync(outgoing.fileno())
        if _hash_copy(temporary) != (digest, size):
            raise HistoryError("The source changed while it was copied.")
        os.link(temporary, destination)
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except FileExistsError:
        if destination.is_symlink() or _hash_copy(destination) != (digest, size):
            raise HistoryError("The retained source conflicts with this file.") from None
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def _hash_copy(path: Path) -> tuple[str, int]:
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            if size > 50 * 1024 * 1024:
                raise HistoryError("The managed source exceeds 50 MiB.")
            digest.update(block)
    return digest.hexdigest(), size


def _gaps(start: str, end: str, intervals: Sequence[tuple[str, str]]) -> list[tuple[str, str]]:
    cursor, last = _date(start), _date(end)
    gaps = []
    for left, right in sorted(intervals):
        left_date, right_date = _date(left), _date(right)
        if right_date < cursor or left_date > last:
            continue
        if left_date > cursor:
            gaps.append((cursor.isoformat(), (left_date - timedelta(days=1)).isoformat()))
        if right_date >= last:
            return gaps
        cursor = max(cursor, right_date + timedelta(days=1))
    if cursor <= last:
        gaps.append((cursor.isoformat(), last.isoformat()))
    return gaps


def _coverage(connection: sqlite3.Connection, account_id: str, scope: str, card_id: str | None) -> list[sqlite3.Row]:
    return connection.execute("SELECT * FROM periods WHERE account_id=? AND kind='verified' AND active=1 AND (scope='account' OR (scope=? AND card_id IS ?))", (account_id, scope, card_id)).fetchall()


def _fingerprint(record: Record) -> str:
    values = asdict(record)
    values["evidence"].pop("location")
    values.pop("uncertainty")
    if record.raw_amount is not None:
        values["amount"] = record.raw_amount
    for name in ("raw_amount", "amount_location", "sign_evidence"):
        values.pop(name)
    values.pop("date_locations")
    return hashlib.sha256(_json(values).encode()).hexdigest()


def _validate_statement(connection: sqlite3.Connection, statement: Statement) -> sqlite3.Row | None:
    if type(statement.complete) is not bool or any(type(record.reliable_reference) is not bool for record in statement.records):
        raise HistoryError("Complete and reliable-reference choices must be true or false.")
    if not statement.section.strip() or not statement.reader.strip() or len(statement.text.encode()) > 64 * 1024 * 1024 or len(statement.records) > 250_000:
        raise HistoryError("Missing section/reader or statement limits exceeded.")
    _evidence(statement.identity_evidence, statement.text)
    for value, evidence in ((statement.start, statement.start_evidence), (statement.end, statement.end_evidence)):
        _boundary(value, evidence, statement.text)
    if statement.start and statement.end and statement.start > statement.end:
        raise HistoryError("Statement dates are reversed; ask the user.")
    if statement.scope not in {None, "account", "card"} or statement.date_basis not in {None, "transaction", "posting"} or statement.outcome not in {None, "failed", "unsupported"}:
        raise HistoryError("Unsupported scope, date basis or outcome.")
    if (statement.scope == "card") != (statement.card_id is not None):
        raise HistoryError("Card scope needs one identified card.")
    account = connection.execute("SELECT * FROM accounts WHERE id=?", (statement.account_id,)).fetchone()
    if statement.account_id is not None and account is None:
        raise HistoryError("Select an existing account.")
    for card_id in (statement.card_id, *(record.card_id for record in statement.records)):
        if card_id is not None:
            card = connection.execute("SELECT account_id FROM cards WHERE id=?", (card_id,)).fetchone()
            if not card or card[0] != statement.account_id:
                raise HistoryError("Card evidence must belong to the selected account.")
            if statement.scope == "card" and card_id != statement.card_id:
                raise HistoryError("A card-only section must not contain another card's records.")
    return account


def _record_problem(record: Record, statement: Statement, account: sqlite3.Row | None) -> tuple[int | None, str | None]:
    _evidence(record.evidence, statement.text)
    if record.kind not in {"transaction", "balance"} or record.status not in {None, "pending", "posted"}:
        raise HistoryError("Unsupported record kind or transaction status.")
    for field in ("transaction_date", "posting_date", "balance_date"):
        value = getattr(record, field)
        if value is not None:
            try:
                _date(value)
                if field not in dict(record.date_locations):
                    _boundary(value, record.evidence, statement.text, period=False)
            except HistoryError as error:
                return None, str(error)
    for value in (record.description, record.bank_reference):
        if value is not None and value not in record.evidence.quote:
            raise HistoryError("Proposed record text is absent from its source quotation.")
    if record.reliable_reference and not record.bank_reference:
        raise HistoryError("A reliable bank reference needs a source value.")
    if record.uncertainty:
        return None, record.uncertainty
    if not account or not account["currency"] or record.currency != account["currency"]:
        return None, "Confirm account and currency."
    raw_amount = record.raw_amount if record.raw_amount is not None else record.amount
    if raw_amount is None or not isinstance(raw_amount, str) or (record.amount_location is None and not re.search(r"(?<![\w.,+\-−(])" + re.escape(raw_amount) + r"(?![\w.,+\-−)])", record.evidence.quote)):
        return None, "Confirm exact signed amount from source evidence."
    try:
        amount = minor_units(record.amount, account["precision"])
        original_amount = minor_units(raw_amount, account["precision"])
        if amount != original_amount:
            sign = record.sign_evidence
            if sign is None or amount != -abs(original_amount) or not re.search(r"\b(debit|negative)\b", sign.quote, re.IGNORECASE):
                return None, "Confirm the source amount and debit/credit sign convention."
    except HistoryError as error:
        return None, str(error)
    if record.kind == "balance":
        if not record.balance_date or record.balance_type not in {"opening", "closing", "current", "ledger", "available"}:
            return amount, "Confirm balance date and type."
    elif not (record.transaction_date or record.posting_date) or record.status is None:
        return amount, "Confirm transaction dates and pending/posted state."
    return amount, None


def _same_transaction(row: sqlite3.Row, record: Record, amount: int, card_id: str | None) -> bool:
    return all(row[key] == value for key, value in (
        ("transaction_date", record.transaction_date), ("posting_date", record.posting_date),
        ("amount", amount), ("currency", record.currency), ("status", record.status),
        ("card_id", card_id), ("description", record.description),
    ))


def _process_section(connection: sqlite3.Connection, file_id: str, statement: Statement, *, save: bool) -> dict[str, object]:
    account = _validate_statement(connection, statement)
    old = connection.execute("SELECT * FROM statements WHERE file_id=? AND section=?", (file_id, statement.section)).fetchone()
    if old:
        if old['outcome'] in {'corrected', 'replaced'}:
            raise HistoryError("This source has explicit maintenance changes; do not replay its original values.")
        for name in ("account_id", "scope", "card_id", "start", "end", "date_basis"):
            value = getattr(statement, name)
            if old[name] is not None and old[name] != value:
                raise HistoryError("Saved statement details changed; use explicit correction.")
    questions = []
    if account is None or statement.scope is None:
        questions.append("Confirm the account and statement scope.")
    if not statement.start or not statement.end:
        questions.append("Supply missing statement boundaries from the header or a user answer.")
    confirmed = not questions
    coverage = _coverage(connection, statement.account_id, statement.scope, statement.card_id) if confirmed else []
    gaps = _gaps(statement.start, statement.end, [(row["start"], row["end"]) for row in coverage]) if confirmed else []
    statement_id = old["id"] if old else _id()
    result: dict[str, object] = {"section": statement.section, "statement_id": statement_id, "outcome": "partially_imported", "added": 0, "matched": 0, "unresolved": 0, "source_records": 0, "uncovered": gaps, "coverage_used": [row["id"] for row in coverage], "questions": questions}
    if confirmed and not gaps:
        result.update(outcome="already_represented", explanation="Completed coverage includes this period; individual rows were not checked.")
    elif statement.outcome:
        result.update(outcome=statement.outcome, explanation="The reader did not complete this section.")
    if old and result["outcome"] == "already_represented":
        if save:
            _change(connection, "import", statement_id, result)
        return result


    if save:
        connection.execute("INSERT INTO statements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(file_id,section) DO UPDATE SET account_id=excluded.account_id, scope=excluded.scope, card_id=excluded.card_id, start=excluded.start, end=excluded.end, start_evidence=excluded.start_evidence, end_evidence=excluded.end_evidence, date_basis=excluded.date_basis, reader=excluded.reader, outcome=excluded.outcome, questions=excluded.questions", (statement_id, file_id, statement.section, statement.account_id, statement.scope, statement.card_id, statement.start, statement.end, _json(asdict(statement.start_evidence)) if statement.start_evidence else None, _json(asdict(statement.end_evidence)) if statement.end_evidence else None, statement.date_basis, statement.reader, result["outcome"], _json(questions)))
    if result["outcome"] in {"already_represented", "failed", "unsupported"}:
        if save:
            _change(connection, "import", statement_id, result)
        return result
    previous = connection.execute("SELECT * FROM statement_records WHERE statement_id=?", (statement_id,)).fetchall()
    occurrences: Counter[str] = Counter()
    incoming = Counter(_fingerprint(record) for record in statement.records)
    saved = Counter(row["fingerprint"] for row in previous)
    if saved - incoming:
        raise HistoryError("Reader output does not agree with saved source records; review before retry.")
    prior = {(row["fingerprint"], row["occurrence"]): row for row in previous}
    existing_transactions = connection.execute("SELECT * FROM transactions WHERE account_id=? AND active=1", (statement.account_id,)).fetchall()
    seen_references: set[str] = set()
    for record in statement.records:
        fingerprint = _fingerprint(record)
        occurrences[fingerprint] += 1
        saved_record = prior.get((fingerprint, occurrences[fingerprint]))
        record_id = saved_record["id"] if saved_record else _id()
        amount, problem = _record_problem(record, statement, account)
        if record.reliable_reference:
            if record.bank_reference in seen_references:
                problem = "Repeated bank reference in this source; ask before counting another transaction."
            seen_references.add(record.bank_reference)
        if not confirmed:
            problem = problem or "Statement period or account scope is unconfirmed."
        basis_date = record.posting_date if statement.date_basis == "posting" else record.transaction_date
        if confirmed and record.kind == "transaction" and (statement.date_basis is None or basis_date is None):
            problem = problem or "Confirm the date basis before assigning the record to a period."
        if confirmed and record.kind == "balance":
            basis_date = record.balance_date
        in_gap = basis_date is not None and any(left <= basis_date <= right for left, right in gaps)
        if confirmed and basis_date and not (statement.start <= basis_date <= statement.end):
            problem = problem or "Record date falls outside the confirmed statement period."
        transaction_id = saved_record["transaction_id"] if saved_record else None
        accepted = bool(saved_record and saved_record["accepted"])
        if not problem and confirmed and not in_gap:
            # Covered rows provide comparison evidence, but never new financial data.
            if record.kind == "transaction":
                refs = [row for row in existing_transactions if record.reliable_reference and row["reliable_reference"] and row["bank_reference"] == record.bank_reference]
                if refs and any(not _same_transaction(row, record, amount, record.card_id or statement.card_id) for row in refs):
                    problem = "Covered record conflicts with accepted data; request a correction."
        elif not problem and in_gap and not accepted:
            if record.kind == "balance":
                accepted = True
            else:
                matches = []
                for row in existing_transactions:
                    if record.reliable_reference and row["reliable_reference"]:
                        same = row["bank_reference"] == record.bank_reference
                    else:
                        same = all(row[key] == value for key, value in (("transaction_date", record.transaction_date), ("posting_date", record.posting_date), ("amount", amount), ("currency", record.currency), ("description", record.description), ("card_id", record.card_id or statement.card_id)))
                    if same:
                        matches.append(row)
                if matches:
                    reliable = [row for row in matches if record.reliable_reference and row["reliable_reference"] and record.bank_reference and row["bank_reference"] == record.bank_reference]
                    if len(reliable) == 1 and _same_transaction(reliable[0], record, amount, record.card_id or statement.card_id):
                        transaction_id, accepted = reliable[0]["id"], True
                        result["matched"] += 1
                    else:
                        problem = "Possible match or changed transaction; ask before counting it."
                else:
                    transaction_id, accepted = _id(), True
                    result["added"] += 1
        if problem:
            result["unresolved"] += 1
            if problem not in questions:
                questions.append(problem)
        if save and saved_record is None:
            connection.execute("INSERT INTO statement_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (record_id, statement_id, fingerprint, occurrences[fingerprint], record.kind, _json({"location": record.evidence.location, "amount_location": record.amount_location, "date_locations": record.date_locations, "sign_evidence": asdict(record.sign_evidence) if record.sign_evidence else None}), record.evidence.quote, record.transaction_date, record.posting_date, record.raw_amount if record.raw_amount is not None else record.amount, amount, record.currency, record.description, record.bank_reference, int(record.reliable_reference), record.card_id or statement.card_id, record.status, record.balance_date, record.balance_type, problem, None, 0, 0))
        if save and accepted and transaction_id and not connection.execute("SELECT 1 FROM transactions WHERE id=?", (transaction_id,)).fetchone():
            connection.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1)", (transaction_id, statement.account_id, record.card_id or statement.card_id, record.transaction_date, record.posting_date, amount, record.currency, record.description, record.bank_reference, int(record.reliable_reference), record.status, record_id))
        if save:
            connection.execute("UPDATE statement_records SET amount_minor=?, uncertainty=?, transaction_id=?, accepted=? WHERE id=?", (amount, problem, transaction_id, int(accepted), record_id))
            if saved_record and record.sign_evidence is not None:
                _change(connection, "record_answer", record_id, {"sign_evidence": asdict(record.sign_evidence), "amount_location": record.amount_location, "accepted_amount": str(amount) if amount is not None else None})
        result["source_records"] += 1
    complete = confirmed and statement.complete and not result["unresolved"]
    if complete:
        result["outcome"] = "imported"
        if save:
            for start, end in gaps:
                connection.execute("INSERT INTO periods VALUES (?,?,?,?,? ,?,'verified',?,?,1)", (_id(), statement.account_id, statement.scope, statement.card_id, start, end, statement_id, "Complete source with confirmed header/user period"))
    elif not statement.complete:
        questions.append("Confirm that all required source information was read.")
    if save:
        connection.execute("UPDATE statements SET outcome=?, questions=? WHERE id=?", (result["outcome"], _json(questions), statement_id))
        _change(connection, "import", statement_id, {"result": result, "identity": asdict(statement.identity_evidence), "start": asdict(statement.start_evidence) if statement.start_evidence else None, "end": asdict(statement.end_evidence) if statement.end_evidence else None})
    return result


def check_statement(history: Path, source: Path, sections: Sequence[Statement]) -> list[dict[str, object]]:
    """Check without saving files, plans, records or coverage."""
    digest, _ = _source(Path(source))
    _check_sections(sections)
    sections = _verify_source(history, source, sections, digest)
    with _connect(history) as connection:
        _check_copies(connection, history)
        row = connection.execute("SELECT id FROM files WHERE content_hash=?", (digest,)).fetchone()
        return [_process_section(connection, row[0] if row else "", section, save=False) for section in sections]


def _check_sections(sections: Sequence[Statement]) -> None:
    if not sections or len({section.section for section in sections}) != len(sections):
        raise HistoryError("Supply distinct statement sections for this file.")
    if sum(len(section.records) for section in sections) > 250_000:
        raise HistoryError("The file exceeds 250,000 records.")
    if len(_json([asdict(section) for section in sections]).encode()) > 16 * 1024 * 1024:
        raise HistoryError("Proposed input exceeds 16 MiB.")


def _date_heading(headers: Sequence[dict[str, object]], location: str, reference: str) -> str | None:
    column = re.sub(r"[0-9]+$", "", reference) or reference
    for header in headers:
        if location.startswith("sheet:") and not header["location"].startswith(location.rsplit(":row:", 1)[0] + ":row:"):
            continue
        names = {cell["text"].strip().lower() for cell in header["cells"]}
        if not names & {"date", "transaction date", "posting date", "balance date", "as of date"}:
            continue
        return next((cell["text"].strip().lower() for cell in header["cells"] if (re.sub(r"[0-9]+$", "", cell["reference"]) or cell["reference"]) == column), None)
    return None


def _verify_source(history: Path, source: Path, sections: Sequence[Statement], digest: str, *, force_records: bool = False) -> tuple[Statement, ...]:
    spec = importlib.util.spec_from_file_location("_bank_statement_reader", Path(__file__).with_name("statement_reader.py"))
    if spec is None or spec.loader is None:
        raise HistoryError("The protected statement reader is missing.")
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    headers = reader.read_statement(source, mode="headers")
    if headers["outcome"] != "read" or headers["source_hash"] != digest:
        raise HistoryError(headers.get("explanation", "The header read did not match the source file."))
    header_locations = {fragment["location"]: fragment for fragment in headers["fragments"]}
    need_records = force_records
    with _connect(history) as connection:
        for section in sections:
            _validate_statement(connection, section)
            for evidence, period in ((section.identity_evidence, False), (section.start_evidence, True), (section.end_evidence, True)):
                if evidence is None or evidence.kind == "user":
                    continue
                fragment = header_locations.get(evidence.location)
                if not fragment or not fragment["usable"] or evidence.quote not in fragment["text"] or (period and not fragment["header"]):
                    raise HistoryError("Header evidence does not match explicit period metadata at its source location.")
            if section.account_id and section.scope and section.start and section.end:
                coverage = _coverage(connection, section.account_id, section.scope, section.card_id)
                if not _gaps(section.start, section.end, [(row["start"], row["end"]) for row in coverage]):
                    continue
            need_records = True
    if not need_records:
        return tuple(sections)
    reading = reader.read_statement(source, mode="records")
    if reading["outcome"] != "read" or reading["source_hash"] != digest:
        raise HistoryError(reading.get("explanation", "The full read did not match the source file."))
    locations = {fragment["location"]: fragment for fragment in reading["fragments"]}
    verified = []
    for section in sections:
        records = []
        for record in section.records:
            fragment = locations.get(record.evidence.location)
            if record.evidence.kind != "record" or not fragment or record.evidence.quote != fragment["text"]:
                raise HistoryError("A record quotation or location does not match the protected source read.")
            problem = record.uncertainty
            cells = fragment["cells"]
            raw = record.raw_amount if record.raw_amount is not None else record.amount
            amount_column = None
            if not fragment["usable"]:
                problem = problem or "This row contains unsupported cell values."
            if len(cells) > 1 or record.amount_location is not None:
                cell = next((cell for cell in cells if record.amount_location == f"{record.evidence.location}:cell:{cell['reference']}"), None)
                if cell is None or cell["text"] != raw:
                    problem = problem or "Identify the exact source cell for this amount."
                elif cell.get("date_style"):
                    problem = problem or "A date-formatted cell cannot supply a money amount."
                elif cell:
                    amount_column = re.sub(r"[0-9]+$", "", cell["reference"]) or cell["reference"]
                    for header in headers["fragments"]:
                        if record.evidence.location.startswith("sheet:") and not header["location"].startswith(record.evidence.location.rsplit(":row:", 1)[0] + ":row:"):
                            continue
                        names = {entry["text"].strip().lower() for entry in header["cells"]}
                        if not names & {"date", "transaction date", "posting date"}:
                            continue
                        heading = next((entry["text"].strip().lower() for entry in header["cells"] if (re.sub(r"[0-9]+$", "", entry["reference"]) or entry["reference"]) == amount_column), None)
                        if record.kind == "transaction" and heading not in {"amount", "transaction amount", "debit", "credit"}:
                            problem = problem or "The selected cell is not a supported transaction amount column."
                        if heading in {"debit", "credit"} and (record.sign_evidence is None or (heading == "debit" and not str(record.amount).startswith("-")) or (heading == "credit" and str(record.amount).startswith("-"))):
                            problem = problem or "Confirm the signed value for the selected debit or credit column."
            if record.sign_evidence:
                _evidence(record.sign_evidence)
                if record.sign_evidence.kind == "header":
                    sign_fragment = header_locations.get(record.sign_evidence.location)
                    if not sign_fragment or record.sign_evidence.quote not in sign_fragment["text"]:
                        raise HistoryError("The sign convention is absent from its source header.")
                    if len(cells) > 1:
                        sign_cells = sign_fragment["cells"]
                        sign_cell = next((entry for entry in sign_cells if (re.sub(r"[0-9]+$", "", entry["reference"]) or entry["reference"]) == amount_column), None)
                        if sign_cell is None or sign_cell["text"] != record.sign_evidence.quote:
                            problem = problem or "The sign convention does not identify this amount column."
                elif record.sign_evidence.kind != "user":
                    raise HistoryError("Use a source header or user answer for sign conventions.")
            if len(dict(record.date_locations)) != len(record.date_locations) or any(field not in {"transaction_date", "posting_date", "balance_date"} for field, _ in record.date_locations):
                raise HistoryError("Supply each supported date field at most once.")
            date_locations = dict(record.date_locations)
            used_dates = set()
            for field, headings in (("transaction_date", {"date", "transaction date"}), ("posting_date", {"posting date"}), ("balance_date", {"date", "balance date", "as of date"})):
                value = getattr(record, field)
                if value is None:
                    continue
                location = date_locations.get(field)
                if len(cells) <= 1 and location is None:
                    continue
                candidates = [cell for cell in cells if (location is None or location == f"{record.evidence.location}:cell:{cell['reference']}") and (cell.get("canonical_date") == value or cell["text"] == value) and _date_heading(headers["fragments"], record.evidence.location, cell["reference"]) in headings]
                if len(candidates) != 1 or candidates[0]["reference"] in used_dates:
                    problem = problem or "The date needs a separate source cell with the correct date-column meaning."
                    continue
                date_cell = candidates[0]
                used_dates.add(date_cell["reference"])
                date_locations[field] = f"{record.evidence.location}:cell:{date_cell['reference']}"
            records.append(replace(record, uncertainty=problem, date_locations=tuple(date_locations.items())))
        verified.append(replace(section, records=tuple(records), reader=str(reading["reader"])))
    return tuple(verified)


def _save_statement(history: Path, source: Path, sections: Sequence[Statement]) -> list[dict[str, object]]:
    """Recheck and save one file atomically. Earlier files stay committed."""
    source = Path(source)
    _check_sections(sections)
    digest, size = _source(source)
    sections = _verify_source(history, source, sections, digest)
    with _connect(history, write=True) as connection:
        _check_copies(connection, history)
        _, directory = _history_paths(history)
        for temporary in directory.glob(".pending-*"):
            if temporary.is_file() and not temporary.is_symlink():
                temporary.unlink()
        destination = _retain_source(history, source, digest, size)
        row = connection.execute("SELECT * FROM files WHERE content_hash=?", (digest,)).fetchone()
        file_id = row["id"] if row else _id()
        if row and row["managed_path"] != destination.name:
            raise HistoryError("The saved source path is invalid.")
        connection.execute("INSERT INTO files VALUES (?,?,?,?,?,?, 'ready') ON CONFLICT(content_hash) DO UPDATE SET copy_state='ready'", (file_id, digest, size, source.suffix.lower()[1:], source.name, destination.name))
        results = [_process_section(connection, file_id, section, save=True) for section in sections]
        if _hash_copy(destination) != (digest, size):
            raise HistoryError("The source copy changed before save; no financial data was committed.")
        return results


def save_statement(history: Path, source: Path, sections: Sequence[Statement]) -> list[dict[str, object]]:
    """Save one file; retain failed-attempt evidence when the history permits it."""
    try:
        return _save_statement(history, source, sections)
    except (HistoryError, OSError) as error:
        try:
            with _connect(history, write=True) as connection:
                _change(connection, "import_failed", _id(), {"file": Path(source).name, "outcome": "failed", "reason": str(error)})
        except (HistoryError, OSError):
            # A damaged or inaccessible history cannot record its own failure.
            pass
        raise


def _reconcile(connection: sqlite3.Connection, statement: sqlite3.Row) -> dict[str, object]:
    result: dict[str, object] = {"statement_id": statement["id"], "outcome": "unavailable", "explanation": "Need complete account data, dated opening/closing balances and a confirmed date basis."}
    if statement["scope"] != "account" or statement["outcome"] != "imported" or statement["date_basis"] is None:
        return result
    account_type = connection.execute("SELECT type FROM accounts WHERE id=?", (statement["account_id"],)).fetchone()[0]
    if account_type not in {"transaction", "savings"}:
        result["explanation"] = "The account's balance and movement sign convention is not established for reconciliation."
        return result
    balances = connection.execute("SELECT * FROM statement_records WHERE statement_id=? AND kind='balance' AND accepted=1 AND superseded=0", (statement["id"],)).fetchall()
    openings = [row for row in balances if row["balance_type"] == "opening" and row["balance_date"] == statement["start"]]
    closings = [row for row in balances if row["balance_type"] == "closing" and row["balance_date"] == statement["end"]]
    if len(openings) != 1 or len(closings) != 1 or openings[0]["currency"] != closings[0]["currency"]:
        return result
    date_column = "posting_date" if statement["date_basis"] == "posting" else "transaction_date"
    rows = connection.execute(f"SELECT * FROM transactions WHERE account_id=? AND active=1 AND {date_column} BETWEEN ? AND ?", (statement["account_id"], statement["start"], statement["end"])).fetchall()
    if any(row["status"] != "posted" or row["currency"] != openings[0]["currency"] for row in rows):
        return result
    difference = openings[0]["amount_minor"] + sum(row["amount"] for row in rows) - closings[0]["amount_minor"]
    result.update(outcome="matched" if difference == 0 else "discrepancy", difference=str(difference), currency=openings[0]["currency"], evidence=[openings[0]["id"], closings[0]["id"]], explanation="Opening balance plus accepted movements minus closing balance; no adjustment was added.")
    return result


def read_history(history: Path, *, account_id: str | None = None, start: str | None = None, end: str | None = None) -> dict[str, object]:
    """Read accepted data, separate unresolved records, and explicit horizon gaps."""
    if (start is None) != (end is None) or (start and _date(start) > _date(end)):
        raise HistoryError("Supply both ordered review boundaries or neither.")
    with _connect(history) as connection:
        accounts = connection.execute("SELECT * FROM accounts" + (" WHERE id=?" if account_id else ""), (account_id,) if account_id else ()).fetchall()
        result: dict[str, object] = {"accounts": [], "transactions": [], "balances": [], "unresolved": [], "statements": [], "sources": [], "gaps": [], "periods": [], "reconciliation": [], "limitations": []}
        for account in accounts:
            account_values = dict(account)
            for field in ("target", "safety_buffer"):
                if account_values[field] is not None:
                    account_values[field] = str(account_values[field])
            account_values["cards"] = [dict(row) for row in connection.execute("SELECT * FROM cards WHERE account_id=?", (account["id"],))]
            result["accounts"].append(account_values)
            transactions = connection.execute("SELECT * FROM transactions WHERE account_id=? AND active=1", (account["id"],)).fetchall()
            for row in transactions:
                when = row["posting_date"] or row["transaction_date"]
                if not start or (when and start <= when <= end):
                    result["transactions"].append({**dict(row), "amount": str(row["amount"])})
            for row in connection.execute("SELECT r.*, s.account_id, s.start, s.end FROM statement_records r JOIN statements s ON s.id=r.statement_id WHERE s.account_id=? AND r.superseded=0", (account["id"],)):
                values = {**dict(row), "amount_minor": str(row["amount_minor"]) if row["amount_minor"] is not None else None}
                if row["uncertainty"]:
                    result["unresolved"].append(values)
                if row["kind"] == "balance" and row["accepted"]:
                    if not start or start <= row["balance_date"] <= end:
                        result["balances"].append(values)
            periods = connection.execute("SELECT * FROM periods WHERE account_id=? AND active=1", (account["id"],)).fetchall()
            result["periods"].extend(dict(row) for row in periods)
            if start and account["expected"]:
                left, right = max(start, account["active_start"] or start), min(end, account["active_end"] or end)
                if left <= right:
                    intervals = [(row["start"], row["end"]) for row in periods if row["kind"] == "verified" and row["scope"] == "account"]
                    result["gaps"].extend({"account_id": account["id"], "start": a, "end": b} for a, b in _gaps(left, right, intervals))
            for row in connection.execute("SELECT * FROM statements WHERE account_id=?", (account["id"],)):
                result["statements"].append(dict(row))
                result["reconciliation"].append(_reconcile(connection, row))
        result["unresolved"].extend(dict(row) for row in connection.execute("SELECT r.* FROM statement_records r JOIN statements s ON s.id=r.statement_id WHERE s.account_id IS NULL") if account_id is None)
        if account_id is None:
            result["statements"].extend(dict(row) for row in connection.execute("SELECT * FROM statements WHERE account_id IS NULL"))
        result["attempts"] = [dict(row) for row in connection.execute("SELECT * FROM changes WHERE kind IN ('import','import_failed','correction','replacement') ORDER BY rowid")]
        if account_id is None:
            result['sources'] = [dict(row) for row in connection.execute('SELECT * FROM files')]
        else:
            relevant_ids = {account_id}
            for table in ('accounts', 'cards', 'statements', 'transactions', 'periods'):
                column = 'id' if table == 'accounts' else 'account_id'
                relevant_ids.update(row[0] for row in connection.execute('SELECT id FROM ' + table + ' WHERE ' + column + '=?', (account_id,)))
            relevant_ids.update(row[0] for row in connection.execute('SELECT r.id FROM statement_records r JOIN statements s ON s.id=r.statement_id LEFT JOIN transactions t ON t.id=r.transaction_id WHERE s.account_id=? OR t.account_id=?', (account_id, account_id)))
            visible_changes = []
            for change in result['attempts']:
                reassigned = False
                if change['kind'] == 'correction':
                    values = json.loads(change['evidence'])
                    reassigned = any(values.get(side, {}).get('account_id') == account_id for side in ('old', 'new'))
                if change['affected_id'] in relevant_ids or reassigned:
                    visible_changes.append(change)
            result['attempts'] = visible_changes
            result['sources'] = [dict(row) for row in connection.execute('SELECT f.* FROM files f WHERE EXISTS (SELECT 1 FROM statements s LEFT JOIN statement_records r ON r.statement_id=s.id LEFT JOIN transactions t ON t.id=r.transaction_id WHERE s.file_id=f.id AND (s.account_id=? OR t.account_id=?))', (account_id, account_id))]
        for source in result["sources"]:
            _, directory = _history_paths(history)
            path = _managed_source(directory, source)
            source["copy_available"] = path.is_file() and not path.is_symlink() and _hash_copy(path) == (source["content_hash"], source["size"])
            if not source["copy_available"]:
                result["limitations"].append("A retained source is missing or changed; its records are not fully persisted.")
        if not start:
            result["limitations"].append("Supply a review period to calculate gaps.")
        return result




def _user_instruction(evidence: Evidence) -> None:
    _evidence(evidence)
    if evidence.kind != "user":
        raise HistoryError("Maintenance needs an explicit user instruction and reason.")


def _invalidate_statements(connection: sqlite3.Connection, statement_ids: Sequence[str]) -> None:
    for statement_id in statement_ids:
        connection.execute("DELETE FROM periods WHERE statement_id=? AND kind='verified'", (statement_id,))
        connection.execute("UPDATE statements SET outcome='corrected' WHERE id=?", (statement_id,))


def apply_correction(history: Path, transaction_id: str, fields: Mapping[str, object], evidence: Evidence,
                     *, expected: Mapping[str, object] | None = None) -> dict[str, object]:
    """Keep original observations and the stable ID; save old/new accepted values together."""
    _user_instruction(evidence)
    allowed = {"account_id", "card_id", "transaction_date", "posting_date", "amount", "description", "status", "bank_reference", "reliable_reference"}
    if not fields or set(fields) - allowed:
        raise HistoryError("Select supported transaction fields only.")
    with _connect(history, write=True) as connection:
        _check_copies(connection, history)
        row = connection.execute("SELECT * FROM transactions WHERE id=? AND active=1", (transaction_id,)).fetchone()
        if row is None:
            raise HistoryError("Select an active transaction.")
        if expected is not None and (set(expected) - set(row.keys()) or any(row[key] != value for key, value in expected.items())):
            raise HistoryError("The selected values changed; review the correction again.")
        values = {**dict(row), **fields}
        account = connection.execute("SELECT * FROM accounts WHERE id=?", (values['account_id'],)).fetchone()
        old_account = connection.execute("SELECT * FROM accounts WHERE id=?", (row['account_id'],)).fetchone()
        if not account or account['currency'] != row['currency'] or account['precision'] != old_account['precision']:
            raise HistoryError("The selected account must use the same currency and precision.")
        if values['card_id'] is not None:
            card = connection.execute("SELECT account_id FROM cards WHERE id=?", (values['card_id'],)).fetchone()
            if not card or card[0] != account['id']:
                raise HistoryError("Select a card on the corrected account or clear the card.")
        updates = dict(fields)
        if 'amount' in updates:
            updates['amount'] = minor_units(updates['amount'], account['precision'])
        for field in ('transaction_date', 'posting_date'):
            if values[field] is not None:
                _date(values[field])
        if values['transaction_date'] is None and values['posting_date'] is None:
            raise HistoryError("Keep at least one known transaction date.")
        if values['status'] not in {'pending', 'posted'} or type(values['reliable_reference']) is not bool and values['reliable_reference'] not in (0, 1):
            raise HistoryError("Confirm transaction status and reference reliability.")
        if 'reliable_reference' in updates and type(updates['reliable_reference']) is not bool:
            raise HistoryError("Reference reliability must be true or false.")
        for field in ('description', 'bank_reference'):
            if values[field] is not None and not isinstance(values[field], str):
                raise HistoryError("Descriptions and references must be text or unknown.")
        if values['reliable_reference'] and not values['bank_reference']:
            raise HistoryError("A reliable reference needs its value.")
        old = {key: row[key] for key in updates}
        connection.execute("UPDATE transactions SET " + ', '.join(key + '=?' for key in updates) + " WHERE id=?", (*updates.values(), transaction_id))
        statements = [item[0] for item in connection.execute("SELECT DISTINCT statement_id FROM statement_records WHERE transaction_id=?", (transaction_id,))]
        if any(key in updates and updates[key] != row[key] for key in ('account_id', 'card_id', 'transaction_date', 'posting_date')):
            _invalidate_statements(connection, statements)
        _change(connection, 'correction', transaction_id, {'old': old, 'new': updates, 'evidence': asdict(evidence), 'reports_stale': True})
        return {'transaction_id': transaction_id, 'old_values': old, 'new_values': updates, 'records_updated': len(statements), 'reports_stale': True}


def _new_directory(destination: Path) -> None:
    if any(path.is_symlink() for path in (destination, *destination.parents)):
        raise HistoryError("Recovery paths must not use symbolic links.")
    try:
        destination.mkdir(mode=0o700)
    except FileExistsError as error:
        raise HistoryError("Select a new recovery folder; existing content will not be overwritten.") from error


def export_history(history: Path, destination: Path, *, copy_sources: bool = True) -> dict[str, object]:
    """Create a checked recovery copy; never replace existing content."""
    if type(copy_sources) is not bool or not copy_sources:
        raise HistoryError("A recovery copy must include its linked statement sources.")
    destination = Path(destination).absolute()
    if Path(history).absolute() in destination.parents:
        raise HistoryError("Keep a recovery copy outside the live history.")
    _history_paths(history)
    _new_directory(destination)
    try:
        (destination / 'sources').mkdir(mode=0o700)
        database = destination / 'history.sqlite3'
        descriptor = os.open(database, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        # Hold the history write lock while its database and linked sources are copied.
        with _connect(history, write=True) as connection:
            _check_copies(connection, history)
            original, sources = _history_paths(history)
            with closing(sqlite3.connect(original.as_uri() + '?mode=ro', uri=True)) as incoming:
                with closing(sqlite3.connect(database)) as outgoing:
                    incoming.backup(outgoing)
            files = connection.execute('SELECT * FROM files').fetchall()
            for row in files:
                if row['copy_state'] != 'ready' or row['managed_path'] != row['content_hash']:
                    raise HistoryError("A source copy is incomplete; recover it before export.")
                target = destination / 'sources' / row['content_hash']
                shutil.copyfile(sources / row['content_hash'], target)
                os.chmod(target, 0o600)
            with _connect(destination) as exported:
                _check_copies(exported, destination)
        return {'database': str(database), 'source_copies_exported': len(files), 'limitations': []}
    except BaseException:
        shutil.rmtree(destination)
        raise


def restore_history(source: Path, destination: Path, *, verify_copies: bool = True) -> dict[str, object]:
    """Restore a verified recovery copy into a new folder only."""
    if type(verify_copies) is not bool or not verify_copies:
        raise HistoryError("Restore must verify the database and all linked copies.")
    source = Path(source).absolute()
    if source.name != 'history.sqlite3':
        raise HistoryError("Select history.sqlite3 from the recovery folder.")
    result = export_history(source.parent, destination)
    return {'restored_database': result['database'], 'source_copies_restored': result['source_copies_exported'], 'limitations': []}


def recalculate_coverage(history: Path, account_id: str) -> dict[str, object]:
    """Keep only supported verified intervals; never infer coverage from transactions."""
    with _connect(history, write=True) as connection:
        if not connection.execute('SELECT 1 FROM accounts WHERE id=?', (account_id,)).fetchone():
            raise HistoryError("Select an existing account.")
        _check_copies(connection, history)
        periods = connection.execute("SELECT * FROM periods WHERE account_id=? AND kind='verified'", (account_id,)).fetchall()
        removed = 0
        for period in periods:
            statement = connection.execute('SELECT * FROM statements WHERE id=?', (period['statement_id'],)).fetchone()
            valid = statement and statement['outcome'] == 'imported' and all(period[key] == statement[key] for key in ('account_id', 'scope', 'card_id')) and statement['start'] <= period['start'] <= period['end'] <= statement['end']
            if not valid:
                connection.execute('DELETE FROM periods WHERE id=?', (period['id'],))
                removed += 1
        return {'account_id': account_id, 'periods_removed': removed, 'new_periods': len(periods) - removed, 'reports_stale': bool(removed)}


def check_safety_buffer(history: Path, account_id: str, period_start: str, period_end: str) -> dict[str, object]:
    """Compare a dated observed balance with its buffer; do not forecast."""
    if _date(period_start) > _date(period_end):
        raise HistoryError("Supply ordered review dates.")
    data = read_history(history, account_id=account_id, start=period_start, end=period_end)
    if not data['accounts']:
        raise HistoryError("Select an existing account.")
    account = data['accounts'][0]
    if account['type'] not in {'transaction', 'savings'}:
        return {'account_id': account_id, 'status': 'not_funding'}
    if account['safety_buffer'] is None:
        return {'account_id': account_id, 'status': 'no_buffer'}
    balances = [row for row in data['balances'] if row['balance_type'] in {'closing', 'current'} and row['currency'] == account['currency']]
    if not balances:
        return {'account_id': account_id, 'status': 'no_data'}
    latest = max(row['balance_date'] for row in balances)
    selected = [row for row in balances if row['balance_date'] == latest]
    if len({row['amount_minor'] for row in selected}) != 1 or data['limitations']:
        return {'account_id': account_id, 'status': 'unknown', 'explanation': 'Conflicting balances or missing sources need review.'}
    balance, buffer = int(selected[0]['amount_minor']), int(account['safety_buffer'])
    return {'account_id': account_id, 'status': 'at_risk' if balance < buffer else 'safe', 'balance_date': latest, 'closing_balance_minor': str(balance), 'safety_buffer_minor': str(buffer), 'margin_minor': str(balance-buffer), 'explanation': 'Observed balance only; this is not a forecast.'}


def _deletion_scope(connection: sqlite3.Connection, account_id: str | None, file_ids: Sequence[str], statement_ids: Sequence[str], transaction_ids: Sequence[str], all_data: bool) -> dict[str, object]:
    tables = {name: [dict(row) for row in connection.execute('SELECT * FROM ' + name)] for name in ('accounts', 'cards', 'files', 'statements', 'statement_records', 'transactions', 'periods', 'changes')}
    selected_statements = set(statement_ids)
    selected_transactions = set(transaction_ids)
    if account_id is not None and account_id not in {row['id'] for row in tables['accounts']}:
        raise HistoryError("Select an existing account.")
    for selected, table in ((file_ids, 'files'), (statement_ids, 'statements'), (transaction_ids, 'transactions')):
        if set(selected) - {row['id'] for row in tables[table]}:
            raise HistoryError("A selected record no longer exists; review the deletion again.")
    selected_statements.update(row['id'] for row in tables['statements'] if all_data or row['file_id'] in file_ids or account_id is not None and row['account_id'] == account_id)
    records = {row['id'] for row in tables['statement_records'] if row['statement_id'] in selected_statements or row['transaction_id'] in selected_transactions}
    support_ids: dict[str, set[str]] = {}
    for record in tables['statement_records']:
        if record['transaction_id'] is not None:
            support_ids.setdefault(record['transaction_id'], set()).add(record['id'])
    # A transaction with remaining source support survives deletion of just one source.
    for row in tables['transactions']:
        supports = support_ids.get(row['id'], set())
        if all_data or account_id is not None and row['account_id'] == account_id or supports and supports <= records:
            selected_transactions.add(row['id'])
    records.update(row['id'] for row in tables['statement_records'] if row['transaction_id'] in selected_transactions)
    affected_statements = selected_statements | {row['statement_id'] for row in tables['statement_records'] if row['id'] in records}
    candidate_files = set(file_ids) | {row['file_id'] for row in tables['statements'] if row['id'] in selected_statements}
    files = {row['id'] for row in tables['files'] if (all_data or row['id'] in candidate_files) and not any(statement['file_id'] == row['id'] and statement['id'] not in selected_statements for statement in tables['statements'])}
    cards = {row['id'] for row in tables['cards'] if all_data or account_id is not None and row['account_id'] == account_id}
    accounts = {row['id'] for row in tables['accounts'] if all_data or row['id'] == account_id}
    periods = {row['id'] for row in tables['periods'] if row['account_id'] in accounts or row['statement_id'] in affected_statements}
    affected = records | selected_transactions | selected_statements | files | cards | accounts | periods
    source_names = {row['original_name'] for row in tables['files'] if row['id'] in candidate_files}
    changes = {row['id'] for row in tables['changes'] if all_data or row['affected_id'] in affected or any(value in row['evidence'] for value in affected | source_names)}
    chosen = {'accounts': accounts, 'cards': cards, 'files': files, 'statements': selected_statements, 'statement_records': records, 'transactions': selected_transactions, 'periods': periods, 'changes': changes}
    return {'rows': {table: [row for row in tables[table] if row['id'] in ids] for table, ids in chosen.items()}, 'affected_statements': sorted(affected_statements), 'retained_sources': [row['id'] for row in tables['files'] if row['id'] not in files], 'all_data': all_data}


def delete_history(history: Path, *, evidence: Evidence, account_id: str | None = None,
                   file_ids: Sequence[str] = (), transaction_ids: Sequence[str] = (), statement_ids: Sequence[str] = (),
                   all_data: bool = False, preview: bool = True, expected: Mapping[str, object] | None = None,
                   recovery: Path | None = None, decline_recovery: bool = False,
                   backup_paths: Sequence[Path] = ()) -> dict[str, object]:
    """Explain and recheck selected effects before deleting managed data."""
    _user_instruction(evidence)
    if any(type(value) is not bool for value in (all_data, preview, decline_recovery)):
        raise HistoryError("Deletion choices must be true or false.")
    if not (all_data or account_id or file_ids or statement_ids or transaction_ids):
        raise HistoryError("Select the deletion scope explicitly.")
    if not preview and (expected is None or (recovery is None) == (not decline_recovery)):
        raise HistoryError("Review the effects and choose a recovery copy or explicitly decline it.")
    if backup_paths:
        # Backup removal accepts only explicitly named, checked recovery folders.
        for backup in backup_paths:
            backup = Path(backup).absolute()
            selected = Path(history).absolute()
            if backup == selected or backup in selected.parents or selected in backup.parents:
                raise HistoryError("A selected backup must be separate from the live history.")
            with _connect(backup) as connection:
                _check_copies(connection, backup)
    with _connect(history, write=True) as connection:
        effects = _deletion_scope(connection, account_id, file_ids, statement_ids, transaction_ids, all_data)
        effects['backup_paths'] = [str(Path(path).absolute()) for path in backup_paths]
        if preview:
            return {'effects': effects, 'external_originals_retained': True, 'limitations': ['Retained shared sources and recovery copies can still contain selected data.']}
        if effects != expected:
            raise HistoryError("The deletion effects changed; review the current effects again.")
    if recovery is not None:
        export_history(history, recovery)
    with _connect(history, write=True) as connection:
        if _deletion_scope(connection, account_id, file_ids, statement_ids, transaction_ids, all_data) != {key: value for key, value in expected.items() if key != 'backup_paths'}:
            raise HistoryError("History changed after the recovery choice; no records were deleted.")
        connection.execute('PRAGMA secure_delete=ON')
        rows = effects['rows']
        removed_records = {row['id'] for row in rows['statement_records']}
        # Break the two-way observation/accepted-transaction links before removing rows.
        for row in rows['statement_records']:
            connection.execute('UPDATE statement_records SET transaction_id=NULL WHERE id=?', (row['id'],))
            survivors = [record for record in connection.execute('SELECT id FROM statement_records WHERE transaction_id=?', (row['transaction_id'],)) if record['id'] not in removed_records] if row['transaction_id'] else []
            if survivors:
                connection.execute('UPDATE transactions SET supporting_record=? WHERE supporting_record=?', (survivors[0]['id'], row['id']))
        for table in ('transactions', 'statement_records', 'periods', 'statements', 'cards', 'accounts', 'files', 'changes'):
            for row in rows[table]:
                connection.execute('DELETE FROM ' + table + ' WHERE id=?', (row['id'],))
        _invalidate_statements(connection, effects['affected_statements'])
    _, sources = _history_paths(history)
    remaining = []
    for row in effects['rows']['files']:
        path = _managed_source(sources, row)
        try:
            path.unlink(missing_ok=True)
        except OSError:
            remaining.append(str(path))
    for backup in backup_paths:
        try:
            # The complete selected recovery folder is the explicit deletion scope.
            shutil.rmtree(backup)
        except OSError:
            remaining.append(str(backup))
    if all_data and not remaining:
        database, _ = _history_paths(history)
        database.unlink()
        for suffix in ('-journal', '-wal', '-shm'):
            database.with_name(database.name + suffix).unlink(missing_ok=True)
        # Leave unexpected files untouched and disclose them.
        remaining.extend(str(path) for path in sources.iterdir())
        if not remaining:
            sources.rmdir()
            if not any(Path(history).iterdir()):
                Path(history).rmdir()
    return {'deleted_scope': {table: [row['id'] for row in rows] for table, rows in effects['rows'].items()}, 'retained_sources': effects['retained_sources'], 'recovery_copy': str(recovery) if recovery else None, 'recovery_declined': decline_recovery, 'remaining_paths': remaining, 'external_originals_retained': True, 'reports_stale': True, 'limitations': ['External originals, retained shared sources and unselected recovery copies can still contain selected data; secure erasure is not promised.']}


def delete_records(history: Path, *, evidence: Evidence, account_id: str | None = None,
                   file_ids: Sequence[str] = (), transaction_ids: Sequence[str] = (), statement_ids: Sequence[str] = (),
                   expected: Mapping[str, object] | None = None, recovery: Path | None = None,
                   decline_recovery: bool = False, include_backups: bool = False) -> dict[str, object]:
    """Use the same checked deletion rules for selected records."""
    if type(include_backups) is not bool or include_backups:
        raise HistoryError("Name selected recovery folders with delete_history; never delete the live history as a backup.")
    return delete_history(history, evidence=evidence, account_id=account_id, file_ids=file_ids,
                          transaction_ids=transaction_ids, statement_ids=statement_ids,
                          preview=expected is None, expected=expected, recovery=recovery, decline_recovery=decline_recovery)


def correct_history(history: Path, source: Path, section: Statement, *, replace_statements: Sequence[str],
                    evidence: Evidence, expected: Mapping[str, object] | None = None,
                    recovery: Path | None = None, decline_recovery: bool = False) -> dict[str, object]:
    """Replace explicitly named statement ranges, keeping earlier evidence and matched IDs."""
    _user_instruction(evidence)
    if type(decline_recovery) is not bool or not replace_statements or len(set(replace_statements)) != len(replace_statements):
        raise HistoryError("Name distinct statements and the recovery choice.")
    if not section.complete or not section.start or not section.end or not section.account_id or section.outcome:
        raise HistoryError("A replacement needs complete source information and confirmed header dates/account.")
    source = Path(source)
    _check_sections((section,))
    digest, size = _source(source)
    section = _verify_source(history, source, (section,), digest, force_records=True)[0]
    with _connect(history) as connection:
        _check_copies(connection, history)
        old = [dict(row) for row in connection.execute('SELECT * FROM statements') if row['id'] in replace_statements]
        if len(old) != len(replace_statements) or any(row['outcome'] not in {'imported', 'corrected'} for row in old):
            raise HistoryError("Select complete or explicitly corrected statements to replace.")
        if any(any(row[key] != old[0][key] for key in ('account_id', 'scope', 'card_id')) for row in old):
            raise HistoryError("Select original sources for one account and scope per replacement.")
        if any(row['file_id'] == file['id'] and row['section'] == section.section for row in old for file in connection.execute('SELECT id FROM files WHERE content_hash=?', (digest,))):
            raise HistoryError("Use a separate correction section to retain the original source section.")
        records = [dict(row) for row in connection.execute('SELECT * FROM statement_records') if row['statement_id'] in replace_statements]
        transaction_ids = {row['transaction_id'] for row in records if row['transaction_id']}
        if any(row['transaction_id'] in transaction_ids and row['statement_id'] not in replace_statements for row in connection.execute('SELECT * FROM statement_records')):
            raise HistoryError("Another source supports a selected transaction; include its effects in the replacement review.")
        transactions = [dict(row) for row in connection.execute('SELECT * FROM transactions') if row['id'] in transaction_ids]
        effects = {'statements': old, 'records': records, 'transactions': transactions, 'replacement_hash': digest, 'replacement': asdict(section)}
    if expected is None:
        return {'effects': effects, 'reports_stale': True, 'explanation': 'Review selected original ranges and the replacement; choose a recovery copy or decline it.'}
    if expected != effects or (recovery is None) == (not decline_recovery):
        raise HistoryError("Replacement effects changed or the recovery choice is missing.")
    if recovery is not None:
        export_history(history, recovery)
    _, sources = _history_paths(history)
    retained_copy = sources / digest
    copy_existed = retained_copy.exists()
    try:
        with _connect(history, write=True) as connection:
            _check_copies(connection, history)
            for table, rows in (('statements', old), ('statement_records', records), ('transactions', transactions)):
                for row in rows:
                    current = connection.execute('SELECT * FROM ' + table + ' WHERE id=?', (row['id'],)).fetchone()
                    if current is None or dict(current) != row:
                        raise HistoryError("Selected values changed before replacement; review again.")
            _invalidate_statements(connection, replace_statements)
            for row in records:
                connection.execute('UPDATE statement_records SET superseded=1, accepted=0 WHERE id=?', (row['id'],))
            for row in transactions:
                connection.execute('UPDATE transactions SET active=0 WHERE id=?', (row['id'],))
            destination = _retain_source(history, source, digest, size)
            file = connection.execute('SELECT id FROM files WHERE content_hash=?', (digest,)).fetchone()
            file_id = file[0] if file else _id()
            if not file:
                connection.execute("INSERT INTO files VALUES (?,?,?,?,?,?, 'ready')", (file_id, digest, size, source.suffix.lower()[1:], source.name, destination.name))
            result = _process_section(connection, file_id, section, save=True)
            if result['outcome'] != 'imported':
                raise HistoryError("The replacement has unresolved records; the original data remains active.")
            new_transactions = connection.execute('SELECT t.* FROM transactions t JOIN statement_records r ON r.id=t.supporting_record WHERE r.statement_id=?', (result['statement_id'],)).fetchall()
            for new in new_transactions:
                matches = [row for row in transactions if row['reliable_reference'] and new['reliable_reference'] and row['bank_reference'] == new['bank_reference'] and row['card_id'] == new['card_id']]
                if len(matches) == 1:
                    stable_id = matches[0]['id']
                    fields = {key: new[key] for key in new.keys() if key != 'id'}
                    connection.execute('UPDATE transactions SET ' + ', '.join(key + '=?' for key in fields) + ' WHERE id=?', (*fields.values(), stable_id))
                    connection.execute('UPDATE statement_records SET transaction_id=? WHERE transaction_id=? AND superseded=0', (stable_id, new['id']))
                    connection.execute('DELETE FROM transactions WHERE id=?', (new['id'],))
                    result['added'] -= 1
                    result['matched'] += 1
            for row in old:
                connection.execute("UPDATE statements SET outcome='replaced' WHERE id=?", (row['id'],))
            if _hash_copy(destination) != (digest, size):
                raise HistoryError("Replacement source changed before save.")
            _change(connection, 'replacement', result['statement_id'], {'old': effects, 'new_statement': result['statement_id'], 'evidence': asdict(evidence), 'recovery_copy': str(recovery) if recovery else None, 'recovery_declined': decline_recovery, 'reports_stale': True})
            return {**result, 'reports_stale': True, 'recovery_copy': str(recovery) if recovery else None}
    except BaseException:
        if not copy_existed and retained_copy.exists():
            try:
                with _connect(history) as connection:
                    tracked = connection.execute('SELECT 1 FROM files WHERE content_hash=?', (digest,)).fetchone()
                if tracked is None:
                    retained_copy.unlink()
            except (HistoryError, OSError) as cleanup_error:
                raise HistoryError(f"Replacement did not finish; retained source needs review: {retained_copy}") from cleanup_error
        raise
