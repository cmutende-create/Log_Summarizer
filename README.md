# Sales Log Summarizer

A command-line tool that parses a sales CSV file, validates each row, and prints summary statistics: total revenue, total profit, average order value, revenue by category, and the best-selling sub-category by units sold.

Built as part of Gate 1 (A1: Idiomatic Python) of a structured Python/Django learning programme.

## Features

- Validates every row explicitly: empty fields, bad types, negative amounts, non-positive quantities, and dates outside `YYYY-MM-DD` are all rejected with a clear reason
- Rows that fail validation are skipped and reported by line number; if every row is invalid, the summary still prints zero totals and `Best-selling sub-category: None`
- Fully typed with type hints, checked with mypy
- Tested with pytest, covering happy paths and failure cases

## Requirements

- Python 3.10+
- A virtual environment (see setup below)

## Setup

```powershell
git clone <your-repo-url>
cd sales-log-summarizer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```powershell
python -m sales_summarizer.cli "data/Sales Dataset.csv"
```

Example output:
```

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
## Expected CSV columns

`Order ID, Amount, Profit, Quantity, Category, Sub-Category, PaymentMode, Order Date, CustomerName, State, City`

`Order Date` must be in `YYYY-MM-DD` format, for example `2023-06-27`.
Dates such as `6/27/2023` or `12/27/2024` are rejected and shown in the skipped rows report.

## Running tests

```powershell
pytest -v
```

## Linting and type checking

```powershell
black sales_summarizer tests
flake8 sales_summarizer tests
mypy sales_summarizer
```

## Project structure
```

sales_summarizer/

models.py       # SalesRecord dataclass

exceptions.py   # InvalidRecordError

parser.py       # parse_sales_record() — validates and converts raw CSV rows

summarizer.py   # SalesSummarizer — aggregation logic

cli.py          # argparse entry point

tests/

test_parser.py

test_summarizer.py

test_cli.py
