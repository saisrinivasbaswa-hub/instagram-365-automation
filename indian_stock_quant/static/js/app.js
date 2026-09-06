// QuantIndia Dashboard Application Logic
document.addEventListener('DOMContentLoaded', () => {
  // Global State
  let scannerData = [];
  let currentFilter = 'ALL';
  let backtestChartInstance = null;

  // DOM Elements
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const btnRefreshScanner = document.getElementById('btnRefreshScanner');
  const filterChips = document.querySelectorAll('.filter-chip');
  const scannerTableBody = document.getElementById('scannerTableBody');
  const niftyPrice = document.getElementById('niftyPrice');
  const niftyBadge = document.getElementById('niftyBadge');
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('statusText');

  // Portfolio DOM Elements
  const valTotalEquity = document.getElementById('valTotalEquity');
  const valTotalPnlPct = document.getElementById('valTotalPnlPct');
  const valCashBalance = document.getElementById('valCashBalance');
  const valRealizedPnl = document.getElementById('valRealizedPnl');
  const valWinRate = document.getElementById('valWinRate');
  const valCircuitReason = document.getElementById('valCircuitReason');
  const holdingsTableBody = document.getElementById('holdingsTableBody');
  const historyTableBody = document.getElementById('historyTableBody');
  const activeCount = document.getElementById('activeCount');

  // Backtest DOM Elements
  const btnRunBacktest = document.getElementById('btnRunBacktest');
  const backtestTicker = document.getElementById('backtestTicker');
  const backtestPeriod = document.getElementById('backtestPeriod');
  const backtestResults = document.getElementById('backtestResults');

  // Tab Navigation Handler
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));
      
      btn.classList.add('active');
      const tabId = btn.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');

      if (tabId === 'portfolio-tab') {
        loadPortfolio();
      }
    });
  });

  // Filter Chips Handler
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.getAttribute('data-filter');
      renderScannerTable();
    });
  });

  // Initial Load
  loadMarketOverview();
  loadScannerSignals();
  loadPortfolio();

  btnRefreshScanner.addEventListener('click', loadScannerSignals);
  btnRunBacktest.addEventListener('click', runBacktest);

  // 1. Fetch NIFTY 50 Benchmark Overview
  async function loadMarketOverview() {
    try {
      const res = await fetch('/api/market_overview');
      const data = await res.json();
      if (data.price) {
        niftyPrice.textContent = `₹${data.price.toLocaleString('en-IN')}`;
        const isBullish = data.change_pct >= 0;
        niftyBadge.textContent = `${isBullish ? '+' : ''}${data.change_pct}%`;
        niftyBadge.className = `ticker-badge ${isBullish ? 'green' : 'red'}`;
      }
    } catch (err) {
      console.error('Market overview fetch failed:', err);
    }
  }

  // 2. Fetch Scanner Signals
  async function loadScannerSignals() {
    scannerTableBody.innerHTML = `<tr><td colspan="10" class="loading-cell">Scanning NSE stocks... Please wait...</td></tr>`;
    try {
      const res = await fetch('/api/scanner');
      const data = await res.json();
      if (data.success) {
        scannerData = data.signals;
        renderScannerTable();
      }
    } catch (err) {
      scannerTableBody.innerHTML = `<tr><td colspan="10" class="loading-cell red-text">Failed to scan market data. Please ensure backend is running.</td></tr>`;
    }
  }

  // 3. Render Scanner Table
  function renderScannerTable() {
    let filtered = scannerData;
    if (currentFilter !== 'ALL') {
      filtered = scannerData.filter(s => s.action === currentFilter || s.signal === currentFilter);
    }

    if (filtered.length === 0) {
      scannerTableBody.innerHTML = `<tr><td colspan="10" class="loading-cell">No stock signals matching filter "${currentFilter}".</td></tr>`;
      return;
    }

    scannerTableBody.innerHTML = filtered.map(s => {
      let badgeClass = 'hold';
      if (s.signal === 'STRONG BUY') badgeClass = 'strong-buy';
      else if (s.signal === 'BUY') badgeClass = 'buy';
      else if (s.signal.includes('SELL')) badgeClass = 'sell';

      const changeClass = s.change_pct >= 0 ? 'green-text' : 'red-text';
      const changePrefix = s.change_pct >= 0 ? '+' : '';

      return `
        <tr>
          <td>
            <strong>${s.name}</strong><br>
            <small class="text-muted">${s.ticker}</small>
          </td>
          <td><strong>₹${s.price.toLocaleString('en-IN')}</strong></td>
          <td class="${changeClass}">${changePrefix}${s.change_pct}%</td>
          <td>
            <div style="font-weight: 700; color: ${s.score >= 70 ? '#10b981' : s.score >= 50 ? '#06b6d4' : '#ef4444'}">
              ${s.score}/100
            </div>
          </td>
          <td><span class="badge ${badgeClass}">${s.signal}</span></td>
          <td>${s.rsi}</td>
          <td>${s.volume_surge}x</td>
          <td>
            <small>Entry: ₹${s.entry_price}</small><br>
            <small class="red-text">SL: ₹${s.stop_loss}</small> | 
            <small class="green-text">TGT: ₹${s.target_price}</small>
          </td>
          <td><strong>${s.risk_reward_ratio}:1</strong></td>
          <td>
            ${s.action === 'BUY' ? `
              <button class="btn success btn-sm" onclick="executePaperTrade('${s.ticker}', 'BUY', ${s.price}, ${s.stop_loss}, ${s.target_price})">
                Paper Buy
              </button>
            ` : `<button class="btn danger btn-sm" disabled>Avoid</button>`}
          </td>
        </tr>
      `;
    }).join('');
  }

  // 4. Execute Paper Trade Handler
  window.executePaperTrade = async function(ticker, action, price, stopLoss, targetPrice) {
    try {
      const res = await fetch('/api/trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker: ticker,
          action: action,
          price: price,
          stop_loss: stopLoss,
          target_price: targetPrice
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        alert(data.message);
        loadPortfolio();
      } else {
        alert(`Trade Rejected: ${data.detail || data.message}`);
      }
    } catch (err) {
      alert(`Error executing trade: ${err.message}`);
    }
  };

  // 5. Load Paper Trading Portfolio
  async function loadPortfolio() {
    try {
      const res = await fetch('/api/portfolio');
      const data = await res.json();
      if (data.success) {
        const p = data.portfolio;

        // Metric Cards
        valTotalEquity.textContent = `₹${p.total_equity.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        valTotalPnlPct.textContent = `${p.total_pnl_pct >= 0 ? '+' : ''}${p.total_pnl_pct}% (₹${p.total_pnl.toLocaleString('en-IN')})`;
        valTotalPnlPct.className = `metric-sub ${p.total_pnl >= 0 ? 'green-text' : 'red-text'}`;

        valCashBalance.textContent = `₹${p.cash_balance.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        valRealizedPnl.textContent = `₹${p.realized_pnl.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        valRealizedPnl.className = `metric-value ${p.realized_pnl >= 0 ? 'green-text' : 'red-text'}`;
        valWinRate.textContent = `Win Rate: ${p.win_rate_pct}% (${p.total_trades} Trades)`;

        activeCount.textContent = p.active_positions_count;

        // Circuit Breaker widget
        if (p.circuit_breaker_tripped) {
          statusDot.className = 'status-dot red';
          statusText.textContent = 'CIRCUIT BREAKER TRIPPED';
          valCircuitReason.textContent = p.circuit_breaker_reason;
          valCircuitReason.className = 'metric-sub red-text';
        } else {
          statusDot.className = 'status-dot green';
          statusText.textContent = 'Risk Engine Active';
          valCircuitReason.textContent = 'Normal Operations - Risk limits healthy.';
          valCircuitReason.className = 'metric-sub green-text';
        }

        // Active Holdings Table
        if (p.positions.length === 0) {
          holdingsTableBody.innerHTML = `<tr><td colspan="7" class="loading-cell">No open positions. Use Scanner tab to execute trades.</td></tr>`;
        } else {
          holdingsTableBody.innerHTML = p.positions.map(pos => {
            const pnlClass = pos.unrealized_pnl >= 0 ? 'green-text' : 'red-text';
            const pnlPrefix = pos.unrealized_pnl >= 0 ? '+' : '';
            return `
              <tr>
                <td><strong>${pos.name}</strong><br><small class="text-muted">${pos.ticker}</small></td>
                <td>${pos.shares}</td>
                <td>₹${pos.entry_price}</td>
                <td>₹${pos.current_price}</td>
                <td>
                  <small class="green-text">TGT: ₹${pos.target_price}</small><br>
                  <small class="red-text">SL: ₹${pos.stop_loss}</small>
                </td>
                <td class="${pnlClass}"><strong>${pnlPrefix}₹${pos.unrealized_pnl}</strong> (${pnlPrefix}${pos.pnl_pct}%)</td>
                <td>
                  <button class="btn danger btn-sm" onclick="closePosition('${pos.ticker}', ${pos.current_price})">
                    Close
                  </button>
                </td>
              </tr>
            `;
          }).join('');
        }

        // History Table
        if (p.trade_history.length === 0) {
          historyTableBody.innerHTML = `<tr><td colspan="6" class="loading-cell">No trades executed yet.</td></tr>`;
        } else {
          historyTableBody.innerHTML = p.trade_history.map(t => {
            const pnlClass = t.realized_pnl >= 0 ? 'green-text' : 'red-text';
            return `
              <tr>
                <td><small>${t.id}</small></td>
                <td><strong>${t.ticker}</strong></td>
                <td><span class="badge ${t.type === 'OPEN' ? 'buy' : 'hold'}">${t.action}</span></td>
                <td>₹${t.price}</td>
                <td class="${pnlClass}">${t.type === 'CLOSE' ? `₹${t.realized_pnl}` : '--'}</td>
                <td><small>${t.timestamp}</small></td>
              </tr>
            `;
          }).join('');
        }
      }
    } catch (err) {
      console.error('Failed to load portfolio:', err);
    }
  }

  // 6. Close Position Handler
  window.closePosition = async function(ticker, currentPrice) {
    try {
      const res = await fetch('/api/close_trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: ticker, exit_price: currentPrice, reason: "Manual User Close" })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        alert(data.message);
        loadPortfolio();
      } else {
        alert(`Failed to close: ${data.detail || data.message}`);
      }
    } catch (err) {
      alert(`Error closing trade: ${err.message}`);
    }
  };

  // 7. Strategy Backtester Handler
  async function runBacktest() {
    const ticker = backtestTicker.value;
    const period = backtestPeriod.value;

    btnRunBacktest.innerHTML = `<span>⏳</span> Running Simulation...`;
    btnRunBacktest.disabled = true;

    try {
      const res = await fetch(`/api/backtest/${ticker}?period=${period}`);
      const data = await res.json();
      if (data.success) {
        const bt = data.backtest;
        backtestResults.classList.remove('hidden');

        document.getElementById('btStrategyReturn').textContent = `${bt.total_return_pct >= 0 ? '+' : ''}${bt.total_return_pct}%`;
        document.getElementById('btStrategyReturn').className = `metric-value ${bt.total_return_pct >= 0 ? 'green-text' : 'red-text'}`;
        document.getElementById('btBenchmarkReturn').textContent = `Vs Buy & Hold: ${bt.benchmark_return_pct >= 0 ? '+' : ''}${bt.benchmark_return_pct}%`;

        document.getElementById('btWinRate').textContent = `${bt.win_rate_pct}%`;
        document.getElementById('btTradeCounts').textContent = `${bt.total_trades} Trades (${bt.winning_trades} Wins / ${bt.losing_trades} Losses)`;

        document.getElementById('btProfitFactor').textContent = bt.profit_factor;
        document.getElementById('btMaxDrawdown').textContent = `${bt.max_drawdown_pct}%`;

        renderBacktestChart(bt.equity_curve);
      }
    } catch (err) {
      alert(`Backtest failed: ${err.message}`);
    } finally {
      btnRunBacktest.innerHTML = `<span>🚀</span> Run Backtest`;
      btnRunBacktest.disabled = false;
    }
  }

  // 8. Render Backtest Chart.js Chart
  function renderBacktestChart(equitySeries) {
    const ctx = document.getElementById('backtestChart').getContext('2d');
    if (backtestChartInstance) {
      backtestChartInstance.destroy();
    }

    const labels = equitySeries.map(pt => pt.date);
    const equityData = equitySeries.map(pt => pt.equity);

    backtestChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Quantitative Strategy Portfolio Equity (₹)',
          data: equityData,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#9ca3af', font: { family: 'Inter' } } }
        },
        scales: {
          x: { ticks: { color: '#9ca3af', maxTicksLimit: 10 }, grid: { color: 'rgba(255, 255, 255, 0.04)' } },
          y: { ticks: { color: '#9ca3af' }, grid: { color: 'rgba(255, 255, 255, 0.04)' } }
        }
      }
    });
  }
});
