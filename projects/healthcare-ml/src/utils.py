import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib


def setup_logging(log_level=logging.INFO, log_format='%(asctime)s - %(levelname)s - %(message)s'):
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (default: INFO)
        log_format: Logging format string
    
    Returns:
        logger: Configured logger
    """
    logging.basicConfig(level=log_level, format=log_format)
    logger = logging.getLogger(__name__)
    return logger


def create_directories(base_dir="..", dirs=None):
    """
    Create necessary directories for the project.
    
    Args:
        base_dir (str): Base directory path
        dirs (list): List of directories to create
    """
    if dirs is None:
        dirs = ["data/raw", "data/processed", "models", "results"]
    
    for dir_path in dirs:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
    
    return {dir_path: os.path.join(base_dir, dir_path) for dir_path in dirs}


def load_and_preprocess_data(file_path, logger=None):
    """
    Load and preprocess the data.
    
    Args:
        file_path (str): Path to the data file
        logger: Logger object
    
    Returns:
        pd.DataFrame: Preprocessed data
    """
    try:
        # Load data
        df = pd.read_csv(file_path)
        
        if logger:
            logger.info(f"Loaded data from {file_path} with shape {df.shape}")
        
        # Drop rows with missing values
        df_clean = df.dropna()
        
        if logger:
            logger.info(f"Data shape after dropping missing values: {df_clean.shape}")
        
        return df_clean
    except Exception as e:
        if logger:
            logger.error(f"Error loading or preprocessing data: {e}")
        return None


def prepare_model_data(df, target_col='life_expectancy', exclude_cols=None, test_size=0.2, random_state=42):
    """
    Prepare data for modeling by splitting into features and target,
    and then into training and testing sets.
    
    Args:
        df (pd.DataFrame): Input data
        target_col (str): Name of the target column
        exclude_cols (list): Columns to exclude from features
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: X_train, X_test, y_train, y_test, feature_cols
    """
    try:
        if exclude_cols is None:
            exclude_cols = ['Country', 'Year']
        
        # Define features and target
        feature_cols = [col for col in df.columns if col not in [target_col] + exclude_cols]
        X = df[feature_cols]
        y = df[target_col]
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        return X_train, X_test, y_train, y_test, feature_cols
    except Exception as e:
        return None, None, None, None, None


def scale_features(X_train, X_test):
    """
    Scale features using StandardScaler.
    
    Args:
        X_train (pd.DataFrame): Training features
        X_test (pd.DataFrame): Testing features
    
    Returns:
        tuple: Scaled X_train, X_test, and the scaler object
    """
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, scaler
    except Exception as e:
        return None, None, None


def calculate_metrics(y_true, y_pred):
    """
    Calculate regression metrics.
    
    Args:
        y_true: True target values
        y_pred: Predicted target values
    
    Returns:
        dict: Dictionary of metrics
    """
    try:
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        return {
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }
    except Exception as e:
        return None


def save_model(model, scaler, feature_names, output_dir):
    """
    Save the trained model and related objects.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        feature_names (list): Names of the features
        output_dir (str): Directory to save the model
    
    Returns:
        dict: Paths to saved files
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(output_dir, 'linear_regression_model.pkl')
        joblib.dump(model, model_path)
        
        # Save scaler
        scaler_path = os.path.join(output_dir, 'scaler.pkl')
        joblib.dump(scaler, scaler_path)
        
        # Save feature names
        feature_path = os.path.join(output_dir, 'feature_names.pkl')
        joblib.dump(feature_names, feature_path)
        
        return {
            'model_path': model_path,
            'scaler_path': scaler_path,
            'feature_path': feature_path
        }
    except Exception as e:
        return None


def load_model(model_dir):
    """
    Load a saved model and related objects.
    
    Args:
        model_dir (str): Directory containing the saved model
    
    Returns:
        tuple: model, scaler, feature_names
    """
    try:
        model_path = os.path.join(model_dir, 'linear_regression_model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        feature_path = os.path.join(model_dir, 'feature_names.pkl')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(feature_path)
        
        return model, scaler, feature_names
    except Exception as e:
        return None, None, None


def plot_correlation_matrix(df, numeric_cols=None, figsize=(14, 10)):
    """
    Plot correlation matrix of numeric columns.
    
    Args:
        df (pd.DataFrame): Input data
        numeric_cols (list): List of numeric columns to include
        figsize (tuple): Figure size
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix', fontsize=16)
    plt.tight_layout()
    
    return plt.gcf()


def plot_feature_importance(feature_names, coefficients, figsize=(12, 8)):
    """
    Plot feature importance based on model coefficients.
    
    Args:
        feature_names (list): Names of the features
        coefficients (array): Model coefficients
        figsize (tuple): Figure size
    """
    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients
    })
    
    coef_df = coef_df.reindex(coef_df['Coefficient'].abs().sort_values(ascending=False).index)
    
    plt.figure(figsize=figsize)
    sns.barplot(x='Coefficient', y='Feature', data=coef_df)
    plt.title('Feature Importance (Coefficient Magnitude)', fontsize=16)
    plt.axvline(x=0, color='r', linestyle='--')
    plt.tight_layout()
    
    return plt.gcf()