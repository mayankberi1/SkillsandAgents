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
import os
import re
import sqlite3
import tempfile
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal, Mapping, Sequence
from urllib.parse import urlsplit
from uuid import uuid4


class HistoryError(ValueError):
    """A history setup or database operation could not be completed."""


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


@dataclass(frozen=True)
class SetupResult:
    status: Literal["ready", "needs_choice", "use_another_database"]
    history_directory: str | None
    missing_tables: tuple[str, ...]
    message: str
    missing_columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeleteResult:
    deleted: bool
    requested_table: str
    requested_id: str
    deleted_rows: Mapping[str, tuple[str, ...]]


_CREATE_TABLES = {
    "accounts": """CREATE TABLE accounts (
        id TEXT PRIMARY KEY, alias TEXT NOT NULL, bank TEXT, type TEXT,
        identity_evidence TEXT NOT NULL, currency TEXT NOT NULL, precision INTEGER NOT NULL)""",
    "files": """CREATE TABLE files (
        id TEXT PRIMARY KEY, content_hash TEXT UNIQUE NOT NULL, size INTEGER NOT NULL,
        format TEXT NOT NULL, original_name TEXT NOT NULL, managed_path TEXT NOT NULL,
        copy_state TEXT NOT NULL)""",
    "statements": """CREATE TABLE statements (
        id TEXT PRIMARY KEY, file_id TEXT NOT NULL REFERENCES files(id), section TEXT NOT NULL,
        account_id TEXT NOT NULL REFERENCES accounts(id), scope TEXT NOT NULL, card_id TEXT,
        start TEXT, end TEXT, start_evidence TEXT, end_evidence TEXT,
        date_basis TEXT, reader TEXT NOT NULL, outcome TEXT NOT NULL, questions TEXT NOT NULL,
        UNIQUE(file_id, section))""",
    "statement_records": """CREATE TABLE statement_records (
        id TEXT PRIMARY KEY, statement_id TEXT NOT NULL REFERENCES statements(id),
        fingerprint TEXT NOT NULL, occurrence INTEGER NOT NULL, kind TEXT NOT NULL,
        source_location TEXT NOT NULL, source_quote TEXT NOT NULL, transaction_date TEXT,
        posting_date TEXT, amount_text TEXT, amount_minor INTEGER, currency TEXT,
        description TEXT, bank_reference TEXT, reliable_reference INTEGER NOT NULL,
        card_id TEXT, status TEXT, balance_date TEXT, balance_type TEXT,
        transaction_id TEXT, accepted INTEGER NOT NULL DEFAULT 1,
        superseded INTEGER NOT NULL DEFAULT 0)""",
    "transactions": """CREATE TABLE transactions (
        id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id), card_id TEXT,
        transaction_date TEXT, posting_date TEXT, amount INTEGER NOT NULL, currency TEXT NOT NULL,
        description TEXT, bank_reference TEXT, reliable_reference INTEGER NOT NULL,
        status TEXT NOT NULL, supporting_record TEXT NOT NULL REFERENCES statement_records(id),
        active INTEGER NOT NULL DEFAULT 1, user_comment TEXT,
        vendor TEXT, category TEXT, vendor_state TEXT NOT NULL DEFAULT 'unknown',
        category_state TEXT NOT NULL DEFAULT 'unknown', user_tags TEXT NOT NULL DEFAULT '[]',
        tag_source_url TEXT, tag_source_title TEXT, tag_lookup_date TEXT,
        tag_uncertainty TEXT, tag_reason TEXT, tag_source_kind TEXT,
        tagging_rule_id TEXT REFERENCES tagging_rules(id) ON DELETE SET NULL)""",
    "tagging_rules": """CREATE TABLE tagging_rules (
        id TEXT PRIMARY KEY, account_id TEXT REFERENCES accounts(id), currency TEXT NOT NULL,
        exact_match TEXT NOT NULL, vendor TEXT NOT NULL, category TEXT,
        user_tags TEXT NOT NULL, evidence TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""",
}
_TABLE_ORDER = tuple(_CREATE_TABLES)
_TABLES = {
    "accounts": {
        "columns": ("id", "alias", "bank", "type", "identity_evidence", "currency", "precision"),
        "required": ("alias", "identity_evidence", "currency", "precision"),
        "integer": ("precision",), "nullable": ("bank", "type"),
    },
    "files": {
        "columns": ("id", "content_hash", "size", "format", "original_name", "managed_path", "copy_state"),
        "required": ("content_hash", "size", "format", "original_name", "managed_path", "copy_state"),
        "integer": ("size",), "nullable": (),
    },
    "statements": {
        "columns": ("id", "file_id", "section", "account_id", "scope", "card_id", "start", "end",
                    "start_evidence", "end_evidence", "date_basis", "reader", "outcome", "questions"),
        "required": ("file_id", "section", "account_id", "scope", "reader", "outcome", "questions"),
        "integer": (), "nullable": ("card_id", "start", "end", "start_evidence", "end_evidence", "date_basis"),
    },
    "statement_records": {
        "columns": ("id", "statement_id", "fingerprint", "occurrence", "kind", "source_location", "source_quote",
                    "transaction_date", "posting_date", "amount_text", "amount_minor", "currency", "description",
                    "bank_reference", "reliable_reference", "card_id", "status", "balance_date", "balance_type",
                    "transaction_id", "accepted", "superseded"),
        "required": ("statement_id", "fingerprint", "occurrence", "kind", "source_location", "source_quote",
                     "reliable_reference"),
        "integer": ("occurrence", "amount_minor", "reliable_reference", "accepted", "superseded"),
        "nullable": ("transaction_date", "posting_date", "amount_text", "amount_minor", "currency", "description",
                     "bank_reference", "card_id", "status", "balance_date", "balance_type", "transaction_id"),
        "defaults": ("accepted", "superseded"),
    },
    "transactions": {
        "columns": ("id", "account_id", "card_id", "transaction_date", "posting_date", "amount", "currency",
                    "description", "bank_reference", "reliable_reference", "status", "supporting_record",
                    "active", "user_comment", "vendor", "category", "vendor_state", "category_state",
                    "user_tags", "tag_source_url", "tag_source_title", "tag_lookup_date", "tag_uncertainty",
                    "tag_reason", "tag_source_kind", "tagging_rule_id"),
        "required": ("account_id", "amount", "currency", "reliable_reference", "status", "supporting_record"),
        "integer": ("amount", "reliable_reference", "active"),
        "nullable": ("card_id", "transaction_date", "posting_date", "description", "bank_reference", "user_comment",
                     "vendor", "category", "tag_source_url", "tag_source_title", "tag_lookup_date",
                     "tag_uncertainty", "tag_reason", "tag_source_kind", "tagging_rule_id"),
        "defaults": ("active", "vendor_state", "category_state", "user_tags"),
    },
    "tagging_rules": {
        "columns": ("id", "account_id", "currency", "exact_match", "vendor", "category", "user_tags",
                    "evidence", "active", "created_at", "updated_at"),
        "required": ("currency", "exact_match", "vendor", "user_tags", "evidence", "created_at", "updated_at"),
        "integer": ("active",),
        "nullable": ("account_id", "category"),
        "defaults": ("active",),
    },
}
_TAG_FIELDS = frozenset({
    "vendor", "category", "vendor_state", "category_state", "user_tags", "tag_source_url",
    "tag_source_title", "tag_lookup_date", "tag_uncertainty", "tag_reason", "tag_source_kind", "tagging_rule_id",
})
_ADDED_TRANSACTION_COLUMNS = {
    "user_comment": "TEXT", "vendor": "TEXT", "category": "TEXT",
    "vendor_state": "TEXT NOT NULL DEFAULT 'unknown'",
    "category_state": "TEXT NOT NULL DEFAULT 'unknown'",
    "user_tags": "TEXT NOT NULL DEFAULT '[]'", "tag_source_url": "TEXT",
    "tag_source_title": "TEXT", "tag_lookup_date": "TEXT", "tag_uncertainty": "TEXT", "tag_reason": "TEXT",
    "tag_source_kind": "TEXT",
    "tagging_rule_id": "TEXT REFERENCES tagging_rules(id) ON DELETE SET NULL",
}


