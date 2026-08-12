"""Aggregates SalesRecord objects into summary statistics."""

from collections import defaultdict
from sales_summarizer.models import SalesRecord


class SalesSummarizer:
    # Summary statistics
    def __init__(self, records: list[SalesRecord]) -> None:
        self.records = records

    def total_revenue(self) -> float:
        return sum(record.amount for record in self.records)

    def total_profit(self) -> float:
        return sum(record.profit for record in self.records)

    def average_order_value(self) -> float:
        if not self.records:
            return 0.0
        return self.total_revenue() / len(self.records)

    def revenue_by_category(self) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for record in self.records:
            totals[record.category] += record.amount
        return dict(totals)

    def best_selling_sub_category(self) -> str | None:
        if not self.records:
            return None

        quantities: dict[str, int] = defaultdict(int)
        for record in self.records:
            quantities[record.sub_category] += record.quantity
        return max(quantities, key=lambda sub_cat: quantities[sub_cat])
