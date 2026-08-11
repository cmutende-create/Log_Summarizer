# Tests for SalesSummarizer
from datetime import date
from sales_summarizer.models import SalesRecord
from sales_summarizer.summarizer import SalesSummarizer
import pytest


def make_records() -> list[SalesRecord]:
    return [
        SalesRecord(
            "B-1",
            100.0,
            20.0,
            2,
            "Electronics",
            "Phones",
            "UPI",
            date(2024, 1, 1),
            "A",
            "TX",
            "Austin",
        ),
        SalesRecord(
            "B-2",
            200.0,
            40.0,
            10,
            "Furniture",
            "Chairs",
            "Cash",
            date(2024, 1, 2),
            "B",
            "NY",
            "NYC",
        ),
        SalesRecord(
            "B-3",
            50.0,
            10.0,
            3,
            "Electronics",
            "Cables",
            "UPI",
            date(2024, 1, 3),
            "C",
            "CA",
            "LA",
        ),
    ]


def test_total_revenue() -> None:
    summarizer = SalesSummarizer(make_records())
    assert summarizer.total_revenue() == 350.0


def test_total_profit() -> None:
    summarizer = SalesSummarizer(make_records())
    assert summarizer.total_profit() == 70.0


def test_average_order_value() -> None:
    summarizer = SalesSummarizer(make_records())
    assert summarizer.average_order_value() == pytest.approx(116.67, rel=1e-2)


def test_revenue_by_value_empty() -> None:
    summarizer = SalesSummarizer([])
    assert summarizer.average_order_value() == 0.0


def test_revenue_by_category() -> None:
    summarizer = SalesSummarizer(make_records())
    result = summarizer.revenue_by_category()
    assert result == {"Electronics": 150.0, "Furniture": 200.0}


def test_best_selling_sub_category() -> None:
    summarizer = SalesSummarizer(make_records())
    assert summarizer.best_selling_sub_category() == "Chairs"


def test_best_selling_sub_category_empty() -> None:
    summarizer = SalesSummarizer([])
    assert summarizer.best_selling_sub_category() is None
