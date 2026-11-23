from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.risk import simulated_returns, rolling_risk, kupiec_pof

out = Path('outputs'); out.mkdir(exist_ok=True)
returns = simulated_returns()
results = rolling_risk(returns)
summary = kupiec_pof(results['exception'])
results.to_csv(out/'rolling_risk.csv', index=False)
with (out/'summary.txt').open('w') as f:
    f.write('SIMULATED RETURNS — EDUCATIONAL PROJECT ONLY\n')
    for k,v in summary.items(): f.write(f'{k}: {v}\n')
fig, ax = plt.subplots(figsize=(11,4))
ax.plot(results['day'], -results['return'], label='Realized daily loss', alpha=.65)
ax.plot(results['day'], results['VaR'], label='99% historical VaR')
ax.scatter(results.loc[results.exception,'day'], -results.loc[results.exception,'return'], marker='x', color='red', label='VaR exceptions')
ax.set(xlabel='Simulated trading day', ylabel='Fraction of portfolio value', title='Rolling 99% Historical VaR vs. Simulated Losses')
ax.legend(); fig.tight_layout(); fig.savefig(out/'var_backtest.png', dpi=160)
print((out/'summary.txt').read_text())
