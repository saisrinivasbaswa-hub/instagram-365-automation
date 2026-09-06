"""
Quantitative Strategy Backtester for Indian Stock Market (NSE).
Simulates historical entry/exit signals over 1-year and 2-year periods to compute empirical metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from backend.research_engine import ResearchEngine
from config import NSE_NAMES

class Backtester:
    def __init__(self):
        self.research_engine = ResearchEngine()

    def run_backtest(
        self,
        ticker: str,
        period: str = "1y",
        initial_capital: float = 100000.0,
        risk_per_trade_pct: float = 0.015
    ) -> Optional[Dict[str, Any]]:
        """Run quantitative backtest on a single stock using historical candle data."""
        df = self.research_engine.fetch_stock_data(ticker, period=period)
        if df is None or len(df) < 50:
            return None

        df = self.research_engine.calculate_technical_indicators(df)

        capital = initial_capital
        cash = initial_capital
        position = None  # None or dict
        trades = []
        equity_series = []

        for i in range(30, len(df)):
            row = df.iloc[i]
            prev_row = df.iloc[i-1]
            date_str = str(row['date'])[:10]
            close_price = float(row['close'])
            atr = float(row['atr']) if not pd.isna(row['atr']) else close_price * 0.02

            # Compute quantitative signal rule
            # Rule: Buy when close > EMA 20 AND RSI < 65 AND MACD Hist > 0 AND Vol Surge > 1.0
            is_buy_signal = (
                row['close'] > row['ema_20'] and
                prev_row['close'] <= prev_row['ema_20'] and
                40 <= row['rsi'] <= 65 and
                row['macd_hist'] > 0 and
                row['supertrend_bullish']
            )

            # Check exit conditions for active position
            if position is not None:
                entry_price = position['entry_price']
                stop_loss = position['stop_loss']
                target_price = position['target_price']
                shares = position['shares']

                exit_trade = False
                exit_price = close_price
                exit_reason = ""

                # Stop Loss hit
                if row['low'] <= stop_loss:
                    exit_trade = True
                    exit_price = stop_loss
                    exit_reason = "Stop Loss Hit"
                # Target hit
                elif row['high'] >= target_price:
                    exit_trade = True
                    exit_price = target_price
                    exit_reason = "Target Hit"
                # Bearish reversal exit
                elif not row['supertrend_bullish'] or row['rsi'] > 75:
                    exit_trade = True
                    exit_price = close_price
                    exit_reason = "Signal Reversal / Overbought"

                if exit_trade:
                    pnl = (exit_price - entry_price) * shares
                    cash += (shares * exit_price)
                    pnl_pct = (pnl / (shares * entry_price)) * 100

                    trades.append({
                        "entry_date": position['entry_date'],
                        "exit_date": date_str,
                        "entry_price": round(entry_price, 2),
                        "exit_price": round(exit_price, 2),
                        "shares": shares,
                        "pnl": round(pnl, 2),
                        "pnl_pct": round(pnl_pct, 2),
                        "reason": exit_reason
                    })
                    position = None

            # Check new entry condition
            elif is_buy_signal and position is None:
                stop_dist = max(atr * 1.5, close_price * 0.015)
                stop_loss = close_price - stop_dist
                target_price = close_price + (stop_dist * 2.0)  # 1:2 Risk/Reward

                risk_per_share = stop_dist
                max_risk = cash * risk_per_trade_pct
                shares = int(max_risk / risk_per_share)
                cost = shares * close_price

                if shares > 0 and cash >= cost:
                    cash -= cost
                    position = {
                        "entry_date": date_str,
                        "entry_price": close_price,
                        "shares": shares,
                        "stop_loss": stop_loss,
                        "target_price": target_price
                    }

            # Update daily portfolio equity
            curr_pos_val = (position['shares'] * close_price) if position else 0.0
            daily_equity = round(cash + curr_pos_val, 2)
            equity_series.append({"date": date_str, "equity": daily_equity, "price": close_price})

        # Close open position at end of backtest period if any
        if position is not None:
            last_close = float(df.iloc[-1]['close'])
            pnl = (last_close - position['entry_price']) * position['shares']
            cash += (position['shares'] * last_close)
            trades.append({
                "entry_date": position['entry_date'],
                "exit_date": str(df.iloc[-1]['date'])[:10],
                "entry_price": round(position['entry_price'], 2),
                "exit_price": round(last_close, 2),
                "shares": position['shares'],
                "pnl": round(pnl, 2),
                "pnl_pct": round((pnl / (position['shares'] * position['entry_price'])) * 100, 2),
                "reason": "Period End Close"
            })

        # Calculate metrics
        final_equity = equity_series[-1]['equity'] if equity_series else initial_capital
        total_return_pct = round(((final_equity - initial_capital) / initial_capital) * 100, 2)

        # Benchmark return (Buy & Hold)
        start_price = float(df.iloc[30]['close'])
        end_price = float(df.iloc[-1]['close'])
        benchmark_return_pct = round(((end_price - start_price) / start_price) * 100, 2)

        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]

        win_rate = round((len(winning_trades) / len(trades) * 100), 1) if trades else 0.0

        gross_profit = sum(t['pnl'] for t in winning_trades)
        gross_loss = abs(sum(t['pnl'] for t in losing_trades))
        profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else (99.99 if gross_profit > 0 else 0.0)

        # Calculate Max Drawdown
        peak = initial_capital
        max_drawdown_pct = 0.0
        for pt in equity_series:
            eq = pt['equity']
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak
            if dd > max_drawdown_pct:
                max_drawdown_pct = dd

        name = NSE_NAMES.get(ticker, ticker.replace(".NS", ""))

        return {
            "ticker": ticker,
            "name": name,
            "period": period,
            "initial_capital": initial_capital,
            "final_equity": final_equity,
            "total_return_pct": total_return_pct,
            "benchmark_return_pct": benchmark_return_pct,
            "total_trades": len(trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate_pct": win_rate,
            "profit_factor": profit_factor,
            "max_drawdown_pct": round(max_drawdown_pct * 100, 2),
            "trades": trades,
            "equity_curve": equity_series[::3]  # sample points for lightweight charting
        }
