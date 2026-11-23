import unittest
import numpy as np
from src.risk import simulated_returns, rolling_risk, kupiec_pof

class RiskTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertTrue(np.array_equal(simulated_returns(seed=5), simulated_returns(seed=5)))
    def test_es_at_least_var(self):
        frame = rolling_risk(simulated_returns(400), 100)
        self.assertTrue((frame.ES >= frame.VaR - 1e-12).all())
    def test_no_lookahead(self):
        x = simulated_returns(400)
        first = rolling_risk(x,100).iloc[0]
        x.iloc[100] = 10.0
        changed = rolling_risk(x,100).iloc[0]
        self.assertAlmostEqual(first.VaR, changed.VaR)
    def test_backtest_counts(self):
        self.assertEqual(kupiec_pof([True,False,False])['exceptions'],1)
if __name__ == '__main__': unittest.main()