def _settings_path() -> Path:
    config_root = os.environ.get("XDG_CONFIG_HOME")
    if config_root:
        return Path(config_root) / "financial-history" / "settings.json"
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if not local_app_data:
            raise HistoryError("LOCALAPPDATA is not set; cannot find financial-history settings.")
        return Path(local_app_data) / "financial-history" / "settings.json"
    return Path.home() / ".config" / "financial-history" / "settings.json"


def _read_settings() -> dict[str, object]:
    path = _settings_path()
    try:
        if not path.exists():
            return {}
        settings = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HistoryError("Could not read the financial-history settings file.") from error
    if not isinstance(settings, dict):
        raise HistoryError("The financial-history settings file must contain a JSON object.")
    return settings


def _write_settings(settings: Mapping[str, object]) -> None:
    path = _settings_path()
    temporary_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", delete=False) as file:
            temporary_path = Path(file.name)
            json.dump(settings, file, ensure_ascii=False, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError) as error:
        raise HistoryError("Could not save the financial-history settings file.") from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _resolve_history(history_directory: Path | None = None) -> Path:
    if history_directory is None:
        saved = _read_settings().get("history_directory")
        if not isinstance(saved, str) or not saved:
            raise HistoryError("Choose or create a financial history before using database functions.")
        history_directory = Path(saved)
    try:
        return Path(history_directory).expanduser().resolve()
    except (OSError, RuntimeError, ValueError) as error:
        raise HistoryError("The selected history path is invalid.") from error


def _database_path(history_directory: Path) -> Path:
    return Path(history_directory) / "history.sqlite3"


def _connect_history(history_directory: Path, *, read_only: bool = False) -> sqlite3.Connection:
    database = _database_path(history_directory).resolve()
    if not database.is_file():
        raise HistoryError("The selected history database does not exist. Link or create a history first.")
    try:
        mode = "ro" if read_only else "rw"
        connection = sqlite3.connect(f"{database.as_uri()}?mode={mode}", uri=True)
        connection.row_factory = sqlite3.Row
        if not read_only:
            connection.execute("PRAGMA foreign_keys=ON")
        return connection
    except sqlite3.Error as error:
        raise HistoryError("Could not open the selected history database.") from error


def _create_missing_tables(connection: sqlite3.Connection, tables: Sequence[str]) -> None:
    for table in _TABLE_ORDER:
        if table in tables:
            connection.execute(_CREATE_TABLES[table])


