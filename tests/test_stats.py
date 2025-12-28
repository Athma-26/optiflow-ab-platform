import pytest
import numpy as np
import sys
import os

# Add the root directory to path so we can import 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiment import ABTestEngine

def test_initialization():
    """Test if the engine initializes with correct defaults."""
    engine = ABTestEngine(baseline_rate=0.1, lift=0.02, sample_size=1000)
    assert engine.baseline_rate == 0.1
    assert engine.sample_size == 1000

def test_simulation_shape():
    """Test if simulation generates the correct amount of data."""
    engine = ABTestEngine(sample_size=2000)
    engine.run_simulation()
    
    assert len(engine.control_data) == 1000
    assert len(engine.test_data) == 1000
    assert engine.control_data.max() <= 1  # Should be binary (0 or 1)

def test_statistics_math():
    """Test the math logic with known values."""
    engine = ABTestEngine()
    
    # Manually inject clear data (50% vs 100% conversion)
    engine.control_data = np.array([0, 1, 0, 1]) # 50%
    engine.test_data = np.array([1, 1, 1, 1])    # 100%
    
    stats = engine.get_statistics()
    
    assert stats['control_rate'] == 0.5
    assert stats['test_rate'] == 1.0
    assert stats['lift'] == 1.0 # (1.0 - 0.5) / 0.5 = 1.0 (100% lift)