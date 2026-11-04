# /// script
# requires-python = ">=3.13"
# dependencies = ["defusedxml==0.7.1"]
# ///
"""Read selected statement files without running their formulas or instructions."""

from __future__ import annotations

import csv
import hashlib
import json
import multiprocessing
import os
import re
import signal
import shutil
import subprocess
import tempfile
import zipfile
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Literal, Sequence
from xml.etree.ElementTree import Element

MAX_FILE = 50 * 1024 * 1024
MAX_BATCH = 500 * 1024 * 1024
MAX_FILES = 100
MAX_PAGES = 1000
MAX_ROWS = 250_000
MAX_EXPANDED = 250 * 1024 * 1024
MAX_ENTRIES = 10_000
MAX_ENTRY = 25 * 1024 * 1024
MAX_FIELD = 1024 * 1024
MAX_TEXT = 64 * 1024 * 1024
MAX_REQUEST = 16 * 1024 * 1024
MAX_SECONDS = 120
MAX_MEMORY = 1024 * 1024 * 1024


class ReadError(ValueError):
    """The supplied file cannot be read within the required protections."""


def _period_metadata(text: str) -> bool:
    return bool(re.match(r"^(?:Account [^:]+:\s*)?(?:(?:Statement\s+)?Period\b|Statement (?:start|end)\b|From\b.*\bto\b)", text.strip(), re.IGNORECASE))


def _columns(cells: Sequence[str]) -> bool:
    names = {cell.strip().lower() for cell in cells}
    return bool(names & {"date", "transaction date", "posting date"}) and bool(names & {"amount", "debit", "credit", "description"})


def _add(fragments: list[dict[str, object]], location: str, text: str, *, header: bool = False, usable: bool = True, cells: list[dict[str, str | bool | None]] | None = None) -> None:
    if len(fragments) >= MAX_ROWS:
        raise ReadError("The document exceeds the row limit.")
    fragments.append({"location": location, "text": text, "header": header, "usable": usable, "cells": cells or []})


def _csv(path: Path, mode: str) -> list[dict[str, object]]:
    fragments: list[dict[str, object]] = []
    csv.field_size_limit(MAX_FIELD)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for index, cells in enumerate(csv.reader(stream, strict=True), 1):
            if index > MAX_ROWS:
                raise ReadError("The document exceeds the row limit.")
            if mode == "headers" and (index > 20 or re.match(r"^\d{4}-\d{2}-\d{2}(?:\b|,)", cells[0] if cells else "")):
                break
            text = ",".join(cells)
            header = index <= 20 and _period_metadata(text)
            values = [{"reference": str(column), "text": value, "type": "text"} for column, value in enumerate(cells, 1)]
            _add(fragments, f"header:{index}" if header else f"row:{index}", text, header=header, cells=values)
            if mode == "headers" and _columns(cells):
                break
    return fragments


def _xml(data: bytes) -> Element:
    try:
        from defusedxml import ElementTree
    except ImportError as error:
        raise ReadError("XLSX needs defusedxml==0.7.1 in the prepared Python environment; request setup first.") from error
    return ElementTree.fromstring(data, forbid_dtd=True, forbid_entities=True, forbid_external=True)


def _excel_date(value: str, epoch_1904: bool) -> str | None:
    if len(value) > 100 or not re.fullmatch(r"\d+(?:\.\d+)?(?:[eE][+-]?\d{1,3})?", value):
        return None
    serial = Decimal(value)
    if serial < 0 or serial > 3_000_000 or (not epoch_1904 and 60 <= serial < 61):
        return None
    base = date(1904, 1, 1) if epoch_1904 else date(1899, 12, 30) if serial >= 61 else date(1899, 12, 31)
    try:
        return (base + timedelta(days=int(serial))).isoformat()
    except (OverflowError, ValueError):
        return None


