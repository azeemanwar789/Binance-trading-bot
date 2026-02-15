import argparse
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import BinanceFuturesClient
from validators import validate_side, validate_quantity
from logging_config import logger


MIN_NOTIONAL = 100  # Minimum order value in USDT for Binance Futures


def create_market_order(client, symbol, side, quantity):
    """Place a MARKET order"""
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type="MARKET",
        quantity=quantity
    )
    logger.info(f"Market Order Response: {response}")
    return response


def main():
    parser = argparse.ArgumentParser(description="Place a Market Order")
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity")
    args = parser.parse_args()

    try:
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        client = BinanceFuturesClient()

        # Fetch current price to calculate notional
        ticker = client.client.futures_symbol_ticker(symbol=args.symbol)
        current_price = float(ticker['price'])
        notional = current_price * quantity

        if notional < MIN_NOTIONAL:
            raise ValueError(f"Order notional ${notional:.2f} is below Binance minimum of ${MIN_NOTIONAL}")

        print(f"Placing MARKET order: {args.symbol} {side} {quantity} @ {current_price} (Notional: ${notional:.2f})")
        response = create_market_order(client, args.symbol, side, quantity)

        print("\nOrder Response:")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        print("\n✅ Market order placed successfully!")

    except Exception as e:
        print(f"\n❌ Market order failed: {str(e)}")
        logger.error(f"Market order failed: {str(e)}")


if __name__ == "__main__":
    main()
