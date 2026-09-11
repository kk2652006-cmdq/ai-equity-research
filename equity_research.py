!pip install yfinance --quiet

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# PICK YOUR COMPANY (change this ticker to any NSE stock)
# ============================================================
TICKER = 'ASIANPAINT.NS'   # Asian Paints
COMPANY_NAME = 'Asian Paints Ltd'

# ============================================================
# FETCH DATA
# ============================================================
stock = yf.Ticker(TICKER)
info = stock.info

# Price data
hist = stock.history(period='1y')
current_price = hist['Close'].iloc[-1]
price_52w_high = hist['Close'].max()
price_52w_low = hist['Close'].min()
return_1y = (current_price / hist['Close'].iloc[0] - 1) * 100

# Financials
income = stock.financials
balance = stock.balance_sheet
cashflow = stock.cashflow

# ============================================================
# EXTRACT KEY FINANCIALS
# ============================================================
def safe_get(df, keys, col_idx=0):
    """Try multiple row names, return first match"""
    for k in keys:
        if k in df.index:
            try:
                return float(df.loc[k].iloc[col_idx])
            except:
                pass
    return None

# Income statement items
revenue = safe_get(income, ['Total Revenue', 'TotalRevenue'])
net_income = safe_get(income, ['Net Income', 'NetIncome'])
ebitda = safe_get(income, ['EBITDA', 'Normalized EBITDA'])
gross_profit = safe_get(income, ['Gross Profit'])
operating_income = safe_get(income, ['Operating Income', 'EBIT'])

# Balance sheet items
total_assets = safe_get(balance, ['Total Assets'])
total_equity = safe_get(balance, ['Stockholders Equity', 'Total Stockholder Equity'])
total_debt = safe_get(balance, ['Total Debt'])
cash = safe_get(balance, ['Cash And Cash Equivalents', 'Cash'])

# Cash flow
operating_cf = safe_get(cashflow, ['Operating Cash Flow', 'Total Cash From Operating Activities'])

# ============================================================
# COMPUTE RATIOS
# ============================================================
def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return round(a / b * 100, 2)

ratios = {
    'Market Cap (₹ Cr)': round(info.get('marketCap', 0) / 1e7, 0) if info.get('marketCap') else None,
    'Current Price (₹)': round(current_price, 2),
    '52W High (₹)': round(price_52w_high, 2),
    '52W Low (₹)': round(price_52w_low, 2),
    '1Y Return (%)': round(return_1y, 2),
    'P/E Ratio': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else None,
    'P/B Ratio': round(info.get('priceToBook', 0), 2) if info.get('priceToBook') else None,
    'Dividend Yield (%)': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else None,
    'ROE (%)': pct(net_income, total_equity),
    'ROA (%)': pct(net_income, total_assets),
    'Operating Margin (%)': pct(operating_income, revenue),
    'Net Margin (%)': pct(net_income, revenue),
    'Debt/Equity': round(total_debt / total_equity, 2) if total_debt and total_equity else None,
    'Revenue (₹ Cr)': round(revenue / 1e7, 0) if revenue else None,
    'Net Income (₹ Cr)': round(net_income / 1e7, 0) if net_income else None,
}

# ============================================================
# PRINT STRUCTURED OUTPUT (for pasting into AI)
# ============================================================
print("=" * 60)
print(f"EQUITY RESEARCH DATA: {COMPANY_NAME}")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 60)

print("\n--- MARKET DATA ---")
for k in ['Current Price (₹)', '52W High (₹)', '52W Low (₹)', '1Y Return (%)', 
          'Market Cap (₹ Cr)', 'P/E Ratio', 'P/B Ratio', 'Dividend Yield (%)']:
    print(f"{k}: {ratios[k]}")

print("\n--- FINANCIAL PERFORMANCE ---")
for k in ['Revenue (₹ Cr)', 'Net Income (₹ Cr)', 'Net Margin (%)', 
          'Operating Margin (%)', 'ROE (%)', 'ROA (%)', 'Debt/Equity']:
    print(f"{k}: {ratios[k]}")

print("\n--- 1-YEAR PRICE HISTORY ---")
print(f"Start: ₹{hist['Close'].iloc[0]:.2f}")
print(f"End:   ₹{current_price:.2f}")
print(f"Change: {return_1y:.1f}%")
