import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
from typing import Dict, Tuple

class ABTestEngine:
    """
    A class to manage A/B test simulations and statistical analysis.
    
    Attributes:
        baseline_rate (float): The current conversion rate (0.0 to 1.0).
        expected_rate (float): The target conversion rate based on lift.
        sample_size (int): Total number of samples (Control + Test).
    """

    def __init__(self, baseline_rate: float = 0.10, lift: float = 0.02, sample_size: int = 10000):
        self.baseline_rate = baseline_rate
        self.expected_rate = baseline_rate + lift
        self.sample_size = sample_size
        self.control_data = None
        self.test_data = None

    def run_simulation(self) -> None:
        """Generates synthetic binomial data for Control and Test groups."""
        group_n = self.sample_size // 2
        
        # Simulate binomial outcomes (0 = No Conversion, 1 = Conversion)
        self.control_data = np.random.binomial(1, self.baseline_rate, group_n)
        self.test_data = np.random.binomial(1, self.expected_rate, group_n)

    def get_statistics(self) -> Dict[str, float]:
        """
        Calculates conversion rates, lift, Z-score, and P-value.
        
        Returns:
            Dict: A dictionary containing key metrics.
        """
        if self.control_data is None:
            raise ValueError("Data not generated. Run .run_simulation() first.")

        control_conv = self.control_data.sum()
        test_conv = self.test_data.sum()
        n_control = len(self.control_data)
        n_test = len(self.test_data)

        # Statistical Test (Two-sided Z-test)
        z_stat, p_value = proportions_ztest(
            [test_conv, control_conv], 
            [n_test, n_control]
        )

        return {
            "control_rate": self.control_data.mean(),
            "test_rate": self.test_data.mean(),
            "lift": (self.test_data.mean() - self.control_data.mean()) / self.control_data.mean(),
            "z_score": z_stat,
            "p_value": p_value
        }

    def get_trend_data(self, days: int = 30) -> pd.DataFrame:
        """Generates cumulative conversion data to simulate a 30-day experiment."""
        dates = pd.date_range(start="2024-01-01", periods=days)
        
        # Split data into roughly equal daily chunks
        chunk_size = len(self.control_data) // days
        
        # Calculate cumulative mean for each day
        c_trend = [self.control_data[:(i+1)*chunk_size].mean() for i in range(days)]
        t_trend = [self.test_data[:(i+1)*chunk_size].mean() for i in range(days)]
        
        return pd.DataFrame({
            "Date": dates,
            "Control": c_trend,
            "Test": t_trend
        })