def _xlsx(path: Path, mode: str, sections: Sequence[str] | None) -> list[dict[str, object]]:
    fragments: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) > MAX_ENTRIES or sum(entry.file_size for entry in entries) > MAX_EXPANDED:
            raise ReadError("The XLSX archive exceeds its entry or expanded-size limit.")
        names = set()
        for entry in entries:
            name = entry.filename
            if name in names or name.startswith("/") or ".." in PurePosixPath(name).parts or "\\" in name or entry.flag_bits & 1:
                raise ReadError("Unsafe, encrypted or repeated XLSX archive entry.")
            if entry.file_size > MAX_ENTRY or (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ReadError("Oversized or linked XLSX archive entry.")
            if any(part in name.lower() for part in ("vbaproject", "externallinks/", "embeddings/", "activex/")):
                raise ReadError("Macro, embedded or external workbook content is unsupported.")
            names.add(name)
        # Check every relationship and XML part before a workbook library could use it.
        for entry in entries:
            if entry.filename.endswith((".xml", ".rels")):
                document = _xml(archive.read(entry))
                for element in document.iter():
                    if element.tag.rsplit("}", 1)[-1] == "Relationship" and element.get("TargetMode", "").lower() == "external":
                        raise ReadError("External XLSX relationships are unsupported.")
                    if mode == "records" and element.tag.rsplit("}", 1)[-1] in {"f", "definedName"}:
                        raise ReadError("Workbook formulas or defined names need review; no value was evaluated.")
        workbook = _xml(archive.read("xl/workbook.xml"))
        properties = next((element for element in workbook if element.tag.rsplit("}", 1)[-1] == "workbookPr"), None)
        if properties is not None and properties.get("date1904", "0") not in {"0", "1", "true", "false"}:
            raise ReadError("The workbook date epoch is unclear.")
        epoch_1904 = properties is not None and properties.get("date1904", "0") in {"1", "true"}
        date_styles = set()
        if "xl/styles.xml" in names:
            styles = _xml(archive.read("xl/styles.xml"))
            formats = next((element for element in styles if element.tag.rsplit("}", 1)[-1] == "cellXfs"), ())
            date_styles = {str(index) for index, element in enumerate(formats) if element.get("numFmtId") in {"14", "15", "16", "17", "22"}}
        relationships = _xml(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {element.get("Id"): element.get("Target") for element in relationships}
        strings = []
        if "xl/sharedStrings.xml" in names:
            strings = ["".join(item.itertext()) for item in _xml(archive.read("xl/sharedStrings.xml"))]
        selected = set(sections or ())
        found = set()
        for sheet in workbook.iter():
            if sheet.tag.rsplit("}", 1)[-1] != "sheet":
                continue
            title = sheet.get("name")
            if selected and title not in selected:
                continue
            if title in found:
                raise ReadError("Repeated worksheet name.")
            found.add(title)
            reference = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = targets.get(reference)
            if not target or target.startswith("/") or ".." in PurePosixPath(target).parts:
                raise ReadError("Unsupported workbook sheet relationship.")
            document = _xml(archive.read("xl/" + target))
            seen_rows = set()
            for row_index, row in enumerate((element for element in document.iter() if element.tag.rsplit("}", 1)[-1] == "row"), 1):
                if mode == "headers" and row_index > 20:
                    break
                cells = []
                row_number = row.get("r", str(row_index))
                if not re.fullmatch(r"[1-9][0-9]*", row_number) or row_number in seen_rows:
                    raise ReadError("Invalid or repeated worksheet row.")
                seen_rows.add(row_number)
                seen_cells = set()
                for cell in row:
                    if cell.tag.rsplit("}", 1)[-1] != "c":
                        continue
                    kind = cell.get("t", "n")
                    reference = cell.get("r", "")
                    if not re.fullmatch(r"[A-Z]+" + row_number, reference) or reference in seen_cells:
                        raise ReadError("Invalid or repeated worksheet cell.")
                    seen_cells.add(reference)
                    value = next((element.text or "" for element in cell if element.tag.rsplit("}", 1)[-1] == "v"), "")
                    if kind == "s":
                        if not value.isdecimal() or int(value) >= len(strings):
                            raise ReadError("Invalid shared-string reference.")
                        value = strings[int(value)]
                    elif kind == "inlineStr":
                        value = "".join(element.text or "" for element in cell.iter() if element.tag.rsplit("}", 1)[-1] == "t")
                    if any(element.tag.rsplit("}", 1)[-1] == "f" for element in cell):
                        kind, value = "formula", ""
                    cell_data: dict[str, str | bool | None] = {"reference": reference, "text": value, "type": kind}
                    if cell.get("s", "0") in date_styles and kind == "n":
                        cell_data.update(date_style=True, canonical_date=_excel_date(value, epoch_1904))
                    cells.append(cell_data)
                values = [cell["text"] for cell in cells]
                if mode == "headers" and values and re.match(r"^\d{4}-\d{2}-\d{2}\b", values[0]):
                    break
                text = "\t".join(values)
                header = row_index <= 20 and _period_metadata(text)
                usable = all(cell["type"] in {"n", "s", "inlineStr", "str", "d"} for cell in cells)
                _add(fragments, f"sheet:{title}:row:{row.get('r', str(row_index))}", text, header=header, usable=usable, cells=cells)
                if mode == "headers" and _columns(values):
                    break
        if selected - found:
            raise ReadError("A selected worksheet is missing.")
    return fragments


def _pdf(path: Path, mode: str) -> list[dict[str, object]]:
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        raise ReadError("PDF needs the installed pdfinfo and pdftotext tools; request setup first.")
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, check=True, timeout=MAX_SECONDS).stdout.decode("utf-8", "replace")
    pages_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    size_match = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+)", info, re.MULTILINE)
    if not pages_match or not size_match or int(pages_match[1]) > MAX_PAGES:
        raise ReadError("Unsupported PDF page information or page limit exceeded.")
    fragments: list[dict[str, object]] = []
    for page in range(1, int(pages_match[1]) + 1):
        command = ["pdftotext", "-f", str(page), "-l", str(page), "-layout"]
        if mode == "headers":
            command.extend(["-x", "0", "-y", "0", "-W", str(int(float(size_match[1]))), "-H", str(int(float(size_match[2]) / 4))])
        output = subprocess.run([*command, str(path), "-"], capture_output=True, check=True, timeout=MAX_SECONDS).stdout
        if len(output) > MAX_TEXT:
            raise ReadError("Extracted text exceeds its limit.")
        for index, text in enumerate(output.decode("utf-8").replace("\f", "").splitlines(), 1):
            if not text.strip():
                continue
            if mode == "headers" and (_columns(text.split()) or re.match(r"^\d{4}-\d{2}-\d{2}\b", text.strip())):
                break
            header = _period_metadata(text)
            _add(fragments, f"page:{page}:{'header' if mode == 'headers' else 'line'}:{index}", text, header=header if mode == "headers" else False)
    if mode == "records" and not fragments:
        raise ReadError("No PDF text was found; scanned statements need a later feature.")
    return fragments


