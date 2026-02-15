import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class BinanceFuturesClient:
    """
    Binance USDT-M Futures Testnet client wrapper.
    Handles MARKET, LIMIT, and STOP (Stop-Limit) orders with logging and error handling.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("API credentials not found in .env")

        # Initialize Binance Client in TESTNET mode
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com"

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
        stop_price: float = None
    ):
        """
        Place an order on Binance Futures Testnet.

        Parameters:
        - symbol: Trading pair (e.g., BTCUSDT)
        - side: "BUY" or "SELL"
        - order_type: "MARKET", "LIMIT", or "STOP"
        - quantity: Order quantity
        - price: Required for LIMIT and STOP
        - stop_price: Required for STOP

        Returns:
        - Binance API response dict
        """

        try:
            # Base order payload
            order_data = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity
            }

            # Add price and timeInForce for LIMIT orders
            if order_type.upper() == "LIMIT":
                if price is None:
                    raise ValueError("LIMIT orders require a price")
                order_data["price"] = price
                order_data["timeInForce"] = "GTC"

            # Add price, stopPrice, and timeInForce for STOP-LIMIT orders
            elif order_type.upper() == "STOP":
                if price is None or stop_price is None:
                    raise ValueError("STOP orders require both price and stop_price")
                order_data["price"] = price
                order_data["stopPrice"] = stop_price
                order_data["timeInForce"] = "GTC"

            # MARKET order does not need price

            self.logger.info(f"Placing order: {order_data}")

            # Execute the order
            response = self.client.futures_create_order(**order_data)

            self.logger.info(f"Order response: {response}")
            return response

        except (BinanceAPIException, BinanceOrderException) as e:
            self.logger.error(f"Binance API order failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing order: {e}")
            raise
