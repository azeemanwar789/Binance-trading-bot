import argparse
from client import BinanceFuturesClient
from validators import validate_side, validate_quantity, validate_price
from logging_config import logger

def create_limit_order(client, symbol, side, quantity, price):
    # LIMIT order
    order = client.place_order(
        symbol=symbol,
        side=side,
        order_type="LIMIT",
        quantity=quantity,
        price=price  # timeInForce is handled internally
    )
    logger.info(f"Limit Order Response: {order}")
    return order

def main():
    parser = argparse.ArgumentParser(description="Place a Limit Order")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("price", type=float, help="Order price")
    args = parser.parse_args()

    try:
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, "LIMIT")
        client = BinanceFuturesClient()

        # Optional: show notional
        ticker = client.client.futures_symbol_ticker(symbol=args.symbol.upper())
        market_price = float(ticker['price'])
        notional = quantity * price
        print(f"Placing LIMIT order: {args.symbol.upper()} {side} {quantity} @ {price} (Notional: ${notional:.2f})")

        response = create_limit_order(client, args.symbol, side, quantity, price)

        print("\nOrder Response:")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        print("\n✅ Limit order placed successfully!")

    except Exception as e:
        print(f"\n❌ Limit order failed: {e}")
        logger.error(f"Limit order failed: {e}")

if __name__ == "__main__":
    main()
