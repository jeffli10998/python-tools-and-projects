import unittest
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Import functions to test
from utils import (
    load_and_preprocess_data,
    prepare_model_data,
    scale_features,
    calculate_metrics
)


class TestModelFunctions(unittest.TestCase):
    """
    Test cases for the model functions.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create a small mock dataset
        np.random.seed(42)
        n_samples = 100
        
        # Create mock data
        self.mock_data = pd.DataFrame({
            'Country': ['Country_' + str(i % 10) for i in range(n_samples)],
            'Year': [2000 + i % 21 for i in range(n_samples)],
            'health_exp_per_capita': np.random.normal(2000, 500, n_samples),
            'health_exp_pct_gdp': np.random.normal(8, 2, n_samples),
            'hospital_beds': np.random.normal(3, 1, n_samples),
            'physicians': np.random.normal(2.5, 0.8, n_samples),
            'gdp_per_capita': np.random.normal(25000, 10000, n_samples),
            'unemployment': np.random.normal(6, 2, n_samples),
            'urban_population': np.random.normal(70, 10, n_samples),
            'life_expectancy': np.random.normal(75, 5, n_samples)
        })
        
        # Add some missing values to test preprocessing
        self.mock_data.loc[0:5, 'health_exp_per_capita'] = np.nan
        
        # Save mock data to a temporary file
        os.makedirs('../data/test', exist_ok=True)
        self.test_file = '../data/test/test_data.csv'
        self.mock_data.to_csv(self.test_file, index=False)
    
    def tearDown(self):
        """
        Clean up after tests.
        """
        # Remove the test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_load_and_preprocess_data(self):
        """
        Test loading and preprocessing data.
        """
        # Test with the mock data file
        df_clean = load_and_preprocess_data(self.test_file)
        
        # Check that the function returns a DataFrame
        self.assertIsInstance(df_clean, pd.DataFrame)
        
        # Check that missing values were removed
        self.assertEqual(df_clean.isnull().sum().sum(), 0)
        
        # Check that the shape is correct (6 rows with NaN should be removed)
        self.assertEqual(df_clean.shape[0], self.mock_data.shape[0] - 6)
    
    def test_prepare_model_data(self):
        """
        Test preparing data for modeling.
        """
        # Use the clean mock data (drop NaN rows first)
        df_clean = self.mock_data.dropna()
        
        # Test data preparation
        X_train, X_test, y_train, y_test, feature_cols = prepare_model_data(
            df_clean, target_col='life_expectancy', exclude_cols=['Country', 'Year']
        )
        
        # Check that the function returns the expected objects
        self.assertIsInstance(X_train, pd.DataFrame)
        self.assertIsInstance(X_test, pd.DataFrame)
        self.assertIsInstance(y_train, pd.Series)
        self.assertIsInstance(y_test, pd.Series)
        self.assertIsInstance(feature_cols, list)
        
        # Check that the feature columns are correct
        expected_features = ['health_exp_per_capita', 'health_exp_pct_gdp', 'hospital_beds', 
                            'physicians', 'gdp_per_capita', 'unemployment', 'urban_population']
        self.assertListEqual(sorted(feature_cols), sorted(expected_features))
        
        # Check that the train-test split is correct (default test_size=0.2)
        total_samples = len(df_clean)
        expected_train_size = int(total_samples * 0.8)
        expected_test_size = total_samples - expected_train_size
        self.assertEqual(len(X_train), expected_train_size)
        self.assertEqual(len(X_test), expected_test_size)
    
    def test_scale_features(self):
        """
        Test scaling features.
        """
        # Create simple test data
        X_train = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        X_test = pd.DataFrame({
            'feature1': [6, 7],
            'feature2': [60, 70]
        })
        
        # Test scaling
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
        
        # Check that the function returns the expected objects
        self.assertIsInstance(X_train_scaled, np.ndarray)
        self.assertIsInstance(X_test_scaled, np.ndarray)
        self.assertIsInstance(scaler, StandardScaler)
        
        # Check that the scaled data has the right shape
        self.assertEqual(X_train_scaled.shape, X_train.shape)
        self.assertEqual(X_test_scaled.shape, X_test.shape)
        
        # Check that the scaled data has mean close to 0 and std close to 1 for training data
        self.assertAlmostEqual(X_train_scaled[:, 0].mean(), 0, places=10)
        self.assertAlmostEqual(X_train_scaled[:, 1].mean(), 0, places=10)
        self.assertAlmostEqual(X_train_scaled[:, 0].std(), 1, places=10)
        self.assertAlmostEqual(X_train_scaled[:, 1].std(), 1, places=10)
    
    def test_calculate_metrics(self):
        """
        Test calculating regression metrics.
        """
        # Create simple test data
        y_true = np.array([3, 5, 2, 7, 9])
        y_pred = np.array([2.8, 4.5, 2.5, 7.2, 8.8])
        
        # Test metric calculation
        metrics = calculate_metrics(y_true, y_pred)
        
        # Check that the function returns a dictionary with the expected keys
        self.assertIsInstance(metrics, dict)
        self.assertIn('mse', metrics)
        self.assertIn('rmse', metrics)
        self.assertIn('r2', metrics)
        
        # Check that the metrics are calculated correctly
        expected_mse = ((3-2.8)**2 + (5-4.5)**2 + (2-2.5)**2 + (7-7.2)**2 + (9-8.8)**2) / 5
        expected_rmse = np.sqrt(expected_mse)
        
        self.assertAlmostEqual(metrics['mse'], expected_mse, places=10)
        self.assertAlmostEqual(metrics['rmse'], expected_rmse, places=10)
        self.assertTrue(0 <= metrics['r2'] <= 1)  # R² should be between 0 and 1 for this good fit


if __name__ == '__main__':
    unittest.main()