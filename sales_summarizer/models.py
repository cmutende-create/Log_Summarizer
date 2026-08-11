#Data models for the sales log summarizer.

from dataclasses import dataclass #autogenerates fields declared eg __init__
from datetime import date

@dataclass(frozen=True) #makes instances immutable after creation eg you cant do record.amount = 99 later
class SalesRecord:
    """ A single validated row from the sales CSV. """
    order_id: str 
    amount: float
    profit: float
    quantity: int
    category: str
    sub_category: str
    payment_mode: str
    order_date: date
    customer_name: str
    state: str
    city: str

    