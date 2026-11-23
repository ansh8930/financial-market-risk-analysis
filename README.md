# Financial Market Risk Analysis & VaR Back-testing

A reproducible educational Python project demonstrating **one-day 99% historical Value at Risk (VaR)**, **Expected Shortfall (ES)**, **rolling out-of-sample back-testing**, **VaR exceptions**, and the **Kupiec unconditional coverage test**.

## Data disclaimer
The dataset is **simulated daily log returns**, generated with a fixed random seed and alternating volatility regimes. It is **not real market data** and is **not appropriate for regulatory capital calculation or live trading**. No regulatory capital framework is implemented.

## Run
```bash
pip install -r requirements.txt
python run_analysis.py
python -m unittest discover -s tests -v
```

Results appear in `outputs/`: `rolling_risk.csv`, `summary.txt`, and `var_backtest.png`.

## Methodology
- Generate 1,500 simulated daily log returns using NumPy.
- For each day after the first 250 observations, estimate the lower 1% quantile of the **previous** 250 returns; VaR is its negative.
- ES is the negative mean of returns in the same historical tail.
- A breach occurs if today's realized negative log return exceeds yesterday's estimated VaR.
- Report breach rate and the Kupiec POF likelihood-ratio test. This tests unconditional exception frequency only, **not independence or full model validity**.

## Limitations
Log-return losses are used as a simplified risk proxy; actual portfolio P&L and capital calculations require additional modeling. Results depend on window length, confidence level, sample size, and the simulated volatility regime. This project does not implement FRTB, Basel capital, stress testing, or production model validation.

## Resume-safe description
- Implemented rolling historical 99% VaR and Expected Shortfall estimation in Python using simulated financial returns.
- Back-tested one-day risk forecasts by identifying VaR exceptions and computing Kupiec unconditional coverage statistics.
- Visualized simulated losses, VaR thresholds, and exceptions to examine risk model behavior under changing volatility.
