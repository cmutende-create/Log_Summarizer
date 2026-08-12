"""Generic CSV cleaning helpers."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

MISSING_VALUES = {"", "na", "n/a", "none", "null", "-"}
DATE_FORMATS = (
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%m-%d-%Y",
)


@dataclass
class CleaningReport:
    """Summary of changes made while cleaning a CSV file."""

    input_rows: int = 0
    output_rows: int = 0
    skipped_blank_rows: int = 0
    missing_cells_filled: int = 0
    extra_cells_dropped: int = 0
    normalized_cells: int = 0
    renamed_headers: list[str] = field(default_factory=list)


def clean_csv(input_path: str | Path, output_path: str | Path) -> CleaningReport:
    """Clean a CSV file without assuming a sales-specific schema."""

    report = CleaningReport()

    with open(input_path, newline="", encoding="utf-8") as source:
        reader = csv.reader(source)
        raw_headers = next(reader, [])
        headers = clean_headers(raw_headers, report)

        with open(output_path, "w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target)
            writer.writerow(headers)

            for raw_row in reader:
                report.input_rows += 1
                if not any(cell.strip() for cell in raw_row):
                    report.skipped_blank_rows += 1
                    continue

                cleaned_row = clean_row(raw_row, len(headers), report)
                writer.writerow(cleaned_row)
                report.output_rows += 1

    return report


def clean_headers(headers: list[str], report: CleaningReport) -> list[str]:
    """Trim, fill, and deduplicate header names."""

    cleaned_headers: list[str] = []
    seen: dict[str, int] = {}

    for index, header in enumerate(headers, start=1):
        original = header
        cleaned = " ".join(header.strip().split())

        if not cleaned:
            cleaned = f"column_{index}"

        count = seen.get(cleaned, 0) + 1
        seen[cleaned] = count
        if count > 1:
            cleaned = f"{cleaned}_{count}"

        if cleaned != original:
            report.renamed_headers.append(f"{original!r} -> {cleaned!r}")

        cleaned_headers.append(cleaned)

    return cleaned_headers


def clean_row(row: list[str], expected_cells: int, report: CleaningReport) -> list[str]:
    """Clean a row and make its length match the header length."""

    cleaned_row = row[:expected_cells]
    if len(row) > expected_cells:
        report.extra_cells_dropped += len(row) - expected_cells

    if len(cleaned_row) < expected_cells:
        report.missing_cells_filled += expected_cells - len(cleaned_row)
        cleaned_row.extend([""] * (expected_cells - len(cleaned_row)))

    return [clean_cell(cell, report) for cell in cleaned_row]


def clean_cell(value: str, report: CleaningReport) -> str:
    """Normalize common dirty CSV cell values."""

    original = value
    cleaned = " ".join(value.strip().split())

    if cleaned.lower() in MISSING_VALUES:
        cleaned = ""
    else:
        cleaned = normalize_boolean(cleaned)
        cleaned = normalize_number(cleaned)
        cleaned = normalize_date(cleaned)

    if cleaned != original:
        report.normalized_cells += 1

    return cleaned


def normalize_boolean(value: str) -> str:
    lowered = value.lower()
    if lowered in {"yes", "y", "true"}:
        return "true"
    if lowered in {"no", "n", "false"}:
        return "false"
    return value


def normalize_number(value: str) -> str:
    candidate = value.replace(",", "")
    if candidate.startswith("$"):
        candidate = candidate[1:]

    try:
        number = float(candidate)
    except ValueError:
        return value

    if number.is_integer():
        return str(int(number))

    return str(number)


def normalize_date(value: str) -> str:
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).date().isoformat()
        except ValueError:
            continue

    return value
