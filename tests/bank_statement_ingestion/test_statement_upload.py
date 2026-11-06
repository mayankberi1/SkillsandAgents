from __future__ import annotations

import sys
import sqlite3
import tempfile
import unittest
from dataclasses import replace
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

    def test_debit_credit_signs_depend_on_account_type(self) -> None:
        for account_type, expected in (("transaction", "1234.50"), ("credit", "-1234.50"), ("loan", "-1234.50")):
            self.assertEqual(bank._convert_amount("1,234.50 CR", ".", ",", account_type=account_type), expected)
        evidence = bank.Evidence("Debits", "column", "header")
        self.assertEqual(bank._convert_amount("25.00", ".", "", sign_evidence=evidence), "-25.00")
        self.assertEqual(bank._convert_amount("(25.00)", ".", ""), "-25.00")
        with self.assertRaises(bank.HistoryError):
            bank._convert_amount("-25.00 CR", ".", "")

    def test_leading_and_trailing_minus_preserve_original_text(self) -> None:
        for raw in ("-300.00", "-$300.00", "$300.00-", "300.00-", "300.00−", " 300.00- ", "1,000.00-", "300.00- CR"):
            with self.subTest(raw=raw):
                amount = bank._convert_amount(raw, ".", ",", account_type="credit")
                self.assertEqual(bank.minor_units(amount, 2), -100000 if "1,000" in raw else -30000)
        for raw in ("-300.00-", "+300.00-", "(300.00)-", "300.00- DR"):
            with self.subTest(raw=raw), self.assertRaises(bank.HistoryError):
                bank._convert_amount(raw, ".", "", account_type="credit")
        record = replace(self.record(), raw_amount="1,234.50-",
                         amount_decimal_separator=".", amount_group_separator=",")
        bank.save_statement(self.history, self.source, (self.statement(record),))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            self.assertEqual(connection.execute("SELECT amount_text,amount_minor FROM statement_records").fetchone(),
                             ("1,234.50-", -123450))

    def test_balance_mismatch_rolls_back_file_and_records(self) -> None:
        opening = bank.Record(
            evidence=bank.Evidence("Opening balance", "opening", "record"), kind="balance",
            balance_date="2024-09-01", balance_type="opening", raw_amount="2000.00 CR",
            amount_decimal_separator=".", amount_group_separator="", currency="AUD")
        closing = replace(opening, evidence=bank.Evidence("Closing balance", "closing", "record"),
                          balance_date="2024-09-30", balance_type="closing", raw_amount="765.55 CR")
        statement = replace(self.statement(self.record()), records=(opening, self.record(), closing))
        with self.assertRaises(bank.HistoryError):
            bank.save_statement(self.history, self.source, (statement,))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM files").fetchone()[0], 0)
        statement = replace(statement, records=(opening, self.record(), replace(closing, raw_amount="765.50 CR")))
        self.assertTrue(bank.save_statement(self.history, self.source, (statement,))[0]["reconciled"])

    def test_retry_unaccepted_import_and_refuse_accepted_partial(self) -> None:
        statement = self.statement(self.record())
        bank.save_statement(self.history, self.source, (statement,))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            connection.execute("UPDATE statements SET outcome='partially_imported'")
        with self.assertRaises(bank.HistoryError):
            bank.save_statement(self.history, self.source, (statement,))
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            connection.execute("DELETE FROM transactions")
            connection.execute("UPDATE statement_records SET accepted=0,transaction_id=NULL")
        self.assertEqual(bank.save_statement(self.history, self.source, (statement,))[0]["added"], 1)
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM statement_records").fetchone()[0], 1)

    def test_identical_purchases_remain_separate_and_totals_are_checked(self) -> None:
        second = replace(self.record(), evidence=bank.Evidence("Second purchase", "row:3", "record"))
        statement = replace(self.statement(self.record()), records=(self.record(), second), expected_debits="2469.00")
        self.assertEqual(bank.save_statement(self.history, self.source, (statement,))[0]["added"], 2)

    def test_changed_file_is_not_silently_skipped(self) -> None:
        statement = self.statement(self.record())
        bank.save_statement(self.history, self.source, (statement,))
        self.source.write_text("changed source")
        with self.assertRaises(bank.HistoryError):
            bank.save_statement(self.history, self.source, (statement,))

    def test_overlap_outcome_is_saved_and_unsigned_amount_is_rejected(self) -> None:
        statement = replace(self.statement(self.record()), records=(replace(self.record(), raw_amount="123.45"),))
        with self.assertRaises(bank.HistoryError):
            bank.save_statement(self.history, self.source, (statement,))
        self.test_reupload_skips_records_in_an_existing_header_range()
        with sqlite3.connect(self.history / "history.sqlite3") as connection:
            self.assertEqual(connection.execute("SELECT outcome FROM statements ORDER BY rowid DESC LIMIT 1").fetchone()[0],
                             "partially_imported")


if __name__ == "__main__":
    unittest.main()
