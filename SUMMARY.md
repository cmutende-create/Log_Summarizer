# Project Code Summary

This file explains the project in simple language so you can walk through it with your mentor.

## Big Picture

The project has two main jobs:

- Clean any CSV file and save a cleaner copy.
- Summarize a sales CSV file after validating its rows.

The cleaner is general. The summarizer is sales-specific.

## `sales_summarizer/cleaner.py`

This file cleans generic CSV files. It does not need sales columns.

### `MISSING_VALUES`

A set of values that mean "missing data".

Examples:

- empty string
- `na`
- `n/a`
- `none`
- `null`
- `-`

When the cleaner sees one of these, it turns the cell into an empty value.

### `DATE_FORMATS`

A list of date formats the cleaner understands.

Examples:

- `2023-06-27`
- `6/27/2023`
- `27/06/2023`

If a cell matches one of these formats, the cleaner converts it to `YYYY-MM-DD`.

### `CleaningReport`

A dataclass that stores the cleaning results.

It tracks:

- how many rows were read
- how many rows were written
- how many blank rows were skipped
- how many missing cells were filled
- how many extra cells were dropped
- how many cells were changed
- which headers were renamed

This is useful because the program can tell the user what happened during cleaning.

### `clean_csv(input_path, output_path)`

This is the main cleaner function.

How it works:

1. Opens the original CSV file.
2. Reads the header row.
3. Cleans the headers.
4. Reads each data row.
5. Skips rows that are completely blank.
6. Cleans each row.
7. Writes the cleaned data to a new CSV file.
8. Returns a `CleaningReport`.

### `clean_headers(headers, report)`

This cleans the column names.

It:

- removes extra spaces
- fills blank headers with names like `column_1`
- renames duplicate headers, for example `Amount` and `Amount_2`
- stores renamed headers in the report

### `clean_row(row, expected_cells, report)`

This makes sure each row has the same number of cells as the header.

If a row has too many cells, extra cells are removed.
If a row has too few cells, empty cells are added.
Then each cell is cleaned with `clean_cell()`.

### `clean_cell(value, report)`

This cleans one cell.

It:

- removes extra spaces
- turns missing values into empty cells
- normalizes booleans
- normalizes numbers
- normalizes dates
- updates the report if the cell changed

### `normalize_boolean(value)`

This converts boolean-like text into a standard format.

Examples:

- `yes` becomes `true`
- `y` becomes `true`
- `no` becomes `false`
- `n` becomes `false`

### `normalize_number(value)`

This cleans number-like values.

Examples:

- `$1,200.00` becomes `1200`
- `42.50` becomes `42.5`

If the value is not a number, it is left unchanged.

### `normalize_date(value)`

This tries to convert a date into `YYYY-MM-DD`.

If the value matches one of the known date formats, it is converted.
If it does not match, it is left unchanged.

## `sales_summarizer/cli.py`

This file controls the command-line program.

### `parse_args()`

This reads the command-line arguments.

It expects:

- `csv_file`: the input CSV file
- `--clean-output`: optional output path for cleaned CSV mode

If `--clean-output` is given, the program cleans a CSV.
If it is not given, the program summarizes a sales CSV.

### `load_records(csv_path)`

This is used by the sales summary mode.

How it works:

1. Opens the CSV file.
2. Reads each row as a dictionary.
3. Sends each row to `parse_sales_record()`.
4. Stores valid rows in `valid_records`.
5. Stores invalid row errors in `errors`.
6. Returns both lists.

This lets the program continue even when some rows are invalid.

### `main()`

This is the main function that runs the program.

If cleaning mode is used:

- it calls `clean_csv()`
- prints the cleaning report
- exits

If sales summary mode is used:

- it loads valid sales records
- creates a `SalesSummarizer`
- prints total revenue, total profit, average order value, revenue by category, and best-selling sub-category
- prints skipped row errors

## `sales_summarizer/parser.py`

This file validates one sales row and converts it into a `SalesRecord`.

### `parse_sales_record(row)`

This function receives one CSV row as a dictionary.

It checks:

