import pandas as pd

# Load historical trades CSV
data = pd.read_csv(r"C:\Azeem's Work\azeem_binance_bot\src\Data\historical_data.csv")  # change path if needed
print(f"Columns in CSV: {data.columns.tolist()}")
print(f"Total rows loaded: {len(data)}\n")

# Optionally load Fear & Greed Index
try:
    fg = pd.read_csv(r"C:\Azeem's Work\azeem_binance_bot\src\Data\fear_greed_index.csv")  # change path if needed
    today_index = fg.iloc[-1]['value']
    print(f"Today's Fear & Greed Index: {today_index}\n")
except FileNotFoundError:
    print("Fear & Greed Index CSV not found. Continuing without it.\n")
    fg = None

# Simple backtest simulation
capital = 10000  # Starting capital in USD
position = 0     # Current coin held

for index, row in data.iterrows():
    price = row['Execution Price']      # Correct column
    size_tokens = row['Size Tokens']
    side = row['Side'].upper()

    # Optional: use Fear & Greed Index to skip buys if greed high
    if fg is not None and side == "BUY" and today_index > 70:
        continue  # Skip buy trades if market is too greedy

    if side == "BUY":
        position += size_tokens
        capital -= size_tokens * price
    elif side == "SELL":
        position -= size_tokens
        capital += size_tokens * price

# Final report
print("\n=== Backtest Summary ===")
print(f"Final USD balance: ${capital:.2f}")
print(f"Final Coin holdings: {position:.4f} coins")
if position > 0:
    print(f"Value of holdings at last price: ${position * price:.2f}")
    print(f"Total value: ${capital + position * price:.2f}")
else:
    print(f"Total value: ${capital:.2f}")