def _ensure_history_schema(
    history_directory: Path, *, create_missing: bool | None = False
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    database = _database_path(history_directory).resolve()
    if not database.is_file():
        raise HistoryError("The selected history database does not exist.")
    try:
        with closing(_connect_history(history_directory)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = {row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            missing = tuple(table for table in _TABLE_ORDER if table not in existing)
            missing_columns: list[str] = []
            for table in _TABLE_ORDER:
                if table in existing:
                    columns = {row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')}
                    missing_columns.extend(f"{table}.{name}" for name in _TABLES[table]["columns"]
                                           if name not in columns)
            allowed_missing = {f"transactions.{name}" for name in _ADDED_TRANSACTION_COLUMNS}
            if set(missing_columns) - allowed_missing:
                raise HistoryError("A history table is not compatible with this financial history.")
            needs_choice = bool(missing or missing_columns)
            if needs_choice and create_missing is not True:
                if create_missing is None or create_missing is False:
                    return missing, tuple(missing_columns)
            if missing or missing_columns:
                _create_missing_tables(connection, missing)
                for column in missing_columns:
                    name = column.split(".", 1)[1]
                    connection.execute(f'ALTER TABLE transactions ADD COLUMN "{name}" {_ADDED_TRANSACTION_COLUMNS[name]}')

            for table in _TABLE_ORDER:
                if table not in existing and table not in missing:
                    continue
                info = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
                columns = {row[1] for row in info}
                expected = set(_TABLES[table]["columns"])
                absent = expected - columns
                if absent:
                    raise HistoryError(f"The {table} table is not compatible with this financial history.")
                types = {row[1]: str(row[2]).upper() for row in info}
                integer_fields = set(_TABLES[table]["integer"])
                if any(types[name] != ("INTEGER" if name in integer_fields else "TEXT") for name in expected):
                    raise HistoryError(f"The {table} table has incompatible field types.")
                nullable = set(_TABLES[table]["nullable"])
                if any(bool(row[3]) != (row[1] not in nullable and row[1] != "id")
                       for row in info if row[1] in expected and row[1] != "id"):
                    raise HistoryError(f"The {table} table has incompatible required fields.")
            if needs_choice and create_missing is True:
                if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                    raise HistoryError("The history contains invalid links. No schema changes were saved.")
                if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise HistoryError("The history integrity check failed. No schema changes were saved.")
            return (), ()
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not check or prepare the history database.") from error


def _ready_result(history: Path, message: str = "History is ready.") -> SetupResult:
    return SetupResult("ready", str(history.resolve()), (), message)


def create_history(history: Path) -> SetupResult:
    """Create a new history database without changing saved settings."""
    history = _resolve_history(history)
    database = _database_path(history)
    if database.exists():
        raise HistoryError("A history database already exists in this folder. Use link_history instead.")
    try:
        history.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(database)) as connection, connection:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("BEGIN IMMEDIATE")
            _create_missing_tables(connection, _TABLE_ORDER)
    except (OSError, sqlite3.Error) as error:
        raise HistoryError("Could not create the financial-history database.") from error
    return _ready_result(history, "Created a new financial-history database.")


def link_history(history: Path, *, create_missing: bool | None = None) -> SetupResult:
    """Check an existing history and add missing schema parts only when chosen."""
    if create_missing is not None and not isinstance(create_missing, bool):
        raise HistoryError("create_missing must be True, False, or None.")
    history = _resolve_history(history)
    missing, missing_columns = _ensure_history_schema(history, create_missing=create_missing)
    if (missing or missing_columns) and create_missing is None:
        return SetupResult("needs_choice", str(history), missing,
                           "Some required tables or fields are missing. Choose to add them or use another database.",
                           missing_columns)
    if (missing or missing_columns) and create_missing is False:
        return SetupResult("use_another_database", str(history), missing,
                           "Use another database. No tables or fields were changed.", missing_columns)
    return _ready_result(history, "Linked to the existing financial-history database.")


def update_history_config(history_directory: Path) -> SetupResult:
    """Select a ready history in settings while preserving other values."""
    history = _resolve_history(history_directory)
    missing, missing_columns = _ensure_history_schema(history)
    if missing or missing_columns:
        raise HistoryError("The selected history is missing required tables or fields. Link it and choose whether to add them.")
    settings = _read_settings()
    settings["history_directory"] = str(history)
    _write_settings(settings)
    return _ready_result(history, "Saved the selected financial-history directory.")


def _prepare_selected_history(history_directory: Path | None = None) -> Path:
    history = _resolve_history(history_directory)
    missing, missing_columns = _ensure_history_schema(history)
    if missing or missing_columns:
        raise HistoryError("The selected history is missing required tables or fields. Use link_history to choose what to do.")
    return history


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
        if value.endswith(("-", "−")):
            if value.startswith(("+", "-", "−", "(")):
                raise HistoryError("The amount contains conflicting signs.")
            value = "-" + value[:-1].strip()
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
        value = re.sub(r"^([+-]?)\$", r"\1", value.replace("−", "-"))
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


def _table_name(table: str) -> str:
    if table not in _TABLES:
        raise HistoryError("Unknown financial-history table.")
    return table


def _validate_fields(table: str, fields: Mapping[str, object], *, partial: bool = False) -> dict[str, object]:
    table = _table_name(table)
    if not isinstance(fields, Mapping) or not fields:
        raise HistoryError("Supply one or more fields as a mapping.")
    if any(not isinstance(name, str) for name in fields):
        raise HistoryError("Field names must be text.")
    allowed = set(_TABLES[table]["columns"])
    if partial:
        allowed.discard("id")
        if table == "transactions":
            allowed.discard("supporting_record")
    unknown = set(fields) - allowed
    if unknown:
        raise HistoryError(f"Unknown or protected field for {table}.")
    if table == "transactions" and set(fields) & _TAG_FIELDS:
        raise HistoryError("Use the tagging functions to change transaction tags.")
    if not partial:
        missing = set(_TABLES[table]["required"]) - set(fields)
        if missing:
            raise HistoryError(f"Missing required fields for {table}: {', '.join(sorted(missing))}.")
    integer_fields = set(_TABLES[table]["integer"])
    nullable_fields = set(_TABLES[table]["nullable"])
    for name, value in fields.items():
        if value is None:
            if name not in nullable_fields:
                raise HistoryError(f"Field {name} cannot be empty.")
        elif name in integer_fields:
            if not isinstance(value, int) or isinstance(value, bool):
                raise HistoryError(f"Field {name} must be an integer.")
        elif not isinstance(value, str):
            raise HistoryError(f"Field {name} must be text.")
        elif name in _TABLES[table]["required"] and not value.strip():
            raise HistoryError(f"Field {name} cannot be empty.")
    if table == "accounts" and fields.get("precision", 0) < 0:
        raise HistoryError("Account precision cannot be negative.")
    if table == "files" and fields.get("size", 0) < 0:
        raise HistoryError("File size cannot be negative.")
    if table == "statement_records":
        if fields.get("occurrence", 1) < 1:
            raise HistoryError("Record occurrence must be positive.")
        for flag in ("reliable_reference", "accepted", "superseded"):
            if flag in fields and fields[flag] not in (0, 1):
                raise HistoryError(f"Field {flag} must be 0 or 1.")
    if table == "transactions":
        for flag in ("reliable_reference", "active"):
            if flag in fields and fields[flag] not in (0, 1):
                raise HistoryError(f"Field {flag} must be 0 or 1.")
    if table == "tagging_rules" and "active" in fields and fields["active"] not in (0, 1):
        raise HistoryError("Field active must be 0 or 1.")
    if "user_tags" in fields:
        try:
            tags = json.loads(str(fields["user_tags"]))
        except (TypeError, json.JSONDecodeError) as error:
            raise HistoryError("User tags must be a JSON list of text values.") from error
        if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
            raise HistoryError("User tags must be a JSON list of text values.")
    if not partial and "id" in fields and (not isinstance(fields["id"], str) or not fields["id"]):
        raise HistoryError("Field id must be non-empty text.")
    return dict(fields)


def _validate_row_links(connection: sqlite3.Connection, table: str, values: Mapping[str, object]) -> None:
    if table == "accounts":
        currency = values.get("currency")
        precision = values.get("precision")
        if "currency" in values or "precision" in values:
            rows = connection.execute(
                "SELECT r.currency, r.amount_minor FROM statements s "
                "JOIN statement_records r ON r.statement_id=s.id WHERE s.account_id=?",
                (values["id"],),
            ).fetchall()
            if "currency" in values and any(row["currency"] not in (None, currency) for row in rows):
                raise HistoryError("The account currency conflicts with linked source records.")
            transactions = connection.execute(
                "SELECT currency FROM transactions WHERE account_id=?", (values["id"],)
            ).fetchall()
            if "currency" in values and any(row["currency"] != currency for row in transactions):
                raise HistoryError("The account currency conflicts with linked transactions.")
            if "precision" in values and any(row["amount_minor"] is not None for row in rows):
                old = connection.execute("SELECT precision FROM accounts WHERE id=?", (values["id"],)).fetchone()
                if old and old["precision"] != precision:
                    raise HistoryError("Cannot change precision while saved amounts use this account.")
            if "precision" in values and transactions:
                old = connection.execute("SELECT precision FROM accounts WHERE id=?", (values["id"],)).fetchone()
                if old and old["precision"] != precision:
                    raise HistoryError("Cannot change precision while saved amounts use this account.")
    elif table == "statements":
        if values.get("start") and values.get("end"):
            try:
                start = datetime.strptime(str(values["start"]), "%Y-%m-%d")
                end = datetime.strptime(str(values["end"]), "%Y-%m-%d")
            except ValueError as error:
                raise HistoryError("Statement dates must use YYYY-MM-DD.") from error
            if start > end:
                raise HistoryError("Statement start date must not follow its end date.")
        account = connection.execute("SELECT currency FROM accounts WHERE id=?", (values["account_id"],)).fetchone()
        if account:
            records = connection.execute(
                "SELECT r.currency,t.account_id AS transaction_account FROM statement_records r "
                "LEFT JOIN transactions t ON t.supporting_record=r.id WHERE r.statement_id=?", (values["id"],)
            ).fetchall()
            if any(row["currency"] not in (None, account["currency"]) or
                   row["transaction_account"] not in (None, values["account_id"]) for row in records):
                raise HistoryError("The statement account currency conflicts with its source records.")
    elif table == "statement_records":
        statement = connection.execute(
            "SELECT account_id FROM statements WHERE id=?", (values["statement_id"],)
        ).fetchone()
        if statement and values.get("currency") is not None:
            account = connection.execute("SELECT currency FROM accounts WHERE id=?", (statement["account_id"],)).fetchone()
            if account and values["currency"] != account["currency"]:
                raise HistoryError("Source-record currency differs from the account currency.")
        for field in ("transaction_date", "posting_date", "balance_date"):
            if values.get(field):
                try:
                    datetime.strptime(str(values[field]), "%Y-%m-%d")
                except ValueError as error:
                    raise HistoryError(f"{field} must use YYYY-MM-DD.") from error
        transaction = connection.execute(
            "SELECT currency,account_id FROM transactions WHERE supporting_record=?", (values["id"],)
        ).fetchone()
        if transaction and transaction["currency"] != values.get("currency"):
            raise HistoryError("Source-record currency differs from its linked transaction.")
        if transaction and statement and transaction["account_id"] != statement["account_id"]:
            raise HistoryError("Source record and transaction must belong to the same account.")
        transaction_id = values.get("transaction_id")
        if transaction_id is not None:
            linked = connection.execute(
                "SELECT supporting_record FROM transactions WHERE id=?", (transaction_id,)
            ).fetchone()
            if not linked or linked["supporting_record"] != values["id"]:
                raise HistoryError("The transaction link does not match this source record.")
    elif table == "transactions":
        for field in ("transaction_date", "posting_date"):
            if values.get(field):
                try:
                    datetime.strptime(str(values[field]), "%Y-%m-%d")
                except ValueError as error:
                    raise HistoryError(f"{field} must use YYYY-MM-DD.") from error
        account = connection.execute("SELECT currency FROM accounts WHERE id=?", (values["account_id"],)).fetchone()
        if account and values.get("currency") != account["currency"]:
            raise HistoryError("Transaction currency differs from the account currency.")
        record = connection.execute(
            "SELECT r.kind,r.currency,r.transaction_id,s.account_id FROM statement_records r "
            "JOIN statements s ON s.id=r.statement_id WHERE r.id=?", (values["supporting_record"],)
        ).fetchone()
        if record:
            if record["kind"] != "transaction" or record["account_id"] != values["account_id"]:
                raise HistoryError("The source record does not belong to this transaction account.")
            if record["currency"] not in (None, values.get("currency")):
                raise HistoryError("Transaction currency differs from its source record.")
            if record["transaction_id"] not in (None, values["id"]):
                raise HistoryError("The source record already links to another transaction.")
    elif table == "tagging_rules" and values.get("account_id") is not None:
        account = connection.execute("SELECT currency FROM accounts WHERE id=?", (values["account_id"],)).fetchone()
        if account is None:
            raise HistoryError("The tagging rule account does not exist.")
        if account["currency"] != values.get("currency"):
            raise HistoryError("The tagging rule currency differs from its account.")


def _insert_row(connection: sqlite3.Connection, table: str, fields: Mapping[str, object]) -> dict[str, object]:
    table = _table_name(table)
    values = dict(fields)
    values.setdefault("id", _id())
    values = _validate_fields(table, values)
    _validate_row_links(connection, table, values)
    columns = tuple(values)
    names = ", ".join(f'"{name}"' for name in columns)
    placeholders = ", ".join("?" for _ in columns)
    connection.execute(f'INSERT INTO "{table}" ({names}) VALUES ({placeholders})', tuple(values.values()))
    if table == "transactions":
        connection.execute("UPDATE statement_records SET transaction_id=? WHERE id=?",
                           (values["id"], values["supporting_record"]))
    row = connection.execute(f'SELECT * FROM "{table}" WHERE id=?', (values["id"],)).fetchone()
    return dict(row)


def _update_row_on_connection(connection: sqlite3.Connection, table: str, row_id: str,
                              changes: Mapping[str, object]) -> dict[str, object]:
    table = _table_name(table)
    updates = _validate_fields(table, changes, partial=True)
    if table == "transactions":
        updates.setdefault("user_comment", "Changed by user")
    current = connection.execute(f'SELECT * FROM "{table}" WHERE id=?', (row_id,)).fetchone()
    if current is None:
        raise HistoryError("The requested row does not exist.")
    values = dict(current)
    values.update(updates)
    _validate_row_links(connection, table, values)
    assignments = ", ".join(f'"{name}"=?' for name in updates)
    connection.execute(f'UPDATE "{table}" SET {assignments} WHERE id=?', (*updates.values(), row_id))
    return dict(connection.execute(f'SELECT * FROM "{table}" WHERE id=?', (row_id,)).fetchone())


def _create_row(table: str, fields: Mapping[str, object], history_directory: Path | None) -> str:
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            row = _insert_row(connection, table, fields)
            return str(row["id"])
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not create the row. Check its values and linked rows.") from error


def _read_authorizer(table: str):
    def authorize(action: int, first: str | None, second: str | None,
                  database: str | None, source: str | None) -> int:
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK if source is None else sqlite3.SQLITE_DENY
        if action == sqlite3.SQLITE_READ:
            allowed = database == "main" and first == table
            return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY
        if action == sqlite3.SQLITE_FUNCTION:
            function = (second or first or "").casefold()
            return sqlite3.SQLITE_DENY if function == "load_extension" else sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    return authorize


_SUMMARY_RE = re.compile(
    r"(?i)^(COUNT\s*\(\s*\*\s*\)|COUNT\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\)|"
    r"SUM\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\)|AVG\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\)|"
    r"MIN\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\)|MAX\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\))"
    r"(?:\s+AS\s+([A-Za-z_][A-Za-z0-9_]*))?$"
)
_COLUMN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(?:\s+AS\s+([A-Za-z_][A-Za-z0-9_]*))?$", re.I)


def _validate_selected_columns(table: str, selected_columns: Sequence[str] | None,
                              group_by: Sequence[str] | None) -> tuple[tuple[str, ...], tuple[str, ...]]:
    table = _table_name(table)
    columns = _TABLES[table]["columns"]
    if selected_columns is None:
        if group_by:
            raise HistoryError("Supply selected_columns when you use group_by.")
        return ("*",), ()
    if not isinstance(selected_columns, Sequence) or isinstance(selected_columns, (str, bytes)) or not selected_columns:
        raise HistoryError("Supply selected_columns as a non-empty list of fields or summaries.")
    if group_by is not None and (not isinstance(group_by, Sequence) or isinstance(group_by, (str, bytes))):
        raise HistoryError("Supply group_by as a list of fields.")
    groups = tuple(group_by or ())
    if any(not isinstance(name, str) for name in groups) or len(set(groups)) != len(groups):
        raise HistoryError("Supply each group_by field once.")
    if any(name not in columns for name in groups):
        raise HistoryError("A group_by field is not in the selected table.")

    expressions: list[str] = []
    raw_fields: list[str] = []
    aliases: set[str] = set()
    has_summary = False
    for selected in selected_columns:
        if not isinstance(selected, str):
            raise HistoryError("Each selected column must be text.")
        summary = _SUMMARY_RE.fullmatch(selected.strip())
        raw = _COLUMN_RE.fullmatch(selected.strip())
        if summary:
            has_summary = True
            expression = re.sub(r"\s+AS\s+", " AS ", selected.strip(), flags=re.I)
            function, argument = re.match(r"(?i)(COUNT|SUM|AVG|MIN|MAX)\s*\(\s*(\*|[A-Za-z_][A-Za-z0-9_]*)", expression).groups()
            if argument != "*" and argument not in columns:
                raise HistoryError("A summary field is not in the selected table.")
            if function.upper() in {"SUM", "AVG"} and argument not in _TABLES[table]["integer"]:
                raise HistoryError("SUM and AVG require an integer amount or count field.")
            if table == "transactions" and argument == "amount" or table == "statement_records" and argument == "amount_minor":
                if function.upper() in {"SUM", "AVG", "MIN", "MAX"} and "currency" not in groups:
                    raise HistoryError("Group money summaries by currency.")
            alias = summary.group(2)
            sql_expression = expression
            if alias:
                sql_expression = expression[:expression.upper().rfind(" AS ")] + f' AS "{alias}"'
            else:
                sql_expression = expression[:expression.upper().rfind(" AS ")] if " AS " in expression.upper() else expression
            expressions.append(sql_expression)
            key = (alias or expression.split(" AS ")[0]).casefold()
        elif raw:
            name, alias = raw.groups()
            if name not in columns:
                raise HistoryError("A selected field is not in the selected table.")
            raw_fields.append(name)
            expressions.append(f'"{name}"' + (f' AS "{alias}"' if alias else ""))
            key = (alias or name).casefold()
        else:
            raise HistoryError("Use a table field or an allowed summary expression in selected_columns.")
        if key in aliases:
            raise HistoryError("Selected columns must have unique result names.")
        aliases.add(key)

    if groups:
        if any(field not in raw_fields for field in groups) or any(field not in groups for field in raw_fields):
            raise HistoryError("Select every group_by field and group every selected raw field.")
    elif has_summary and raw_fields:
        raise HistoryError("Group selected raw fields when you also use summaries.")
    return tuple(expressions), groups


def _read_table_rows(table: str, where_clause: str | None, parameters: Sequence[object],
                     selected_columns: Sequence[str] | None, group_by: Sequence[str] | None,
                     history_directory: Path | None) -> list[dict[str, object]]:
    table = _table_name(table)
    expressions, groups = _validate_selected_columns(table, selected_columns, group_by)
    if where_clause is not None and not isinstance(where_clause, str):
        raise HistoryError("where_clause must be text.")
    clause = where_clause.strip() if where_clause else ""
    if not isinstance(parameters, Sequence) or isinstance(parameters, (str, bytes)):
        raise HistoryError("Pass Read filter values as a sequence.")
    if not clause and parameters:
        raise HistoryError("Pass filter values only when where_clause has placeholders.")
    if re.search(r";|--|/\*|\*/", clause) or re.search(
        r"\b(SELECT|UNION|WITH|ATTACH|DETACH|PRAGMA|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|REPLACE|VACUUM|"
        r"GROUP|ORDER|LIMIT|OFFSET|HAVING|WINDOW|RETURNING|EXCEPT|INTERSECT)\b",
        clause, re.I,
    ):
        raise HistoryError("Use only a filter expression after WHERE; full SQL is not allowed.")
    history = _prepare_selected_history(history_directory)
    sql = f'SELECT {", ".join(expressions)} FROM "{table}"'
    if clause:
        sql += f" WHERE {clause}"
    if groups:
        sql += " GROUP BY " + ", ".join(f'"{field}"' for field in groups)
        sql += " ORDER BY " + ", ".join(f'"{field}"' for field in groups)
    try:
        with closing(_connect_history(history, read_only=True)) as connection:
            connection.set_authorizer(_read_authorizer(table))
            return [dict(row) for row in connection.execute(sql, tuple(parameters)).fetchall()]
    except sqlite3.Error as error:
        raise HistoryError("Read failed. Check the filter and selected fields.") from error


def _update_row(table: str, row_id: str, changes: Mapping[str, object],
                history_directory: Path | None) -> dict[str, object]:
    table = _table_name(table)
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            return _update_row_on_connection(connection, table, row_id, changes)
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not update the row. Check its values and linked rows.") from error


def _delete_linked_rows(
    connection: sqlite3.Connection, table: str, row_id: str,
    shared_rule_choices: Mapping[str, str] | None = None,
) -> DeleteResult:
    table = _table_name(table)
    if connection.execute(f'SELECT 1 FROM "{table}" WHERE id=?', (row_id,)).fetchone() is None:
        return DeleteResult(False, table, row_id, {})
    deleted: dict[str, set[str]] = {name: set() for name in _TABLE_ORDER}
    deleted[table].add(row_id)
    if table == "accounts":
        account = connection.execute("SELECT currency FROM accounts WHERE id=?", (row_id,)).fetchone()
        shared_rules = {row[0] for row in connection.execute(
            "SELECT id FROM tagging_rules WHERE account_id IS NULL AND currency=? AND active=1",
            (account["currency"],),
        )}
        if shared_rule_choices is not None and not isinstance(shared_rule_choices, Mapping):
            raise HistoryError("shared_rule_choices must map rule IDs to keep or remove.")
        choices = dict(shared_rule_choices or {})
        if set(choices) != shared_rules or any(
            not isinstance(choice, str) or choice not in {"keep", "remove"} for choice in choices.values()
        ):
            raise HistoryError("Review every active same-currency shared rule and choose keep or remove.")
        account_rules = {row[0] for row in connection.execute(
            "SELECT id FROM tagging_rules WHERE account_id=?", (row_id,))}
        for rule_id in account_rules:
            connection.execute("DELETE FROM tagging_rules WHERE id=?", (rule_id,))
        deleted["tagging_rules"].update(account_rules)
        for rule_id, choice in choices.items():
            if choice == "remove":
                connection.execute("DELETE FROM tagging_rules WHERE id=?", (rule_id,))
                deleted["tagging_rules"].add(rule_id)
        deleted["statements"].update(row[0] for row in connection.execute(
            "SELECT id FROM statements WHERE account_id=?", (row_id,)))
        deleted["transactions"].update(row[0] for row in connection.execute(
            "SELECT id FROM transactions WHERE account_id=?", (row_id,)))
    elif table == "files":
        deleted["statements"].update(row[0] for row in connection.execute(
            "SELECT id FROM statements WHERE file_id=?", (row_id,)))
    if table in {"accounts", "files", "statements"} and deleted["statements"]:
        ids = deleted["statements"]
        marks = ",".join("?" for _ in ids)
        deleted["statement_records"].update(row[0] for row in connection.execute(
            f"SELECT id FROM statement_records WHERE statement_id IN ({marks})", tuple(ids)))
    if table in {"accounts", "files", "statements", "statement_records"}:
        records = deleted["statement_records"]
        if table == "statement_records":
            records.add(row_id)
        if records:
            marks = ",".join("?" for _ in records)
            deleted["transactions"].update(row[0] for row in connection.execute(
                f"SELECT id FROM transactions WHERE supporting_record IN ({marks})", tuple(records)))
            deleted["transactions"].update(row[0] for row in connection.execute(
                f"SELECT transaction_id FROM statement_records WHERE id IN ({marks}) "
                "AND transaction_id IS NOT NULL", tuple(records)))
    if table == "transactions":
        deleted["transactions"].add(row_id)

    transaction_ids = deleted["transactions"]
    record_ids = deleted["statement_records"]
    if transaction_ids:
        marks = ",".join("?" for _ in transaction_ids)
        connection.execute(f"UPDATE statement_records SET transaction_id=NULL WHERE transaction_id IN ({marks})",
                           tuple(transaction_ids))
        connection.execute(f"DELETE FROM transactions WHERE id IN ({marks})", tuple(transaction_ids))
    if record_ids:
        marks = ",".join("?" for _ in record_ids)
        connection.execute(f"DELETE FROM statement_records WHERE id IN ({marks})", tuple(record_ids))
    if deleted["statements"]:
        ids = deleted["statements"]
        marks = ",".join("?" for _ in ids)
        connection.execute(f"DELETE FROM statements WHERE id IN ({marks})", tuple(ids))
    if table in {"accounts", "files"}:
        connection.execute(f'DELETE FROM "{table}" WHERE id=?', (row_id,))
    return DeleteResult(True, table, row_id,
                        {name: tuple(sorted(ids)) for name, ids in deleted.items() if ids})


def _delete_row(
    table: str, row_id: str, history_directory: Path | None,
    shared_rule_choices: Mapping[str, str] | None = None,
) -> DeleteResult:
    table = _table_name(table)
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            return _delete_linked_rows(connection, table, row_id, shared_rule_choices)
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not delete the row and its linked child rows.") from error


def create_account(fields: Mapping[str, object], history_directory: Path | None = None) -> str:
    return _create_row("accounts", fields, history_directory)


def create_file(fields: Mapping[str, object], history_directory: Path | None = None) -> str:
    return _create_row("files", fields, history_directory)


def create_statement(fields: Mapping[str, object], history_directory: Path | None = None) -> str:
    return _create_row("statements", fields, history_directory)


def create_statement_record(fields: Mapping[str, object], history_directory: Path | None = None) -> str:
    return _create_row("statement_records", fields, history_directory)


def create_transaction(fields: Mapping[str, object], history_directory: Path | None = None) -> str:
    return _create_row("transactions", fields, history_directory)


def read_account(where_clause: str | None = None, parameters: Sequence[object] = (),
                 selected_columns: Sequence[str] | None = None, group_by: Sequence[str] | None = None,
                 history_directory: Path | None = None) -> list[dict[str, object]]:
    return _read_table_rows("accounts", where_clause, parameters, selected_columns, group_by, history_directory)


def read_file(where_clause: str | None = None, parameters: Sequence[object] = (),
              selected_columns: Sequence[str] | None = None, group_by: Sequence[str] | None = None,
              history_directory: Path | None = None) -> list[dict[str, object]]:
    return _read_table_rows("files", where_clause, parameters, selected_columns, group_by, history_directory)


def read_statement(where_clause: str | None = None, parameters: Sequence[object] = (),
                   selected_columns: Sequence[str] | None = None, group_by: Sequence[str] | None = None,
                   history_directory: Path | None = None) -> list[dict[str, object]]:
    return _read_table_rows("statements", where_clause, parameters, selected_columns, group_by, history_directory)


def read_statement_record(where_clause: str | None = None, parameters: Sequence[object] = (),
                          selected_columns: Sequence[str] | None = None, group_by: Sequence[str] | None = None,
                          history_directory: Path | None = None) -> list[dict[str, object]]:
    return _read_table_rows("statement_records", where_clause, parameters, selected_columns, group_by, history_directory)


def read_transaction(where_clause: str | None = None, parameters: Sequence[object] = (),
                     selected_columns: Sequence[str] | None = None, group_by: Sequence[str] | None = None,
                     history_directory: Path | None = None) -> list[dict[str, object]]:
    return _read_table_rows("transactions", where_clause, parameters, selected_columns, group_by, history_directory)


def update_account(row_id: str, changes: Mapping[str, object], history_directory: Path | None = None) -> dict[str, object]:
    return _update_row("accounts", row_id, changes, history_directory)


def update_file(row_id: str, changes: Mapping[str, object], history_directory: Path | None = None) -> dict[str, object]:
    return _update_row("files", row_id, changes, history_directory)


def update_statement(row_id: str, changes: Mapping[str, object], history_directory: Path | None = None) -> dict[str, object]:
    return _update_row("statements", row_id, changes, history_directory)


def update_statement_record(row_id: str, changes: Mapping[str, object], history_directory: Path | None = None) -> dict[str, object]:
    return _update_row("statement_records", row_id, changes, history_directory)


def update_transaction(row_id: str, changes: Mapping[str, object], history_directory: Path | None = None) -> dict[str, object]:
    return _update_row("transactions", row_id, changes, history_directory)


def delete_account(
    row_id: str, history_directory: Path | None = None,
    shared_rule_choices: Mapping[str, str] | None = None,
) -> DeleteResult:
    return _delete_row("accounts", row_id, history_directory, shared_rule_choices)


def delete_file(row_id: str, history_directory: Path | None = None) -> DeleteResult:
    return _delete_row("files", row_id, history_directory)


def delete_statement(row_id: str, history_directory: Path | None = None) -> DeleteResult:
    return _delete_row("statements", row_id, history_directory)


def delete_statement_record(row_id: str, history_directory: Path | None = None) -> DeleteResult:
    return _delete_row("statement_records", row_id, history_directory)


def delete_transaction(row_id: str, history_directory: Path | None = None) -> DeleteResult:
    return _delete_row("transactions", row_id, history_directory)


def _normalise_match(value: str) -> str:
    return " ".join(value.casefold().split())


def _tag_list(values: Sequence[str] | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise HistoryError("user_tags must be a list of text values.")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise HistoryError("Each user tag must be non-empty text.")
    return list(dict.fromkeys(value.strip() for value in values))


def _tag_date(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except (TypeError, ValueError) as error:
        raise HistoryError("Tag dates must use YYYY-MM-DD.") from error


def read_tagging_data(
    account_id: str | None = None,
    transaction_id: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    after_transaction_id: str | None = None,
    limit: int = 100,
    history_directory: Path | None = None,
) -> dict[str, object]:
    """Read a bounded page of active transactions and rules for their account/currency scope."""
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise HistoryError("limit must be an integer from 1 to 100.")
    if account_id is not None and (not isinstance(account_id, str) or not account_id):
        raise HistoryError("account_id must be a non-empty account ID.")
    if transaction_id is not None and (not isinstance(transaction_id, str) or not transaction_id):
        raise HistoryError("transaction_id must be a non-empty transaction ID.")
    if transaction_id is not None and after_transaction_id is not None:
        raise HistoryError("Use transaction_id or after_transaction_id, not both.")
    start_date = _tag_date(start_date)
    end_date = _tag_date(end_date)
    if start_date and end_date and start_date > end_date:
        raise HistoryError("start_date must not follow end_date.")
    filters = ["active=1"]
    parameters: list[object] = []
    if account_id is not None:
        filters.append("account_id=?")
        parameters.append(account_id)
    if transaction_id is not None:
        filters.append("id=?")
        parameters.append(transaction_id)
    if start_date is not None:
        filters.append("transaction_date>=?")
        parameters.append(start_date)
    if end_date is not None:
        filters.append("transaction_date<=?")
        parameters.append(end_date)
    scope = " AND ".join(filters)
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history, read_only=True)) as connection:
            if account_id is not None and connection.execute(
                "SELECT 1 FROM accounts WHERE id=?", (account_id,)
            ).fetchone() is None:
                raise HistoryError("The requested account does not exist.")
            if after_transaction_id is not None:
                if not isinstance(after_transaction_id, str) or not after_transaction_id:
                    raise HistoryError("after_transaction_id must be a transaction ID.")
                cursor = connection.execute(
                    f"SELECT 1 FROM transactions WHERE {scope} AND id=?",
                    (*parameters, after_transaction_id),
                ).fetchone()
                if cursor is None:
                    raise HistoryError("The page cursor is not in the selected transaction scope.")
            page_filters = [scope]
            page_parameters = list(parameters)
            if after_transaction_id is not None:
                page_filters.append("id>? ")
                page_parameters.append(after_transaction_id)
            rows = connection.execute(
                "SELECT id,account_id,currency,description,vendor,category,vendor_state,category_state,user_tags,"
                "tag_source_url,tag_source_title,tag_lookup_date,tag_uncertainty,tag_reason,tag_source_kind,tagging_rule_id "
                "FROM transactions WHERE " + " AND ".join(page_filters) +
                " ORDER BY id LIMIT ?", (*page_parameters, limit + 1),
            ).fetchall()
            more = len(rows) > limit
            rows = rows[:limit]
            transactions = [dict(row) for row in rows]
            for row in transactions:
                row["user_tags"] = json.loads(row["user_tags"])

            pairs = {(row["account_id"], row["currency"]) for row in transactions}
            if account_id is not None:
                account = connection.execute("SELECT currency FROM accounts WHERE id=?", (account_id,)).fetchone()
                pairs.add((account_id, account["currency"]))
            conditions: list[str] = []
            rule_parameters: list[object] = []
            currencies = sorted({currency for _, currency in pairs})
            account_pairs = sorted(pairs)
            if currencies:
                conditions.append("(account_id IS NULL AND currency IN (" +
                                  ",".join("?" for _ in currencies) + "))")
                rule_parameters.extend(currencies)
            for rule_account, currency in account_pairs:
                conditions.append("(account_id=? AND currency=?)")
                rule_parameters.extend((rule_account, currency))
            rules = []
            if conditions:
                rules = [dict(row) for row in connection.execute(
                    "SELECT * FROM tagging_rules WHERE active=1 AND (" + " OR ".join(conditions) +
                    ") ORDER BY currency, exact_match, account_id LIMIT 201", tuple(rule_parameters),
                ).fetchall()]
                if len(rules) > 200:
                    raise HistoryError("More than 200 applicable tagging rules exist. Remove unused rules before tagging.")
                for rule in rules:
                    rule["user_tags"] = json.loads(rule["user_tags"])
                    rule["evidence"] = json.loads(rule["evidence"])
            return {
                "transactions": transactions,
                "rules": rules,
                "next_cursor": transactions[-1]["id"] if more and transactions else None,
            }
    except HistoryError:
        raise
    except (sqlite3.Error, json.JSONDecodeError) as error:
        raise HistoryError("Could not read tagging data.") from error


def save_tagging_result(
    transaction_id: str,
    vendor: str | None,
    category: str | None = None,
    user_tags: Sequence[str] | None = None,
    *,
    vendor_state: Literal["unknown", "suggested", "user_confirmed", "rule_confirmed"] = "unknown",
    category_state: Literal["unknown", "user_confirmed", "rule_confirmed"] = "unknown",
    source_kind: Literal["user", "web", "rule"] | None = None,
    source_url: str | None = None,
    source_title: str | None = None,
    lookup_date: str | None = None,
    uncertainty: str | None = None,
    reason: str | None = None,
    tagging_rule_id: str | None = None,
    user_confirmed: bool = False,
    clear: bool = False,
    history_directory: Path | None = None,
) -> dict[str, object]:
    """Save the current vendor, category and user tags without changing financial fields."""
    if not isinstance(transaction_id, str) or not transaction_id:
        raise HistoryError("transaction_id must be a non-empty transaction ID.")
    if not isinstance(vendor_state, str) or vendor_state not in {
        "unknown", "suggested", "user_confirmed", "rule_confirmed"
    }:
        raise HistoryError("vendor_state is not supported.")
    if not isinstance(category_state, str) or category_state not in {"unknown", "user_confirmed", "rule_confirmed"}:
        raise HistoryError("category_state is not supported.")
    if not isinstance(source_kind, str) or source_kind not in {"user", "web", "rule"}:
        raise HistoryError("Choose user, web or rule as the tag source.")
    if vendor is not None and (not isinstance(vendor, str) or not vendor.strip()):
        raise HistoryError("vendor must be non-empty text or None.")
    if category is not None and (not isinstance(category, str) or not category.strip()):
        raise HistoryError("category must be non-empty text or None.")
    for name, value in (("source_url", source_url), ("source_title", source_title),
                        ("uncertainty", uncertainty), ("reason", reason)):
        if value is not None and not isinstance(value, str):
            raise HistoryError(f"{name} must be text or None.")
    tags = _tag_list(user_tags)
    vendor = vendor.strip() if vendor else None
    category = category.strip() if category else None
    if not isinstance(clear, bool):
        raise HistoryError("clear must be True or False.")
    if clear:
        if (user_confirmed is not True or source_kind != "user" or vendor is not None or category is not None or tags or
            source_url is not None or source_title is not None or lookup_date is not None or uncertainty is not None or
            reason is not None or
            tagging_rule_id is not None):
            raise HistoryError("Clear tags only after a direct user request, without other tag values.")
        vendor_state = "unknown"
        category_state = "unknown"
    else:
        if vendor_state == "unknown" and category_state == "unknown" and not tags:
            raise HistoryError("Supply a vendor, category or user tag to save.")
    if (vendor_state == "unknown") != (vendor is None):
        raise HistoryError("Supply a vendor only when vendor_state is not unknown.")
    if (category_state == "unknown") != (category is None):
        raise HistoryError("Supply a category only when category_state is not unknown.")
    if vendor_state == "suggested":
        try:
            parsed = urlsplit(source_url or "")
            hostname = parsed.hostname
        except ValueError as error:
            raise HistoryError("A vendor suggestion needs a valid public source URL.") from error
        if not vendor or source_kind != "web" or parsed.scheme not in {"http", "https"} or not hostname:
            raise HistoryError("A vendor suggestion needs a public HTTP or HTTPS source.")
        if (parsed.username or parsed.password or category is not None or category_state != "unknown" or tags):
            raise HistoryError("A web result can suggest a vendor only; it cannot confirm a category or user tag.")
        lookup_date = _tag_date(lookup_date or datetime.now(timezone.utc).date().isoformat())
        if not isinstance(reason, str) or not reason.strip() or not isinstance(uncertainty, str) or not uncertainty.strip():
            raise HistoryError("A vendor suggestion needs a reason and a short uncertainty note.")
    elif source_kind == "web":
        raise HistoryError("Use web source data only for a vendor suggestion.")
    elif source_kind == "user" and source_url is not None:
        try:
            parsed = urlsplit(source_url)
            hostname = parsed.hostname
        except ValueError as error:
            raise HistoryError("A saved source needs a valid public URL.") from error
        if parsed.scheme not in {"http", "https"} or not hostname or parsed.username or parsed.password:
            raise HistoryError("A saved source needs a valid public HTTP or HTTPS URL.")
        lookup_date = _tag_date(lookup_date)
        if lookup_date is None:
            raise HistoryError("A saved source URL needs its lookup date.")
    elif source_kind == "rule" and any(
        value is not None for value in (source_url, source_title, lookup_date, uncertainty, reason)
    ):
        raise HistoryError("A rule result does not take web source fields.")
    elif any(value is not None for value in (source_title, lookup_date, uncertainty, reason)):
        raise HistoryError("Source title, date and uncertainty need a source URL.")
    if (vendor_state == "user_confirmed" or category_state == "user_confirmed" or
        (tags and source_kind == "user")):
        if source_kind != "user" or user_confirmed is not True:
            raise HistoryError("Save a user classification only after the user confirms it.")
    if vendor_state == "rule_confirmed" or category_state == "rule_confirmed":
        if source_kind != "rule" or not tagging_rule_id:
            raise HistoryError("A rule-based result must include its active rule ID.")
    elif source_kind == "rule" or tagging_rule_id is not None:
        raise HistoryError("Link a tagging rule only when it supplies a confirmed result.")
    lookup_date = _tag_date(lookup_date)
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            transaction = connection.execute(
                "SELECT id, account_id, currency, active FROM transactions WHERE id=?", (transaction_id,)
            ).fetchone()
            if transaction is None or not transaction["active"]:
                raise HistoryError("The requested active transaction does not exist.")
            if tagging_rule_id:
                rule = connection.execute("SELECT * FROM tagging_rules WHERE id=? AND active=1", (tagging_rule_id,)).fetchone()
                if (rule is None or rule["currency"] != transaction["currency"] or
                    rule["account_id"] not in (None, transaction["account_id"]) or
                    _normalise_match(rule["exact_match"]) != _normalise_match(vendor or "")):
                    raise HistoryError("The rule does not apply to this transaction.")
            values = {
                "vendor": vendor, "category": category, "vendor_state": vendor_state,
                "category_state": category_state, "user_tags": _json(tags),
                "tag_source_url": source_url, "tag_source_title": source_title,
                "tag_lookup_date": None if clear else lookup_date,
                "tag_uncertainty": None if clear else uncertainty,
                "tag_reason": None if clear else reason,
                "tag_source_kind": None if clear else source_kind,
                "tagging_rule_id": None if clear else tagging_rule_id,
            }
            assignments = ", ".join(f'"{name}"=?' for name in values)
            connection.execute(f"UPDATE transactions SET {assignments} WHERE id=?", (*values.values(), transaction_id))
            saved = dict(connection.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,)).fetchone())
            saved["user_tags"] = json.loads(saved["user_tags"])
            return saved
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not save the tagging result.") from error


def save_tagging_rule(
    exact_match: str,
    currency: str,
    vendor: str,
    *,
    account_id: str | None = None,
    category: str | None = None,
    user_tags: Sequence[str] | None = None,
    user_confirmed: bool = False,
    active: bool = True,
    history_directory: Path | None = None,
) -> dict[str, object]:
    """Save or disable one exact-match rule after the user confirms its scope and values."""
    if user_confirmed is not True:
        raise HistoryError("Save or remove a rule only after the user confirms the exact match and scope.")
    if not isinstance(exact_match, str) or not exact_match.strip():
        raise HistoryError("exact_match must be non-empty text.")
    if not isinstance(currency, str) or not currency.strip():
        raise HistoryError("currency must be non-empty text.")
    if not isinstance(vendor, str) or not vendor.strip():
        raise HistoryError("vendor must be non-empty text.")
    if category is not None and (not isinstance(category, str) or not category.strip()):
        raise HistoryError("category must be non-empty text or None.")
    if not isinstance(active, bool):
        raise HistoryError("active must be True or False.")
    tags = _tag_list(user_tags)
    exact_match = _normalise_match(exact_match)
    currency = currency.strip()
    vendor = vendor.strip()
    category = category.strip() if category else None
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    history = _prepare_selected_history(history_directory)
    try:
        with closing(_connect_history(history)) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            if account_id is not None:
                account = connection.execute("SELECT currency FROM accounts WHERE id=?", (account_id,)).fetchone()
                if account is None or account["currency"] != currency:
                    raise HistoryError("The rule account does not exist or uses a different currency.")
            existing = connection.execute(
                "SELECT * FROM tagging_rules WHERE account_id IS ? AND currency=? AND exact_match=?",
                (account_id, currency, exact_match),
            ).fetchone()
            if not active:
                if existing is None or not existing["active"]:
                    raise HistoryError("The active rule does not exist.")
                connection.execute("UPDATE tagging_rules SET active=0, updated_at=? WHERE id=?", (now, existing["id"]))
                row = dict(connection.execute("SELECT * FROM tagging_rules WHERE id=?", (existing["id"],)).fetchone())
                row["user_tags"] = json.loads(row["user_tags"])
                row["evidence"] = json.loads(row["evidence"])
                return row
            rule_id = existing["id"] if existing else _id()
            evidence = _json({
                "confirmed_by_user": True,
                "confirmed_at": now,
                "scope": "account" if account_id else "history_currency",
                "account_id": account_id,
                "currency": currency,
                "exact_match": exact_match,
                "vendor": vendor,
                "category": category,
                "user_tags": tags,
            })
            values = {
                "id": rule_id, "account_id": account_id, "currency": currency,
                "exact_match": exact_match, "vendor": vendor, "category": category,
                "user_tags": _json(tags), "evidence": evidence,
                "active": 1, "created_at": existing["created_at"] if existing else now, "updated_at": now,
            }
            _validate_fields("tagging_rules", values)
            _validate_row_links(connection, "tagging_rules", values)
            if existing:
                updates = {name: value for name, value in values.items() if name not in {"id", "created_at"}}
                assignments = ", ".join(f'"{name}"=?' for name in updates)
                connection.execute(f"UPDATE tagging_rules SET {assignments} WHERE id=?",
                                   (*updates.values(), rule_id))
            else:
                connection.execute(
                    "INSERT INTO tagging_rules (" + ", ".join(f'"{name}"' for name in values) +
                    ") VALUES (" + ", ".join("?" for _ in values) + ")", tuple(values.values()),
                )
            row = dict(connection.execute("SELECT * FROM tagging_rules WHERE id=?", (rule_id,)).fetchone())
            row["user_tags"] = json.loads(row["user_tags"])
            row["evidence"] = json.loads(row["evidence"])
            return row
    except HistoryError:
        raise
    except sqlite3.Error as error:
        raise HistoryError("Could not save the tagging rule.") from error


def save_account(
    history: Path,
    fields: Mapping[str, str | int | None],
    evidence: Evidence,
    *,
    account_id: str | None = None,
) -> str:
    """Save the account fields needed for statement import."""
    account_id = account_id or _id()
    history = _prepare_selected_history(history)
    with closing(_connect_history(history)) as connection, connection:
        connection.execute("BEGIN IMMEDIATE")
        _upsert_account(connection, fields, evidence, account_id)
    return account_id


def _upsert_account(connection: sqlite3.Connection, fields: Mapping[str, str | int | None],
                    evidence: Evidence, account_id: str) -> None:
    values = {"id": account_id, "alias": fields["alias"], "bank": fields.get("bank"),
              "type": fields.get("type"), "identity_evidence": evidence.quote,
              "currency": fields["currency"], "precision": fields["precision"]}
    _validate_fields("accounts", values)
    _validate_row_links(connection, "accounts", values)
    connection.execute(
        "INSERT INTO accounts (id,alias,bank,type,identity_evidence,currency,precision) VALUES (?,?,?,?,?,?,?) "
        "ON CONFLICT(id) DO UPDATE SET alias=excluded.alias,bank=excluded.bank,type=excluded.type,"
        "identity_evidence=excluded.identity_evidence,currency=excluded.currency,precision=excluded.precision",
        tuple(values.values()),
    )


def _save_file(connection: sqlite3.Connection, fields: Mapping[str, object]) -> str:
    existing = connection.execute("SELECT id FROM files WHERE content_hash=?", (fields["content_hash"],)).fetchone()
    if existing:
        return str(existing["id"])
    return str(_insert_row(connection, "files", fields)["id"])


def _save_statement(connection: sqlite3.Connection, fields: Mapping[str, object]) -> str:
    statement_id = str(fields["id"])
    existing = connection.execute("SELECT 1 FROM statements WHERE id=?", (statement_id,)).fetchone()
    if existing:
        _update_row_on_connection(connection, "statements", statement_id, {
            "start_evidence": fields["start_evidence"], "end_evidence": fields["end_evidence"],
            "reader": fields["reader"], "outcome": fields["outcome"], "questions": fields["questions"],
        })
    else:
        _insert_row(connection, "statements", fields)
    return statement_id


def _delete_unaccepted_records(connection: sqlite3.Connection, statement_id: str) -> None:
    rows = connection.execute(
        "SELECT id, accepted, transaction_id FROM statement_records WHERE statement_id=?", (statement_id,)
    ).fetchall()
    if any(row["accepted"] or row["transaction_id"] for row in rows):
        raise HistoryError("Incomplete import contains accepted rows; review recovery before retrying.")
    if rows:
        marks = ",".join("?" for _ in rows)
        ids = tuple(row["id"] for row in rows)
        if connection.execute(
            f"SELECT 1 FROM transactions WHERE supporting_record IN ({marks}) LIMIT 1", ids
        ).fetchone():
            raise HistoryError("Incomplete import contains linked transactions; review recovery before retrying.")
    for row in rows:
        _delete_linked_rows(connection, "statement_records", row["id"])


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
    history = _prepare_selected_history(history)
    with closing(_connect_history(history)) as connection, connection:
        connection.execute("BEGIN IMMEDIATE")
        file_id = _save_file(connection, {
            "id": _id(), "content_hash": digest, "size": file_size,
            "format": source.suffix.lower().lstrip("."), "original_name": source.name,
            "managed_path": digest, "copy_state": "not_retained",
        })
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
                    "SELECT id, section, start, end, file_id, outcome, date_basis FROM statements "
                    "WHERE file_id=? AND account_id=? AND scope=? AND card_id IS ?",
                    (file_id, section.account_id, section.scope, section.card_id),
                ).fetchone()
            if duplicate:
                if duplicate["file_id"] != file_id or duplicate["date_basis"] != section.date_basis:
                    raise HistoryError("Saved period has different source or date basis; review a correction.")
                if duplicate["outcome"] == "imported":
                    results.append({"section": duplicate["section"], "statement_id": duplicate["id"],
                                    "outcome": "already_imported", "added": 0, "skipped": len(section.records)})
                    continue
                if duplicate["outcome"] not in {"partially_imported", "failed"}:
                    raise HistoryError("Incomplete import contains accepted rows; review recovery before retrying.")
                _delete_unaccepted_records(connection, duplicate["id"])
            account = connection.execute("SELECT * FROM accounts WHERE id=?", (section.account_id,)).fetchone()
            if account is None or account["type"] not in {"transaction", "savings", "credit", "loan"}:
                raise HistoryError("Select an existing account with a supported type.")
            prepared, reconciled = _prepare_statement(section, account)
            statement_id, section_id = (duplicate["id"], duplicate["section"]) if duplicate else (_id(), _id())
            if duplicate:
                prior_ranges = [row for row in prior_ranges if row["id"] != statement_id]
            _save_statement(connection, {
                "id": statement_id, "file_id": file_id, "section": section_id,
                "account_id": section.account_id, "scope": section.scope, "card_id": section.card_id,
                "start": section.start, "end": section.end,
                "start_evidence": _json(asdict(section.start_evidence)) if section.start_evidence else None,
                "end_evidence": _json(asdict(section.end_evidence)) if section.end_evidence else None,
                "date_basis": section.date_basis, "reader": "llm input", "outcome": "imported", "questions": "[]",
            })
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
                _insert_row(connection, "statement_records", {
                    "id": record_id, "statement_id": statement_id,
                    "fingerprint": hashlib.sha256(f"{statement_id}:{index}".encode()).hexdigest(),
                    "occurrence": 1, "kind": record.kind, "source_location": _json(source_location),
                    "source_quote": record.evidence.quote, "transaction_date": dates["transaction_date"],
                    "posting_date": dates["posting_date"], "amount_text": raw_amount, "amount_minor": amount,
                    "currency": record.currency, "description": record.description,
                    "bank_reference": record.bank_reference, "reliable_reference": int(record.reliable_reference),
                    "card_id": record.card_id or section.card_id, "status": record.status or "posted",
                    "balance_date": dates["balance_date"], "balance_type": record.balance_type,
                    "transaction_id": None,
                })
                if transaction_id:
                    _insert_row(connection, "transactions", {
                        "id": transaction_id, "account_id": section.account_id,
                        "card_id": record.card_id or section.card_id,
                        "transaction_date": dates["transaction_date"], "posting_date": dates["posting_date"],
                        "amount": amount, "currency": record.currency, "description": record.description,
                        "bank_reference": record.bank_reference, "reliable_reference": int(record.reliable_reference),
                        "status": record.status or "posted", "supporting_record": record_id,
                    })
                    added += 1
            outcome = "partially_imported" if skipped and added else "already_imported" if skipped else "imported"
            _update_row_on_connection(connection, "statements", statement_id, {"outcome": outcome})
            results.append({"section": section_id, "statement_id": statement_id,
                            "outcome": outcome, "added": added, "skipped": skipped,
                            "reconciled": reconciled})
    return results
