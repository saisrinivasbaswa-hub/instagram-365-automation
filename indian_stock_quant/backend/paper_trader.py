"""
Virtual Paper Trading Broker & Portfolio Ledger for Indian Stock Market (NSE).
Tracks virtual balance, open holdings, unrealized/realized PnL (₹), and execution history.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from config import DEFAULT_PORTFOLIO_CAPITAL, NSE_NAMES
from backend.risk_manager import RiskManager

class PaperTrader:
    def __init__(self, initial_capital: float = DEFAULT_PORTFOLIO_CAPITAL):
        self.initial_capital = initial_capital
        self.cash_balance = initial_capital
        self.initial_daily_equity = initial_capital
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.trade_history: List[Dict[str, Any]] = []
        self.risk_manager = RiskManager()
        self.equity_curve: List[Dict[str, Any]] = [
            {"timestamp": datetime.now().strftime("%H:%M:%S"), "equity": initial_capital}
        ]

    def get_portfolio_summary(self, current_prices: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Calculate total portfolio equity, cash, unrealized & realized PnL."""
        unrealized_pnl = 0.0

        for ticker, pos in self.positions.items():
            current_price = current_prices.get(ticker, pos['entry_price']) if current_prices else pos['entry_price']
            pos['current_price'] = current_price
            if pos['action'] == "BUY":
                pnl = (current_price - pos['entry_price']) * pos['shares']
            else:
                pnl = (pos['entry_price'] - current_price) * pos['shares']
            pos['unrealized_pnl'] = round(pnl, 2)
            pos['pnl_pct'] = round((pnl / (pos['entry_price'] * pos['shares'])) * 100, 2)
            unrealized_pnl += pnl

        total_equity = round(self.cash_balance + sum(p['shares'] * p['current_price'] for p in self.positions.values()), 2)
        total_realized_pnl = sum(t['realized_pnl'] for t in self.trade_history)
        total_pnl = round(total_equity - self.initial_capital, 2)
        total_pnl_pct = round((total_pnl / self.initial_capital) * 100, 2)

        # Check risk engine circuit breaker
        self.risk_manager.evaluate_circuit_breaker(self.initial_daily_equity, total_equity)

        # Win rate calculation
        closed_trades = [t for t in self.trade_history if t['type'] == "CLOSE"]
        winning_trades = [t for t in closed_trades if t['realized_pnl'] > 0]
        win_rate = round((len(winning_trades) / len(closed_trades) * 100), 1) if closed_trades else 0.0

        return {
            "initial_capital": self.initial_capital,
            "cash_balance": round(self.cash_balance, 2),
            "total_equity": total_equity,
            "unrealized_pnl": round(unrealized_pnl, 2),
            "realized_pnl": round(total_realized_pnl, 2),
            "total_pnl": total_pnl,
            "total_pnl_pct": total_pnl_pct,
            "win_rate_pct": win_rate,
            "total_trades": len(closed_trades),
            "active_positions_count": len(self.positions),
            "circuit_breaker_tripped": self.risk_manager.circuit_breaker_tripped,
            "circuit_breaker_reason": self.risk_manager.circuit_breaker_reason,
            "positions": list(self.positions.values()),
            "trade_history": self.trade_history[-10:]  # latest 10 trades
        }

    def execute_paper_trade(
        self,
        ticker: str,
        action: str,
        price: float,
        stop_loss: float,
        target: float,
        requested_shares: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute a virtual buy or sell paper trade with risk validation."""
        summary = self.get_portfolio_summary()
        current_equity = summary['total_equity']

        if ticker in self.positions:
            return {"success": False, "message": f"Already holding an active position in {ticker}."}

        # Risk Manager validation & position sizing
        approved, reason, allowed_shares, trade_value = self.risk_manager.calculate_position_size(
            portfolio_equity=current_equity,
            entry_price=price,
            stop_loss_price=stop_loss,
            target_price=target,
            current_open_positions_count=len(self.positions)
        )

        if not approved:
            return {"success": False, "message": reason}

        shares = requested_shares if (requested_shares and requested_shares <= allowed_shares) else allowed_shares

        if self.cash_balance < (shares * price):
            return {"success": False, "message": f"Insufficient cash balance (₹{self.cash_balance:.2f}) for trade value ₹{(shares * price):.2f}."}

        # Deduct cash and record position
        cost = shares * price
        self.cash_balance -= cost

        name = NSE_NAMES.get(ticker, ticker.replace(".NS", ""))

        position = {
            "ticker": ticker,
            "name": name,
            "action": action,
            "shares": shares,
            "entry_price": price,
            "current_price": price,
            "stop_loss": stop_loss,
            "target_price": target,
            "trade_value": round(cost, 2),
            "unrealized_pnl": 0.0,
            "pnl_pct": 0.0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.positions[ticker] = position

        trade_event = {
            "id": f"TRD-{len(self.trade_history)+1:04d}",
            "ticker": ticker,
            "name": name,
            "type": "OPEN",
            "action": action,
            "shares": shares,
            "price": price,
            "trade_value": round(cost, 2),
            "realized_pnl": 0.0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.trade_history.append(trade_event)

        # Log equity point
        self.equity_curve.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "equity": round(self.cash_balance + cost, 2)
        })

        return {
            "success": True,
            "message": f"Successfully executed PAPER {action} for {shares} shares of {name} at ₹{price:.2f}.",
            "position": position
        }

    def close_paper_position(self, ticker: str, exit_price: float, reason: str = "Manual Exit") -> Dict[str, Any]:
        """Close an active paper trading position."""
        if ticker not in self.positions:
            return {"success": False, "message": f"No active position found for {ticker}."}

        pos = self.positions.pop(ticker)
        shares = pos['shares']
        entry_price = pos['entry_price']

        if pos['action'] == "BUY":
            realized_pnl = (exit_price - entry_price) * shares
        else:
            realized_pnl = (entry_price - exit_price) * shares

        return_capital = (shares * entry_price) + realized_pnl
        self.cash_balance += return_capital

        trade_event = {
            "id": f"TRD-{len(self.trade_history)+1:04d}",
            "ticker": ticker,
            "name": pos['name'],
            "type": "CLOSE",
            "action": "SELL" if pos['action'] == "BUY" else "COVER",
            "shares": shares,
            "price": exit_price,
            "trade_value": round(shares * exit_price, 2),
            "realized_pnl": round(realized_pnl, 2),
            "close_reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.trade_history.append(trade_event)

        # Log equity point
        summary = self.get_portfolio_summary()
        self.equity_curve.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "equity": summary['total_equity']
        })

        return {
            "success": True,
            "message": f"Closed position in {pos['name']} at ₹{exit_price:.2f}. Realized PnL: ₹{realized_pnl:+.2f}.",
            "realized_pnl": round(realized_pnl, 2)
        }
