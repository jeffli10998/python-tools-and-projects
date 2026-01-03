import pytest
import pandas as pd
import numpy as np
from analyzer import TrendAnalyzer

def test_normalization_standard():
    data = [
        {'date': '2023-01-01', 'series1': 10, 'series2': 100},
        {'date': '2023-01-02', 'series1': 20, 'series2': 200},
        {'date': '2023-01-03', 'series1': 30, 'series2': 300},
    ]
    analyzer = TrendAnalyzer(data)
    results = analyzer.get_normalized_data(method='standard')
    
    # Check if mean is close to 0 and std is close to 1
    assert np.isclose(results['series1'].mean(), 0)
    assert np.isclose(results['series2'].mean(), 0)
    assert np.isclose(results['series1'].std(ddof=0), 1)

def test_normalization_minmax():
    data = [
        {'date': '2023-01-01', 'series1': 10, 'series2': 100},
        {'date': '2023-01-02', 'series1': 20, 'series2': 200},
        {'date': '2023-01-03', 'series1': 30, 'series2': 300},
    ]
    analyzer = TrendAnalyzer(data)
    results = analyzer.get_normalized_data(method='minmax')
    
    assert results['series1'].min() == 0
    assert results['series1'].max() == 1
    assert results['series2'].min() == 0
    assert results['series2'].max() == 1

def test_correlation():
    # Perfectly correlated
    data = [
        {'date': '2023-01-01', 'series1': 1, 'series2': 10},
        {'date': '2023-01-02', 'series1': 2, 'series2': 20},
        {'date': '2023-01-03', 'series1': 3, 'series2': 30},
    ]
    analyzer = TrendAnalyzer(data)
    correlations = analyzer.calculate_correlations()
    
    assert np.isclose(correlations['series1']['series2'], 1.0)

def test_empty_data():
    analyzer = TrendAnalyzer([])
    results = analyzer.get_analysis_results()
    assert results['data'] == []
    assert results['correlations'] == {}

def test_single_point():
    data = [{'date': '2023-01-01', 'series1': 10, 'series2': 100}]
    analyzer = TrendAnalyzer(data)
    results = analyzer.get_analysis_results()
    # Normalizing a single point usually results in 0 (standard) or NaN/0 (minmax)
    # StandardScaler on 1 point results in 0
    assert results['data'][0]['series1'] == 0
    assert results['correlations'] == {}