def _worker(path: Path, mode: str, sections: Sequence[str] | None, destination: Path) -> None:
    try:
        import resource
        os.setsid()
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_SECONDS, MAX_SECONDS))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_TEXT * 2, MAX_TEXT * 2))
        if path.suffix == ".csv":
            fragments = _csv(path, mode)
        elif path.suffix == ".xlsx":
            fragments = _xlsx(path, mode, sections)
        else:
            fragments = _pdf(path, mode)
        if sum(len(str(fragment["text"]).encode()) for fragment in fragments) > MAX_TEXT:
            raise ReadError("Extracted text exceeds its limit.")
        result = {"outcome": "read", "fragments": fragments, "complete": mode == "records"}
    except (Exception, MemoryError) as error:
        result = {"outcome": "unsupported" if isinstance(error, (ReadError, ImportError)) else "failed", "fragments": [], "complete": False, "explanation": str(error) or type(error).__name__}
    try:
        destination.write_text(json.dumps(result), encoding="utf-8")
    except OSError:
        destination.unlink(missing_ok=True)


def read_statement(source: Path, *, mode: Literal["headers", "records"] = "records", sections: Sequence[str] | None = None) -> dict[str, object]:
    """Read a bounded private snapshot in a separate process; never install software."""
    source = Path(source)
    if mode not in {"headers", "records"} or len(json.dumps(list(sections or ())).encode()) > MAX_REQUEST:
        raise ReadError("Unsupported reading mode or oversized input.")
    if source.is_symlink() or not source.is_file() or source.suffix.lower() not in {".pdf", ".csv", ".xlsx"}:
        return {"outcome": "unsupported", "fragments": [], "complete": False, "explanation": "Supply a regular PDF, CSV or XLSX file."}
    try:
        import resource  # noqa: F401
        context = multiprocessing.get_context("fork")
    except (ImportError, ValueError):
        return {"outcome": "unsupported", "fragments": [], "complete": False, "explanation": "This host lacks the required process and resource protections."}
    with tempfile.TemporaryDirectory(prefix="bank-read-") as temporary:
        directory = Path(temporary)
        snapshot, result_path = directory / ("source" + source.suffix.lower()), directory / "result.json"
        digest, size = hashlib.sha256(), 0
        with source.open("rb") as incoming, snapshot.open("xb") as outgoing:
            os.chmod(snapshot, 0o600)
            while block := incoming.read(1024 * 1024):
                size += len(block)
                if size > MAX_FILE:
                    return {"outcome": "unsupported", "fragments": [], "complete": False, "explanation": "The source exceeds the file-size limit."}
                digest.update(block)
                outgoing.write(block)
        process = context.Process(target=_worker, args=(snapshot, mode, sections, result_path))
        process.start()
        process.join(MAX_SECONDS)
        if process.is_alive():
            os.killpg(process.pid, signal.SIGKILL)
            process.join()
            return {"outcome": "failed", "fragments": [], "complete": False, "explanation": "Reader time limit exceeded."}
        if process.exitcode != 0 or not result_path.is_file() or result_path.stat().st_size > MAX_TEXT * 2:
            return {"outcome": "failed", "fragments": [], "complete": False, "explanation": "Reader stopped or exceeded a required resource limit."}
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result.update(source_hash=digest.hexdigest(), format=source.suffix.lower()[1:], mode=mode, reader="statement_reader/1", limitations=["Only explicit period metadata establishes header dates; other layouts need user answers."])
        return result


def read_batch(sources: Sequence[Path], *, mode: Literal["headers", "records"] = "records") -> list[dict[str, object]]:
    size = 0
    for path in sources:
        try:
            size += Path(path).stat().st_size
        except OSError:
            continue
    if len(sources) > MAX_FILES or size > MAX_BATCH:
        raise ReadError("The batch exceeds its file-count or total-size limit.")
    results = []
    for path in sources:
        try:
            results.append(read_statement(path, mode=mode))
        except (OSError, ReadError) as error:
            results.append({"outcome": "failed", "explanation": str(error), "fragments": [], "complete": False})
    return results
