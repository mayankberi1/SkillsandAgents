---
name: bank-statement-ingestion
description: >
  Read bank statements, save accepted transaction and balance history, run maintenance and coverage checks. Trigger on: statements to import, corrections to apply, coverage recalculation, safety buffer checks, deletion requests. Use when the user supplies statement files (text PDF, CSV or XLSX) and asks to ingest them into a local personal history, or to correct, delete, export or review saved statement data.
---
# Bank statement ingestion

This version supports statement import only. It does not support corrections, reports, tagging, coverage checks, deletion, export or restore.

Read uploaded statements with the available document skills. For each file, identify the account and read its rows. Choose the date and amount formats from the statement.

Build `Statement` and `Record` values. Save statement header dates as `YYYY-MM-DD`; ask the user if a header date is unclear. Keep each original transaction date and amount text. Pass each date format to `date_formats`. Pass the decimal and group separators to `amount_decimal_separator` and `amount_group_separator`. Include the source location and sign evidence.

Call `bank_history.save_statement(history, source, sections)` once per file. It converts dates and amounts, then writes the rows in one database transaction. It saves file details but does not keep a copy of the file. It skips rows whose dates fall inside a saved statement's header date range. It reports skipped row counts.

Use `YYYY-MM-DD` for saved dates. Store money as exact currency minor units. Do not round amounts. The script supports Python `strptime` date patterns, including `%y` for a two-digit year. It uses the supplied amount separators as given.

## Setup

Use Python 3.13 or later. `bank_history.py` uses built-in libraries. Import it from the skill's `scripts` folder. The document skills handle PDF and spreadsheet reading. Do not add a `requirements.txt` file.
