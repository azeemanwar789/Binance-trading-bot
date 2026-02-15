def validate_side(side: str):
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side

def validate_order_type(order_type: str):
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT", "STOP"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP")
    return order_type

def validate_quantity(quantity: float):
    if quantity is None or quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    return quantity

def validate_price(price: float, order_type: str = None):
    """
    LIMIT and STOP require price; MARKET does not.
    """
    if order_type in ["LIMIT", "STOP"]:
        if price is None or price <= 0:
            raise ValueError(f"Price must be >0 for {order_type} orders")
    return price
