# src/advanced/sentiment_helper.py
import pandas as pd

def get_fear_greed_index(csv_path=r"C:\Azeem's Work\azeem_binance_bot\src\Data\fear_greed_index.csv"):
    """
    Returns the latest Fear & Greed index value as an integer (0-100).
    Returns None if CSV not found or column missing.
    """
    try:
        fg = pd.read_csv(csv_path)
        if 'value' in fg.columns:
            return fg.iloc[-1]['value']
        else:
            print("Fear & Greed CSV does not have 'value' column")
            return None
    except FileNotFoundError:
        print("Fear & Greed CSV not found.")
        return None
