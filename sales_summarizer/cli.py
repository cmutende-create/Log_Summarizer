import argparse
import csv

from sales_summarizer.exceptions import InvalidRecordError
from sales_summarizer.parser import parse_sales_record
from sales_summarizer.summarizer import SalesSummarizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize sales data from a CSV file."
    )
    parser.add_argument("csv_file", help="Path to the sales CSV file.")
    return parser.parse_args()


def load_records(csv_path: str) -> tuple[list, list]:
    valid_records = []
    errors = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_number, row in enumerate(reader, start=2):
            try:
                record = parse_sales_record(row)
                valid_records.append(record)
            except InvalidRecordError as e:
                errors.append((row_number, str(e)))

    return valid_records, errors


def main() -> None:
    args = parse_args()
    valid_records, errors = load_records(args.csv_file)

    summarizer = SalesSummarizer(valid_records)

    print(
        f"Processed {len(valid_records)} valid records "
        f"({len(errors)} skipped due to errors)\n"
    )

    print(f"Total revenue: {summarizer.total_revenue():.2f}")
    print(f"Total profit: {summarizer.total_profit():.2f}")
    print(f"Average order value: {summarizer.average_order_value():.2f}")

    print("\nRevenue by category:")
    for category, revenue in summarizer.revenue_by_category().items():
        print(f"  {category}: {revenue:.2f}")

    best = summarizer.best_selling_sub_category()
    print(f"\nBest-selling sub-category: {best}")

    if errors:
        print(f"\nSkipped rows ({len(errors)}):")
        for row_number, message in errors[:10]:
            print(f"  Row {row_number}: {message}")
        if len(errors) > 10:
            print(f"  ...and {len(errors) - 10} more")


if __name__ == "__main__":
    main()
