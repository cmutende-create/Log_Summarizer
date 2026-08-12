# Sales Log Summarizer

A command-line Python project with two workflows:

- Clean a generic CSV file and write a cleaned copy.
- Summarize a sales CSV file with totals and category statistics.

The generic cleaner does not require sales-specific columns. The sales summarizer is stricter and expects a specific sales CSV schema.

Built as part of Gate 1 (A1: Idiomatic Python) of a structured Python/Django learning programme.

## Features

- Cleans generic CSV files without requiring `Order ID`, `Amount`, `Order Date`, or any other sales column.
- Normalizes common CSV issues: extra spaces, blank headers, duplicate headers, missing cells, extra cells, missing markers such as `n/a`, currency/number formatting, booleans, and common date formats.
- Writes cleaned data to a new CSV file instead of modifying the original file.
- Reports how many rows and cells were changed during cleaning.
- Validates sales rows explicitly before summarizing them.
- Skips invalid sales rows and reports the first 10 skipped row errors by line number.
- Uses type hints and is checked with mypy.
- Includes pytest coverage for the parser, summarizer, CLI loader, and cleaner.

## Requirements

- Python 3.10+
- A virtual environment is recommended.

## Setup

```powershell
git clone <your-repo-url>
cd sales-log-summarizer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Clean Any CSV

```powershell
python -m sales_summarizer.cli "data/messy.csv" --clean-output "data/cleaned.csv"
```

This mode reads any CSV file, cleans common messy values, writes the cleaned copy to the output path, prints a cleaning report, and exits.

Examples of cleanup:

- `  Amount  ` becomes `Amount`
- duplicate headers such as `Amount,Amount` become `Amount,Amount_2`
- blank headers become `column_1`, `column_2`, and so on
- `n/a`, `NULL`, `none`, and `-` become empty cells
- `$1,200.00` becomes `1200`
- `YES` and `no` become `true` and `false`
- `6/27/2023` becomes `2023-06-27`

Important limitation: the cleaner normalizes common patterns, but it does not infer a full schema for unknown datasets. For example, it will not know whether a column is required unless that rule is coded.

## Summarize A Sales CSV

```powershell
python -m sales_summarizer.cli "data/Sales_Dataset.csv"
```

The sales summary mode expects these columns:

```text
Order ID, Amount, Profit, Quantity, Category, Sub-Category, PaymentMode, Order Date, CustomerName, State, City
```

`Order Date` must already be in `YYYY-MM-DD` format, for example `2023-06-27`.
Dates such as `6/27/2023` or `12/27/2024` are rejected in summary mode. To normalize those dates first, use the cleaning mode and then summarize the cleaned CSV.

Example output:

```text
Processed 1194 valid records (0 skipped due to errors)

Total revenue: 6182639.00
Total profit: 1610697.00
Average order value: 5178.09

Revenue by category:
  Electronics: 2054456.00
  Office Supplies: 2089510.00
  Furniture: 2038673.00

Best-selling sub-category: Tables
```

If every row is invalid, the summarizer receives no valid records and prints zero totals:

```text
Total revenue: 0.00
Total profit: 0.00
Average order value: 0.00
Best-selling sub-category: None
```

## Running Tests

```powershell
pytest -v
```

## Linting And Type Checking

```powershell
black sales_summarizer tests
flake8 sales_summarizer tests
mypy sales_summarizer
```

## Project Structure

```text
sales_summarizer/
  __init__.py       # marks this folder as a Python package
  cleaner.py        # generic CSV cleaning logic
  cli.py            # command-line entry point
  exceptions.py     # custom validation exception
  models.py         # SalesRecord dataclass
  parser.py         # validates and converts sales CSV rows
  summarizer.py     # calculates sales summary statistics

tests/
  __init__.py
  test_cleaner.py
  test_cli.py
  test_parser.py
  test_summarizer.py
```

## Code Summary

For a simple mentor-friendly explanation of every file, class, and function, see [SUMMARY.md](SUMMARY.md).
