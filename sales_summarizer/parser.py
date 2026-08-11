# imports and functions signature
from datetime import datetime, date

from sales_summarizer.models import SalesRecord
from sales_summarizer.exceptions import InvalidRecordError

def parse_sales_record(row: dict[str, str]) -> SalesRecord:
    order_id = row.get("Order ID", "").strip() 
    #checks order id is not empty
    if not order_id:
        raise InvalidRecordError("Missing Order ID")

    #checks amount is valid
    try:
        amount =float(row.get("Amount", ""))
    except ValueError:
        raise InvalidRecordError(f"Invalid Amount: {row.get('Amount')}")

    if amount < 0:
        raise InvalidRecordError(f"Negative Amount: {amount}")

    #checks profit is valid
    try:
        profit = float(row.get("Profit", ""))
    except ValueError:
        raise InvalidRecordError(f"Invalid Profit: {row.get('Profit')}")
    
    #checks quantity is valid
    try: 
        quantity = int(row.get("Quantity", ""))
    except ValueError:
        raise InvalidRecordError(f"Invalid Quantity: {row.get('Quantity')}")
    if quantity <= 0:
        raise InvalidRecordError(f"Non-positive Quantity: {quantity}")

    category = row.get("Category", "").strip()
    if not category:
        raise InvalidRecordError("Missing Category")

    sub_category = row.get("Sub-Category", "").strip()
    if not sub_category:
        raise InvalidRecordError("Missing Sub-Category")
    
    payment_mode = row.get("PaymentMode", "").strip()
    customer_name = row.get("CustomerName", "").strip()
    state = row.get("State", "").strip()
    city = row.get("City", "").strip()

    order_date_str = row.get("Order Date", "").strip()
    try:
        order_date = datetime.strptime(order_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidRecordError(f"Invalid Order Date: {order_date_str}")

    return SalesRecord(
        order_id=order_id,
        amount=amount,
        profit=profit,
        quantity=quantity,
        category=category,
        sub_category=sub_category,
        payment_mode=payment_mode,
        order_date=order_date,
        customer_name=customer_name,
        state=state,
        city=city
    )
    """Validate and convert a raw CSV row into a SalesRecord.

    Raises InvalidRecordError if any field fails validation.
    """