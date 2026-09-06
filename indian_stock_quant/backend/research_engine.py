"""
Quantitative Research & Technical Analysis Engine for Indian Stock Market (NSE).
Calculates RSI, MACD, EMA Crossovers, Bollinger Bands, ATR, Supertrend & Quantitative Scores.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from config import NSE_TICKERS, NSE_NAMES, BENCHMARK_TICKER

class ResearchEngine:
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}

    def fetch_stock_data(self, ticker: str, period: str = "6mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        """Fetch historical candle data from YFinance for NSE stocks."""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            if df.empty or len(df) < 30:
                return None
            df.reset_index(inplace=True)
            # Ensure standard column names
            df.rename(columns={
                'Date': 'date', 'Open': 'open', 'High': 'high',
                'Low': 'low', 'Close': 'close', 'Volume': 'volume'
            }, inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators on stock dataframe."""
        df = df.copy()

        # Exponential Moving Averages (EMA)
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

        # Relative Strength Index (RSI - 14)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df['rsi'] = 100 - (100 / (1 + rs))

        # MACD (12, 26, 9)
        ema_12 = df['close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # Bollinger Bands (20, 2 std)
        df['sma_20'] = df['close'].rolling(window=20).mean()
        std_20 = df['close'].rolling(window=20).std()
        df['bollinger_upper'] = df['sma_20'] + (std_20 * 2)
        df['bollinger_lower'] = df['sma_20'] - (std_20 * 2)

        # Average True Range (ATR - 14)
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = true_range.rolling(window=14).mean()

        # Volume Analysis
        df['vol_sma_20'] = df['volume'].rolling(window=20).mean()
        df['vol_surge'] = df['volume'] / (df['vol_sma_20'] + 1e-10)

        # Supertrend Indicator (10, factor 3)
        multiplier = 3.0
        period = 10
        hl2 = (df['high'] + df['low']) / 2.0
        df['basic_upper'] = hl2 + (multiplier * df['atr'])
        df['basic_lower'] = hl2 - (multiplier * df['atr'])

        supertrend = [True] * len(df)
        final_upper = [0.0] * len(df)
        final_lower = [0.0] * len(df)

        for i in range(1, len(df)):
            if df['basic_upper'].iloc[i] < final_upper[i-1] or df['close'].iloc[i-1] > final_upper[i-1]:
                final_upper[i] = df['basic_upper'].iloc[i]
            else:
                final_upper[i] = final_upper[i-1]

            if df['basic_lower'].iloc[i] > final_lower[i-1] or df['close'].iloc[i-1] < final_lower[i-1]:
                final_lower[i] = df['basic_lower'].iloc[i]
            else:
                final_lower[i] = final_lower[i-1]

            if supertrend[i-1] and df['close'].iloc[i] < final_lower[i]:
                supertrend[i] = False
            elif not supertrend[i-1] and df['close'].iloc[i] > final_upper[i]:
                supertrend[i] = True
            else:
                supertrend[i] = supertrend[i-1]

        df['supertrend_bullish'] = supertrend

        return df

    def analyze_stock(self, ticker: str, period: str = "6mo") -> Optional[Dict[str, Any]]:
        """Perform comprehensive quantitative analysis on a single stock."""
        df = self.fetch_stock_data(ticker, period=period)
        if df is None or len(df) < 30:
            return None

        df = self.calculate_technical_indicators(df)
        latest = df.iloc[-1]
        prev = df.iloc[-2]

        current_price = round(float(latest['close']), 2)
        atr = round(float(latest['atr']), 2) if not pd.isna(latest['atr']) else round(current_price * 0.02, 2)
        rsi = round(float(latest['rsi']), 2) if not pd.isna(latest['rsi']) else 50.0
        vol_surge = round(float(latest['vol_surge']), 2) if not pd.isna(latest['vol_surge']) else 1.0

        # Quantitative Scoring Rules (0 - 100)
        score = 50  # baseline

        # Trend alignment (+25 max)
        if latest['close'] > latest['ema_20'] > latest['ema_50']:
            score += 15
        if latest['close'] > latest['ema_200']:
            score += 10

        # Momentum (+20 max)
        if latest['macd_hist'] > 0 and latest['macd_hist'] > prev['macd_hist']:
            score += 10
        if 40 <= rsi <= 65:
            score += 10
        elif rsi < 35:
            score += 15  # Oversold reversal setup

        # Volume Surge (+15 max)
        if vol_surge > 1.5:
            score += 15
        elif vol_surge > 1.2:
            score += 8

        # Supertrend Confirmation (+10 max)
        if latest['supertrend_bullish']:
            score += 10

        score = min(100, max(0, score))

        # Determine Signal & Action
        if score >= 70:
            signal = "STRONG BUY"
            action = "BUY"
        elif score >= 58:
            signal = "BUY"
            action = "BUY"
        elif score <= 35:
            signal = "SELL / AVOID"
            action = "SELL"
        else:
            signal = "NEUTRAL"
            action = "HOLD"

        # Calculate Entry, Stop Loss & Target Price using ATR
        stop_loss_distance = max(atr * 1.5, current_price * 0.015)
        target_distance = stop_loss_distance * 2.0  # 1:2 Risk to Reward

        if action == "BUY":
            entry_price = current_price
            stop_loss = round(entry_price - stop_loss_distance, 2)
            target = round(entry_price + target_distance, 2)
        else:
            entry_price = current_price
            stop_loss = round(entry_price + stop_loss_distance, 2)
            target = round(entry_price - target_distance, 2)

        risk_reward = round(target_distance / stop_loss_distance, 2)

        name = NSE_NAMES.get(ticker, ticker.replace(".NS", ""))

        return {
            "ticker": ticker,
            "name": name,
            "price": current_price,
            "score": score,
            "signal": signal,
            "action": action,
            "rsi": rsi,
            "atr": atr,
            "volume_surge": vol_surge,
            "ema_20": round(float(latest['ema_20']), 2),
            "ema_50": round(float(latest['ema_50']), 2),
            "supertrend_bullish": bool(latest['supertrend_bullish']),
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "target_price": target,
            "risk_reward_ratio": risk_reward,
            "change_pct": round(float((latest['close'] - prev['close']) / prev['close'] * 100), 2)
        }

    def scan_universe(self) -> List[Dict[str, Any]]:
        """Scan the entire NSE universe and return scored signals sorted by score."""
        results = []
        for ticker in NSE_TICKERS:
            analysis = self.analyze_stock(ticker)
            if analysis:
                results.append(analysis)
        # Sort descending by score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def get_market_overview(self) -> Dict[str, Any]:
        """Fetch NIFTY 50 benchmark data."""
        df = self.fetch_stock_data(BENCHMARK_TICKER, period="1mo")
        if df is None or len(df) < 2:
            return {"ticker": "NIFTY 50", "price": 0.0, "change_pct": 0.0}
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        price = round(float(latest['close']), 2)
        change_pct = round(float((latest['close'] - prev['close']) / prev['close'] * 100), 2)
        return {
            "ticker": "NIFTY 50 Index",
            "symbol": "^NSEI",
            "price": price,
            "change_pct": change_pct,
            "status": "BULLISH" if change_pct >= 0 else "BEARISH"
        }
