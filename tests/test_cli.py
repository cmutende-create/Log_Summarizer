from pathlib import Path
from sales_summarizer.cli import load_records

CSV_HEADER = (
    "Order ID,Amount,Profit,Quantity,Category,Sub-Category,"
    "PaymentMode,Order Date,CustomerName,City,State\n"
)

VALID_ROW = "B-1,100,20,2,Electronics,Phones,UPI,2024-01-01,A,TX,Austin\n"
BAD_ROW = "B-2,not_a_number,10,1,Furniture,Chairs,Cash,2024-01-02,B,NY,NYC\n"


def test_load_records_splits_valid_and_invalid(tmp_path: Path) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(CSV_HEADER + VALID_ROW + BAD_ROW)

    valid_records, errors = load_records(str(csv_file))

    assert len(valid_records) == 1
    assert valid_records[0].order_id == "B-1"

    assert len(errors) == 1
    row_number, message = errors[0]
    assert row_number == 3
    assert "Invalid Amount" in message
