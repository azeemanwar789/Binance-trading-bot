# src/advanced/Backtest/backtest_with_fgi.py
import pandas as pd
import os

# ======= Paths =======
HISTORICAL_CSV = r"C:\Azeem's Work\azeem_binance_bot\src\Data\historical_data.csv"
FEAR_GREED_CSV = r"C:\Azeem's Work\azeem_binance_bot\src\Data\fear_greed_index.csv"

# ======= Load historical data =======
data = pd.read_csv(HISTORICAL_CSV)
print(f"Columns in historical CSV: {data.columns.tolist()}")
print(f"Total rows loaded: {len(data)}\n")

# ======= Load Fear & Greed Index =======
fgi = None
if os.path.exists(FEAR_GREED_CSV):
    fg = pd.read_csv(FEAR_GREED_CSV)
    # dynamic column detection
    for col in fg.columns:
        if col.lower() in ['value', 'fgi', 'fear & greed index']:
            fgi = fg.iloc[-1][col]
            break
    print(f"Latest Fear & Greed Index: {fgi}\n")
else:
    print("Fear & Greed CSV not found. Continuing without it.\n")

# ======= Backtest simulation =======
capital = 10000       # starting USD
position = 0          # coins held
last_price = 0

for _, row in data.iterrows():
    price = row['Execution Price']      # column from historical CSV
    size_tokens = row['Size Tokens']
    side = row['Side'].upper()
    last_price = price

    # ======= Fear & Greed logic =======
    if fgi is not None:
        if side == "BUY":
            if fgi > 70:
                # Market too greedy → skip buy
                continue
            elif fgi < 30:
                # Market fearful → buy 50% more
                size_tokens *= 1.5

    # ======= Simulate trades =======
    if side == "BUY":
        position += size_tokens
        capital -= size_tokens * price
    elif side == "SELL":
        position -= size_tokens
        capital += size_tokens * price

# ======= Backtest Summary =======
print("\n=== Backtest Summary ===")
print(f"Final USD balance: ${capital:.2f}")
print(f"Final Coin holdings: {position:.4f} coins")
if position > 0:
    holdings_value = position * last_price
    print(f"Value of holdings at last price: ${holdings_value:.2f}")
    print(f"Total portfolio value: ${capital + holdings_value:.2f}")
else:
    print(f"Total portfolio value: ${capital:.2f}")

# Optional: simple report string for report.pdf screenshots
report = f"""
Backtest Report:
Total trades: {len(data)}
Fear & Greed Index used: {fgi if fgi is not None else 'Not used'}
Final USD balance: ${capital:.2f}
Final Coin holdings: {position:.4f}
Total portfolio value: ${capital + (position * last_price if position>0 else 0):.2f}
"""
print(report)
