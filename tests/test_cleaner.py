import csv
from pathlib import Path

from sales_summarizer.cleaner import clean_csv


def read_csv(path: Path) -> list[list[str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def test_clean_csv_normalizes_common_csv_errors(tmp_path: Path) -> None:
    source = tmp_path / "dirty.csv"
    target = tmp_path / "clean.csv"
    source.write_text(
        " Name ,Amount,Amount,,Date,Active\n"
        ' Alice ,"$1,200.00",n/a,extra,6/27/2023,YES\n'
        "\n"
        " Bob ,42.50\n"
        " Carol ,10,20,30,2024-01-03,no,ignored\n",
        encoding="utf-8",
    )

    report = clean_csv(source, target)

    assert read_csv(target) == [
        ["Name", "Amount", "Amount_2", "column_4", "Date", "Active"],
        ["Alice", "1200", "", "extra", "2023-06-27", "true"],
        ["Bob", "42.5", "", "", "", ""],
        ["Carol", "10", "20", "30", "2024-01-03", "false"],
    ]
    assert report.input_rows == 4
    assert report.output_rows == 3
    assert report.skipped_blank_rows == 1
    assert report.missing_values_found == 5
    assert report.missing_cells_filled == 4
    assert report.extra_cells_dropped == 1
    assert report.normalized_cells > 0
    assert "' Name ' -> 'Name'" in report.renamed_headers
    assert "'' -> 'column_4'" in report.renamed_headers
