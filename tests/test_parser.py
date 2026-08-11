# A test to ensure that the parser correctly reads and validates sales records from a CSV file.

import pytest

from sales_summarizer.parser import parse_sales_record
from sales_summarizer.exceptions import InvalidRecordError

def make_valid_row(**overrides: str) -> dict[str, str]:
    row = {
        "Order ID": "B-26776",
        "Amount": "9726",
        "Profit": "1275",
        "Quantity": "5",
        "Category": "Electronics",
        "Sub-Category": "Electronic Games",
        "PaymentMode": "UPI",
        "Order Date": "2023-06-27",
        "CustomerName": "David Padilla",
        "State": "Florida",
        "City": "Miami"
    }
    row.update(overrides)
    return row

def test_parse_valid_row_returns_sales_record() -> None:
    row = make_valid_row()
    record = parse_sales_record(row)

    assert record.order_id == "B-26776"
    assert record.amount == 9726.0
    assert record.profit == 1275.0
    assert record.quantity == 5
    assert record.category == "Electronics"
    assert record.sub_category == "Electronic Games"
    assert record.payment_mode == "UPI"


#failure-case tests
def test_missing_order_id_raises() -> None:
    row = make_valid_row(**{"Order ID": ""})
    with pytest.raises(InvalidRecordError, match="Missing Order ID"):
        parse_sales_record(row)


def test_invalid_amount_raises() -> None:
    row = make_valid_row(Amount="not_a_number")
    with pytest.raises(InvalidRecordError, match="Invalid Amount"):
        parse_sales_record(row)


def test_negative_amount_raises() -> None:
    row = make_valid_row(Amount="-50")
    with pytest.raises(InvalidRecordError, match="Negative Amount"):
        parse_sales_record(row)


def test_zero_quantity_raises() -> None:
    row = make_valid_row(Quantity="0")
    with pytest.raises(InvalidRecordError, match="Non-positive Quantity"):
        parse_sales_record(row)


def test_negative_profit_is_allowed() -> None:
    row = make_valid_row(Profit="-200")
    record = parse_sales_record(row)
    assert record.profit == -200.0


def test_invalid_order_date_raises() -> None:
    row = make_valid_row(**{"Order Date": "27-06-2023"})
    with pytest.raises(InvalidRecordError, match="Invalid Order Date"):
        parse_sales_record(row)