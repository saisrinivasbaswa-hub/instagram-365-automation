"""
Risk Management & Circuit Breaker Engine for Indian Stock Market Quantitative Trading.
Enforces Kelly / Fixed-Fractional position sizing and daily stop-loss circuit breakers.
"""

from typing import Dict, Any, Tuple
from config import MAX_DAILY_LOSS_PCT, RISK_PER_TRADE_PCT, MIN_RISK_REWARD_RATIO, MAX_OPEN_POSITIONS

class RiskManager:
    def __init__(self, max_daily_loss_pct: float = MAX_DAILY_LOSS_PCT, risk_per_trade_pct: float = RISK_PER_TRADE_PCT):
        self.max_daily_loss_pct = max_daily_loss_pct
        self.risk_per_trade_pct = risk_per_trade_pct
        self.circuit_breaker_tripped = False
        self.circuit_breaker_reason = ""

    def evaluate_circuit_breaker(self, initial_daily_equity: float, current_total_equity: float) -> bool:
        """Evaluate whether daily loss limit has been breached."""
        if initial_daily_equity <= 0:
            return False

        daily_drawdown_pct = (initial_daily_equity - current_total_equity) / initial_daily_equity

        if daily_drawdown_pct >= self.max_daily_loss_pct:
            self.circuit_breaker_tripped = True
            self.circuit_breaker_reason = f"Daily Circuit Breaker Tripped! Daily drawdown is {daily_drawdown_pct*100:.2f}% (Limit: {self.max_daily_loss_pct*100:.2f}%). Trading halted to protect principal."
            return True
        else:
            self.circuit_breaker_tripped = False
            self.circuit_breaker_reason = "Normal Operations - Risk limits healthy."
            return False

    def calculate_position_size(
        self,
        portfolio_equity: float,
        entry_price: float,
        stop_loss_price: float,
        target_price: float,
        current_open_positions_count: int
    ) -> Tuple[bool, str, int, float]:
        """
        Calculate allowed share quantity based on portfolio risk limits.
        Returns: (is_approved, reason, allowed_shares, max_trade_value)
        """
        if self.circuit_breaker_tripped:
            return False, f"Order Rejected: {self.circuit_breaker_reason}", 0, 0.0

        if current_open_positions_count >= MAX_OPEN_POSITIONS:
            return False, f"Order Rejected: Maximum open positions limit ({MAX_OPEN_POSITIONS}) reached.", 0, 0.0

        risk_per_share = abs(entry_price - stop_loss_price)
        if risk_per_share <= 0:
            return False, "Order Rejected: Invalid stop-loss (distance to entry must be > 0).", 0, 0.0

        reward_per_share = abs(target_price - entry_price)
        risk_reward_ratio = reward_per_share / risk_per_share

        if risk_reward_ratio < MIN_RISK_REWARD_RATIO:
            return False, f"Order Rejected: Risk/Reward ratio {risk_reward_ratio:.2f} is below required minimum of {MIN_RISK_REWARD_RATIO:.1f}.", 0, 0.0

        # Account risk budget in INR ₹
        max_risk_amount = portfolio_equity * self.risk_per_trade_pct

        # Calculate max shares based on risk budget
        shares_by_risk = int(max_risk_amount / risk_per_share)

        # Cap max position value to 25% of total portfolio equity
        max_position_value = portfolio_equity * 0.25
        shares_by_capital = int(max_position_value / entry_price)

        final_shares = min(shares_by_risk, shares_by_capital)

        if final_shares <= 0:
            return False, f"Order Rejected: Insufficient capital to maintain position sizing rules for {entry_price} INR.", 0, 0.0

        trade_value = round(final_shares * entry_price, 2)
        reason = f"Approved: Allocating {final_shares} shares (₹{trade_value:.2f}) risking ₹{round(final_shares * risk_per_share, 2):.2f} ({self.risk_per_trade_pct*100:.1f}% of equity)."

        return True, reason, final_shares, trade_value