- `Order ID` is not empty
- `Amount` is a valid number
- `Amount` is not negative
- `Profit` is a valid number
- `Quantity` is a valid integer
- `Quantity` is greater than zero
- `Category` is not empty
- `Sub-Category` is not empty
- `Order Date` is in `YYYY-MM-DD` format

If something is wrong, it raises `InvalidRecordError`.

If everything is valid, it returns a `SalesRecord`.

Important detail: negative profit is allowed because a sale can make a loss.

## `sales_summarizer/summarizer.py`

This file calculates sales statistics from valid records.

### `SalesSummarizer`

This class receives a list of `SalesRecord` objects and calculates summary values.

### `__init__(records)`

Stores the list of records in `self.records`.

### `total_revenue()`

Adds all `amount` values together.

### `total_profit()`

Adds all `profit` values together.

### `average_order_value()`

Divides total revenue by the number of valid records.

If there are no records, it returns `0.0` so the program does not crash from division by zero.

### `revenue_by_category()`

Groups sales by category and totals the revenue for each category.

Example result:

```python
{"Electronics": 150.0, "Furniture": 200.0}
```

### `best_selling_sub_category()`

Adds up quantities by sub-category.

It returns the sub-category with the highest total quantity sold.
If there are no records, it returns `None`.

## `sales_summarizer/models.py`

This file contains the data model for one valid sales row.

### `SalesRecord`

A dataclass that represents one validated sales record.

It has these fields:

- `order_id`
- `amount`
- `profit`
- `quantity`
- `category`
- `sub_category`
- `payment_mode`
- `order_date`
- `customer_name`
- `state`
- `city`

The dataclass is frozen, which means the values cannot be changed after the record is created.

## `sales_summarizer/exceptions.py`

This file contains the custom error used by the parser.

### `InvalidRecordError`

This exception is raised when a sales row is invalid.

The CLI catches this error, records the row number, and continues processing the rest of the file.

## `sales_summarizer/__init__.py`

This file is empty.

It marks `sales_summarizer` as a Python package so files can import from it.

## `tests/test_cleaner.py`

This file tests the generic CSV cleaner.

### `read_csv(path)`

A helper function that reads a CSV file and returns its rows as a list.

### `test_clean_csv_normalizes_common_csv_errors(tmp_path)`

Tests that the cleaner:

- fixes messy headers
- skips blank rows
- fills missing cells
- drops extra cells
- normalizes numbers
- normalizes dates
- normalizes booleans
- returns the correct report counts

## `tests/test_cli.py`

This file tests the CSV loading logic used by the CLI.

### `test_load_records_splits_valid_and_invalid(tmp_path)`

Creates a temporary CSV with:

- one valid row
- one invalid row

Then it checks that `load_records()` returns one valid record and one error.

## `tests/test_parser.py`

This file tests the sales row parser.

### `make_valid_row(**overrides)`

A helper that creates a valid row for tests.

Tests can override one field to make the row invalid.

### `test_parse_valid_row_returns_sales_record()`

Checks that a valid row becomes a `SalesRecord`.

### `test_missing_order_id_raises()`

Checks that a missing order ID is rejected.

### `test_invalid_amount_raises()`

Checks that a non-number amount is rejected.

### `test_negative_amount_raises()`

Checks that a negative amount is rejected.

### `test_zero_quantity_raises()`

Checks that quantity must be greater than zero.

### `test_negative_profit_is_allowed()`

Checks that negative profit is allowed.

### `test_invalid_order_date_raises()`

Checks that an invalid date format is rejected.

## `tests/test_summarizer.py`

This file tests the sales summary calculations.

### `make_records()`

Creates sample `SalesRecord` objects for the tests.

### `test_total_revenue()`

Checks that total revenue is calculated correctly.

### `test_total_profit()`

Checks that total profit is calculated correctly.

### `test_average_order_value()`

Checks that average order value is calculated correctly.

### `test_revenue_by_value_empty()`

Checks that average order value is `0.0` when there are no records.

### `test_revenue_by_category()`

Checks that revenue is grouped correctly by category.

### `test_best_selling_sub_category()`

Checks that the highest-selling sub-category is returned.

### `test_best_selling_sub_category_empty()`

Checks that the result is `None` when there are no records.
