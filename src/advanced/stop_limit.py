import argparse
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import BinanceFuturesClient
from validators import validate_side, validate_quantity, validate_price
from logging_config import logger


def create_stop_limit_order(client, symbol, side, quantity, price, stop_price):
    """Place a STOP-LIMIT order via Binance Futures"""
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type="STOP",
        quantity=quantity,
        price=price,
        stop_price=stop_price
    )
    logger.info(f"Stop-Limit Order Response: {response}")
    return response


def get_current_price(client, symbol):
    """Fetch latest market price from Binance Testnet"""
    ticker = client.client.futures_symbol_ticker(symbol=symbol)
    return float(ticker['price'])


def main():
    parser = argparse.ArgumentParser(description="Place a Stop-Limit Order safely")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("price", type=float, help="Limit price")
    parser.add_argument("stop_price", type=float, nargs='?', default=None,
                        help="Stop trigger price (optional, will auto-adjust if unsafe)")
    args = parser.parse_args()

    try:
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, "STOP")
        client = BinanceFuturesClient()

        current_price = get_current_price(client, args.symbol)
        print(f"Current market price: {current_price}")

        # Auto-adjust stop_price if missing or unsafe
        if args.stop_price is None:
            if side == "BUY":
                stop_price = current_price + 100  # safe default for testnet
            else:  # SELL
                stop_price = current_price - 100
            print(f"No stop_price provided. Using safe stop_price: {stop_price}")
        else:
            stop_price = validate_price(args.stop_price, "STOP")
            # Check against current price
            if side == "BUY" and stop_price <= current_price:
                stop_price = current_price + 100
                print(f"STOP price too low for BUY. Adjusted to: {stop_price}")
            elif side == "SELL" and stop_price >= current_price:
                stop_price = current_price - 100
                print(f"STOP price too high for SELL. Adjusted to: {stop_price}")

        print(f"Placing STOP-LIMIT order: {args.symbol} {side} {quantity} @ {price}, stop @ {stop_price}")
        response = create_stop_limit_order(client, args.symbol, side, quantity, price, stop_price)

        print("\nOrder Response:")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        print("\n✅ Stop-Limit order placed successfully!")

    except Exception as e:
        print(f"\n❌ Stop-Limit order failed: {str(e)}")
        logger.error(f"Stop-Limit order failed: {str(e)}")


if __name__ == "__main__":
    main()
