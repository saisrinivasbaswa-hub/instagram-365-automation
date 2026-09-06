"""
FastAPI Server & REST API for Indian Stock Market Quantitative Research & Trading System.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os

from backend.research_engine import ResearchEngine
from backend.paper_trader import PaperTrader
from backend.backtester import Backtester
from config import NSE_TICKERS, NSE_NAMES

app = FastAPI(
    title="Indian Stock Market Quantitative Research & Trading System",
    description="Automated stock scanner, backtester, paper trader, and risk engine for NSE/BSE",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
research_engine = ResearchEngine()
paper_trader = PaperTrader(initial_capital=100000.0)
backtester = Backtester()

# Pydantic Request Models
class TradeRequest(BaseModel):
    ticker: str
    action: str  # BUY or SELL
    price: float
    stop_loss: float
    target_price: float
    shares: Optional[int] = None

class CloseTradeRequest(BaseModel):
    ticker: str
    exit_price: float
    reason: Optional[str] = "Manual Exit"

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Indian Stock Quant Backend API is running. Dashboard HTML coming soon."}

@app.get("/api/market_overview")
def get_market_overview():
    """Get NIFTY 50 Benchmark Overview."""
    return research_engine.get_market_overview()

@app.get("/api/scanner")
def get_scanner_signals():
    """Scan top NSE tickers and return quantitative signals."""
    try:
        signals = research_engine.scan_universe()
        return {
            "success": True,
            "total_scanned": len(signals),
            "signals": signals
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{ticker}")
def get_stock_analysis(ticker: str):
    """Get detailed analysis and technical indicators for a specific ticker."""
    analysis = research_engine.analyze_stock(ticker)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Stock data not found for {ticker}")
    return {"success": True, "analysis": analysis}

@app.get("/api/portfolio")
def get_portfolio():
    """Get paper trading portfolio summary, positions, and risk status."""
    # Refresh LTPs for open positions
    current_prices = {}
    for ticker in paper_trader.positions.keys():
        analysis = research_engine.analyze_stock(ticker, period="5d")
        if analysis:
            current_prices[ticker] = analysis['price']

    summary = paper_trader.get_portfolio_summary(current_prices=current_prices)
    return {"success": True, "portfolio": summary}

@app.post("/api/trade")
def execute_trade(req: TradeRequest):
    """Execute a paper trade (Buy/Sell)."""
    result = paper_trader.execute_paper_trade(
        ticker=req.ticker,
        action=req.action.upper(),
        price=req.price,
        stop_loss=req.stop_loss,
        target=req.target_price,
        requested_shares=req.shares
    )
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.post("/api/close_trade")
def close_trade(req: CloseTradeRequest):
    """Close an open paper position."""
    result = paper_trader.close_paper_position(
        ticker=req.ticker,
        exit_price=req.exit_price,
        reason=req.reason
    )
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.get("/api/backtest/{ticker}")
def run_backtest(ticker: str, period: str = Query("1y", pattern="^(6mo|1y|2y|5y)$")):
    """Run strategy backtest on a ticker."""
    result = backtester.run_backtest(ticker=ticker, period=period)
    if not result:
        raise HTTPException(status_code=404, detail=f"Backtest data unavailable for {ticker}")
    return {"success": True, "backtest": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
