from __future__ import annotations

import sys
import sqlite3
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).parents[2] / "skills" / "bank-statement-ingestion" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import bank_history as bank


class StatementUploadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.history = self.root / "history"
        bank.create_history(self.history)
        user = bank.Evidence("AUD account with two decimal places", "chat", "user")
        self.account = bank.save_account(self.history, {"alias": "Main", "type": "transaction", "currency": "AUD", "precision": 2}, user)
        self.source = self.root / "statement.csv"
        self.source.write_text("19/09/24 Shop -1.234,50\n")

    def record(self, *, date_text: str = "19/09/24", date_format: str = "%d/%m/%y") -> bank.Record:
        return bank.Record(
            evidence=bank.Evidence(f"{date_text} Shop -1.234,50", "row:2", "record"),
            transaction_date=None,
            raw_dates=(("transaction_date", date_text),),
            date_formats=(("transaction_date", date_format),),
            raw_amount="-1.234,50",
            amount_decimal_separator=",",
            amount_group_separator=".",
            currency="AUD",
            description="Shop",
            status="posted",
        )

    def statement(self, record: bank.Record) -> bank.Statement:
        return bank.Statement(account_id=self.account, records=(record,), start="2024-09-01", end="2024-09-30")

    def test_upload_uses_supplied_formats_and_writes_the_rows(self) -> None:
        result = bank.save_statement(self.history, self.source, (self.statement(self.record()),))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            rows = connection.execute("SELECT transaction_date, amount, description FROM transactions").fetchall()
        self.assertEqual(result[0]["added"], 1)
        self.assertEqual(rows[0], ("2024-09-19", -123450, "Shop"))

    def test_bad_conversion_writes_no_rows(self) -> None:
        with self.assertRaises(bank.HistoryError):
            bank.save_statement(self.history, self.source, (self.statement(self.record(date_format="%Q")),))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 0)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM statements").fetchone()[0], 0)

    def test_reupload_skips_records_in_an_existing_header_range(self) -> None:
        monthly = self.statement(self.record())
        bank.save_statement(self.history, self.source, (monthly,))

        yearly_source = self.root / "year.csv"
        yearly_source.write_text("year statement")
        yearly = bank.Statement(
            account_id=self.account,
            records=(self.record(), self.record(date_text="20/10/24")),
            start="2024-01-01",
            end="2024-12-31",
        )
        result = bank.save_statement(self.history, yearly_source, (yearly,))

        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            dates = connection.execute("SELECT transaction_date FROM transactions ORDER BY transaction_date").fetchall()
        self.assertEqual(dates, [("2024-09-19",), ("2024-10-20",)])
        self.assertEqual((result[0]["outcome"], result[0]["added"], result[0]["skipped"]), ("partially_imported", 1, 1))

    def test_reupload_same_statement_does_not_add_rows_or_statements(self) -> None:
        statement = self.statement(self.record())
        bank.save_statement(self.history, self.source, (statement,))
        result = bank.save_statement(self.history, self.source, (statement,))

        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            transaction_count = connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            statement_count = connection.execute("SELECT COUNT(*) FROM statements").fetchone()[0]
        self.assertEqual((transaction_count, statement_count), (1, 1))
        self.assertEqual((result[0]["outcome"], result[0]["added"]), ("already_imported", 0))

    def test_same_header_range_for_another_account_is_imported(self) -> None:
        other_account = bank.save_account(
            self.history,
            {"alias": "Other", "type": "transaction", "currency": "AUD", "precision": 2},
            bank.Evidence("AUD account", "chat", "user"),
        )
        other_statement = bank.Statement(
            account_id=other_account,
            records=(self.record(),),
            start="2024-09-01",
            end="2024-09-30",
        )

        result = bank.save_statement(self.history, self.source, (other_statement,))

        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            rows = connection.execute("SELECT account_id, transaction_date FROM transactions ORDER BY account_id").fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (other_account, "2024-09-19"))
        self.assertEqual((result[0]["outcome"], result[0]["added"]), ("imported", 1))


if __name__ == "__main__":
    unittest.main()
