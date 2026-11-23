"""Educational market risk estimates using simulated daily log returns."""
import numpy as np
import pandas as pd


def simulated_returns(n=1500, seed=42):
    rng = np.random.default_rng(seed)
    # Simulated daily log returns; volatility clustering via a two-regime schedule.
    volatility = np.where((np.arange(n) // 150) % 3 == 2, 0.025, 0.012)
    return pd.Series(rng.normal(0, volatility), name="daily_log_return")


def rolling_risk(returns, window=250, confidence=0.99):
    """One-day-ahead historical VaR/ES using only prior observations."""
    if not 0 < confidence < 1 or window < 20 or len(returns) <= window:
        raise ValueError("Invalid confidence, window, or sample length")
    x = np.asarray(returns, dtype=float)
    if not np.isfinite(x).all():
        raise ValueError("Returns must be finite")
    rows = []
    for i in range(window, len(x)):
        history = x[i-window:i]
        q = np.quantile(history, 1-confidence)
        tail = history[history <= q]
        var = -q
        es = -tail.mean()
        realized_loss = -x[i]
        rows.append((i, x[i], var, es, realized_loss > var))
    return pd.DataFrame(rows, columns=["day", "return", "VaR", "ES", "exception"])


def kupiec_pof(exceptions, confidence=0.99):
    """Kupiec unconditional coverage likelihood-ratio statistic and p-value."""
    from scipy.stats import chi2
    flags = np.asarray(exceptions, dtype=bool)
    n = len(flags)
    if n == 0:
        raise ValueError("No observations")
    k = int(flags.sum())
    p0 = 1-confidence
    phat = k/n
    def loglik(p):
        if p == 0:
            return 0.0 if k == 0 else -np.inf
        if p == 1:
            return 0.0 if k == n else -np.inf
        return k*np.log(p)+(n-k)*np.log1p(-p)
    lr = max(0.0, 2*(loglik(phat)-loglik(p0)))
    return {"observations":n, "exceptions":k, "exception_rate":phat, "expected_rate":p0, "kupiec_lr":lr, "p_value":float(chi2.sf(lr,1))}
