# AI-Powered Equity Research Pipeline

Python pipeline that pulls NSE data, computes 15+ financial ratios, and uses AI to generate first-draft equity research notes.

## What it does
1. Pulls live data from Yahoo Finance (price, financials, ratios)
2. Computes 15+ key metrics (ROE, margins, D/E, valuation)
3. Feeds structured data to an LLM to generate a research note
4. Outputs a clean 1-page PDF

## Tools
Python | yfinance | pandas | Claude/ChatGPT

## Sample Output
Asian Paints Ltd — HOLD, Target ₹2,650–2,850

## How to use
1. Open the script in Google Colab
2. Change TICKER to any NSE stock
3. Run → paste output into the AI prompt
4. Format as PDF

## What I learned
- Time saved: ~3 hours → 10 minutes for a first draft
- AI is good at structure and speed, not judgment
- Human review remains essential for accuracy

## Author
[Kumaran B] | MBA-BF
