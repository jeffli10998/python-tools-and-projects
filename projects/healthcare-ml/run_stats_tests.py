import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths relative to the script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "processed_health_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def load_data(file_path):
    """Loads processed data."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded data from {file_path} with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None

def load_model_components(model_dir):
    """Loads the trained model, scaler, and feature names."""
    try:
        model = joblib.load(os.path.join(model_dir, 'linear_regression_model.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        feature_names = joblib.load(os.path.join(model_dir, 'feature_names.pkl'))
        logger.info("Model, scaler, and feature names loaded successfully.")
        return model, scaler, feature_names
    except Exception as e:
        logger.error(f"Error loading model components: {e}")
        return None, None, None

def prepare_test_data(df, feature_names, target_col='life_expectancy'):
    """Prepares test data using the loaded feature names."""
    try:
        df = df.dropna() # Ensure no NaNs
        X = df[feature_names]
        y = df[target_col]
        logger.info(f"Prepared test data with {len(feature_names)} features.")
        return X, y
    except Exception as e:
        logger.error(f"Error preparing test data: {e}")
        return None, None

def run_statistical_tests():
    """
    Loads the model and data, runs statistical tests, and prints explanations.
    """
    logger.info("Starting statistical tests for the healthcare linear regression model.")

    # 1. Load Data
    df = load_data(PROCESSED_DATA_PATH)
    if df is None:
        logger.error("Failed to load processed data. Please ensure 'download_data.py' has been run.")
        return

    # 2. Load Model Components
    model, scaler, feature_names = load_model_components(MODELS_DIR)
    if model is None or scaler is None or feature_names is None:
        logger.error("Failed to load model components. Please ensure 'model.py' has been run to train and save the model.")
        return

    # 3. Prepare Test Data
    # We need to re-create X_test and y_test from the full dataset
    # to ensure consistency with how the model was trained.
    # For simplicity, we'll use the entire processed dataset as 'test' data here
    # to get a comprehensive statsmodels summary.
    # In a real scenario, you'd use the actual X_test and y_test from your split.
    # For this script, we'll assume the model was trained on a split, and we're
    # now evaluating its overall fit on the processed data.
    
    # Define target column
    target_col = 'life_expectancy'
    
    # Exclude non-feature columns and the target column
    exclude_cols = ['Country', 'Year']
    actual_feature_names = [col for col in df.columns if col not in [target_col] + exclude_cols]

    X_full = df[actual_feature_names]
    y_full = df[target_col]

    # Scale features using the loaded scaler
    X_full_scaled = scaler.transform(X_full)
    X_full_scaled_df = pd.DataFrame(X_full_scaled, columns=actual_feature_names, index=X_full.index)

    # 4. Make Predictions
    y_pred = model.predict(X_full_scaled_df)

    print("\\n" + "="*50)
    print("STATISTICAL TEST RESULTS AND EXPLANATIONS")
    print("="*50 + "\\n")

    # --- R-squared (R2) and Root Mean Squared Error (RMSE) ---
    r2 = r2_score(y_full, y_pred)
    rmse = np.sqrt(mean_squared_error(y_full, y_pred))

    print("## 1. Model Performance Metrics")
    print(f"R-squared (R2): {r2:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}\\n")

    print("### Explanation of Metrics:")
    print("-   **R-squared (R2)**: This metric represents the proportion of the variance in the dependent variable (life expectancy) that is predictable from the independent variables (healthcare indicators). An R2 value of 1 indicates that the model explains all the variability of the response data around its mean, while an R2 of 0 indicates that the model explains no variability. A higher R2 generally indicates a better fit.")
    print("-   **Root Mean Squared Error (RMSE)**: This is the standard deviation of the residuals (prediction errors). Residuals are a measure of how far from the regression line data points are. RMSE is a measure of the absolute fit of the model to the data—how close the observed data points are to the model's predicted values. A lower RMSE indicates a better fit.\\n")

    # --- T-tests for Regression Coefficients using Statsmodels ---
    print("## 2. T-tests for Regression Coefficients using Statsmodels")
    print("Using `statsmodels` to get detailed statistical output for each predictor variable.\\n")

    # Add a constant (intercept) to the independent variables for statsmodels
    X_full_sm = sm.add_constant(X_full_scaled_df)

    # Create and fit the OLS model
    sm_model = sm.OLS(y_full, X_full_sm)
    sm_results = sm_model.fit()

    # Print the summary
    print(sm_results.summary())
    print("\\n")

    print("### Explanation of Statsmodels Output:")
    print("The `sm_results.summary()` output provides a wealth of information. Here are the key components and their interpretations:\\n")

    print("#### **A. Model Statistics (Top Section):**")
    print("-   **R-squared**: Same as the R2 calculated with `sklearn.metrics`, indicating the proportion of variance in the dependent variable explained by the model.")
    print("-   **Adj. R-squared**: Adjusted R-squared accounts for the number of predictor variables in the model. It increases only if the new term improves the model more than would be expected by chance. Useful for comparing models with different numbers of predictors.")
    print("-   **F-statistic**: This is a global test for the significance of the regression model. It tests the null hypothesis that all regression coefficients are equal to zero (i.e., none of the independent variables have a linear relationship with the dependent variable). A large F-statistic with a small p-value (`Prob (F-statistic)`) indicates that the model is statistically significant.")
    print("-   **Prob (F-statistic)**: The p-value associated with the F-statistic. If this value is less than your chosen significance level (e.g., 0.05), you can reject the null hypothesis and conclude that the model is statistically significant.")
    print("-   **Log-Likelihood, AIC, BIC**: Information criteria used for model comparison. Lower values generally indicate a better model.\\n")

    print("#### **B. Coefficients Table (Middle Section):**")
    print("This table is crucial for understanding the contribution of each predictor variable.")
    print("-   **const**: This is the intercept of the regression model. It represents the expected mean value of the dependent variable when all independent variables are zero.")
    print("-   **[Feature Names]**: These are your independent variables (e.g., 'Health_Expenditure_per_Capita', 'GDP_per_Capita', etc.).")
    print("    -   **coef**: The estimated regression coefficient for each predictor. For a linear regression, this represents the change in the dependent variable for a one-unit increase in the predictor variable, holding all other predictors constant. Since your features are scaled, these coefficients represent the change in life expectancy for a one-standard-deviation change in the respective scaled feature.")
    print("    -   **std err**: The standard error of the coefficient estimate. It measures the precision of the coefficient. A smaller standard error indicates a more precise estimate.")
    print("    -   **t**: The t-statistic for each coefficient. It's calculated as `coef / std err`. It tests the null hypothesis that the true coefficient is zero (i.e., the predictor has no effect on the dependent variable).")
    print("    -   **P>|t|**: The p-value associated with the t-statistic. This is the most important value for determining the statistical significance of each predictor.")
    print("        -   If `P>|t|` is less than your chosen significance level (e.g., 0.05), you can reject the null hypothesis and conclude that the predictor variable has a statistically significant effect on the dependent variable.")
    print("        -   If `P>|t|` is greater than the significance level, you cannot reject the null hypothesis, suggesting that the predictor may not have a statistically significant linear relationship with the dependent variable in the presence of other predictors.")
    print("    -   **[0.025, 0.975]**: This represents the 95% confidence interval for the coefficient. It means that we are 95% confident that the true value of the coefficient lies within this range. If the interval includes zero, the coefficient is not statistically significant at the 5% level.\\n")

    print("#### **C. Omnibus and Durbin-Watson (Bottom Section):**")
    print("-   **Omnibus/Prob(Omnibus)**: Tests the normality of the residuals. A low p-value (e.g., < 0.05) suggests that the residuals are not normally distributed, which can indicate issues with the model assumptions.")
    print("-   **Durbin-Watson**: Tests for autocorrelation in the residuals. A value close to 2 indicates no autocorrelation. Values significantly less than 2 suggest positive autocorrelation, while values significantly greater than 2 suggest negative autocorrelation. Autocorrelation can violate the assumptions of linear regression.")
    print("-   **Jarque-Bera (JB)/Prob(JB)**: Another test for the normality of residuals. Similar to Omnibus, a low p-value suggests non-normal residuals.")
    print("-   **Skew**: Measures the asymmetry of the residuals distribution.")
    print("-   **Kurtosis**: Measures the \"tailedness\" of the residuals distribution.\\n")

    logger.info("Statistical tests completed.")

if __name__ == "__main__":
    run_statistical_tests()