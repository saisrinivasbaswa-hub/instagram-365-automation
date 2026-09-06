"""
Configuration file for Indian Stock Market Quantitative Trading & Research System.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Portfolio Starting Capital (in INR ₹)
DEFAULT_PORTFOLIO_CAPITAL = 100000.0  # ₹1,00,000 INR

# Risk Management Settings
MAX_DAILY_LOSS_PCT = 0.01  # 1.0% Hard Circuit Breaker Stop-Trade limit
RISK_PER_TRADE_PCT = 0.015  # 1.5% max account risk per trade
MIN_RISK_REWARD_RATIO = 2.0  # Minimum 1:2 Risk to Reward Ratio
MAX_OPEN_POSITIONS = 5  # Max concurrent open positions to ensure diversification

# Indian Market Universe (Top Liquid NIFTY 100 Tickers)
NSE_TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "INFY.NS",
    "BHARTIARTL.NS",
    "ITC.NS",
    "SBIN.NS",
    "LTIM.NS",
    "LT.NS",
    "TATAMOTORS.NS",
    "AXISBANK.NS",
    "KOTAKBANK.NS",
    "SUNPHARMA.NS",
    "TITAN.NS",
    "MARUTI.NS",
    "BAJFINANCE.NS",
    "M&M.NS",
    "ULTRACEMCO.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "TATASTEEL.NS",
    "COALINDIA.NS",
    "HCLTECH.NS",
    "WIPRO.NS",
]

# Ticker Display Names mapping
NSE_NAMES = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "INFY.NS": "Infosys",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ITC.NS": "ITC Limited",
    "SBIN.NS": "State Bank of India",
    "LTIM.NS": "LTIMindtree",
    "LT.NS": "Larsen & Toubro",
    "TATAMOTORS.NS": "Tata Motors",
    "AXISBANK.NS": "Axis Bank",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "SUNPHARMA.NS": "Sun Pharma",
    "TITAN.NS": "Titan Company",
    "MARUTI.NS": "Maruti Suzuki",
    "BAJFINANCE.NS": "Bajaj Finance",
    "M&M.NS": "Mahindra & Mahindra",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "NTPC.NS": "NTPC Limited",
    "POWERGRID.NS": "Power Grid Corp",
    "TATASTEEL.NS": "Tata Steel",
    "COALINDIA.NS": "Coal India",
    "HCLTECH.NS": "HCL Technologies",
    "WIPRO.NS": "Wipro Limited",
}

# Benchmark Ticker for Indian Market
BENCHMARK_TICKER = "^NSEI"  # NIFTY 50 Index
