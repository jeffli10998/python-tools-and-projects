import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data(data_file):
    """
    Load the processed health data.
    
    Args:
        data_file (str): Path to the processed data file
    
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        df = pd.read_csv(data_file)
        logger.info(f"Loaded data from {data_file} with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None


def prepare_data(df, target_col='life_expectancy', test_size=0.2, random_state=42):
    """
    Prepare data for modeling by splitting into features and target,
    and then into training and testing sets.
    
    Args:
        df (pd.DataFrame): Input data
        target_col (str): Name of the target column
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: X_train, X_test, y_train, y_test, feature_names
    """
    try:
        # Drop rows with missing values
        df = df.dropna()
        
        # Define features and target
        feature_cols = [col for col in df.columns if col not in [target_col, 'Country', 'Year']]
        X = df[feature_cols]
        y = df[target_col]
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        logger.info(f"Data prepared with {len(feature_cols)} features")
        logger.info(f"Training set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")
        
        return X_train, X_test, y_train, y_test, feature_cols
    except Exception as e:
        logger.error(f"Error preparing data: {e}")
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
        
        logger.info("Features scaled using StandardScaler")
        
        return X_train_scaled, X_test_scaled, scaler
    except Exception as e:
        logger.error(f"Error scaling features: {e}")
        return None, None, None


def train_model(X_train, y_train):
    """
    Train a linear regression model.
    
    Args:
        X_train: Training features
        y_train: Training target
    
    Returns:
        LinearRegression: Trained model
    """
    try:
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        logger.info("Linear regression model trained successfully")
        
        return model
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return None


def evaluate_model(model, X_test, y_test, feature_names=None):
    """
    Evaluate the trained model on the test set.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        feature_names (list): Names of the features
    
    Returns:
        dict: Dictionary of evaluation metrics
    """
    try:
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Get coefficients if feature names are provided
        coefficients = None
        if feature_names is not None:
            coefficients = dict(zip(feature_names, model.coef_))
        
        # Log results
        logger.info(f"Model evaluation results:")
        logger.info(f"  MSE: {mse:.4f}")
        logger.info(f"  RMSE: {rmse:.4f}")
        logger.info(f"  R²: {r2:.4f}")
        
        if coefficients:
            logger.info("Feature coefficients:")
            for feature, coef in sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True):
                logger.info(f"  {feature}: {coef:.4f}")
        
        return {
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'coefficients': coefficients,
            'y_test': y_test,
            'y_pred': y_pred
        }
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        return None


def plot_results(results, output_dir):
    """
    Plot the results of the model evaluation.
    
    Args:
        results (dict): Results from model evaluation
        output_dir (str): Directory to save the plots
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style="whitegrid")
        
        # 1. Actual vs Predicted plot
        plt.figure(figsize=(10, 6))
        plt.scatter(results['y_test'], results['y_pred'], alpha=0.5)
        plt.plot([results['y_test'].min(), results['y_test'].max()], 
                 [results['y_test'].min(), results['y_test'].max()], 
                 'r--')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted Values')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'actual_vs_predicted.png'))
        plt.close()
        
        # 2. Feature Importance plot
        if results['coefficients']:
            coef_df = pd.DataFrame({
                'Feature': list(results['coefficients'].keys()),
                'Coefficient': list(results['coefficients'].values())
            })
            coef_df = coef_df.sort_values('Coefficient', key=abs, ascending=False)
            
            plt.figure(figsize=(12, 8))
            sns.barplot(x='Coefficient', y='Feature', data=coef_df)
            plt.title('Feature Importance (Coefficient Magnitude)')
            plt.axvline(x=0, color='r', linestyle='--')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
            plt.close()
        
        # 3. Residuals plot
        residuals = results['y_test'] - results['y_pred']
        plt.figure(figsize=(10, 6))
        sns.histplot(residuals, kde=True)
        plt.xlabel('Residuals')
        plt.ylabel('Frequency')
        plt.title('Distribution of Residuals')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'residuals_distribution.png'))
        plt.close()
        
        # 4. Residuals vs Predicted plot
        plt.figure(figsize=(10, 6))
        plt.scatter(results['y_pred'], residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residuals vs Predicted Values')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'residuals_vs_predicted.png'))
        plt.close()
        
        logger.info(f"Plots saved to {output_dir}")
    except Exception as e:
        logger.error(f"Error plotting results: {e}")


def save_model(model, scaler, feature_names, output_dir):
    """
    Save the trained model and scaler.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        feature_names (list): Names of the features
        output_dir (str): Directory to save the model
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
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        logger.info(f"Feature names saved to {feature_path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")


def main():
    """
    Main function to train and evaluate the linear regression model.
    """
    # Define paths
    data_file = "../data/processed/processed_health_data.csv"
    models_dir = "../models"
    results_dir = "../results"
    
    # Create results directory
    os.makedirs(results_dir, exist_ok=True)
    
    # Load data
    df = load_data(data_file)
    if df is None:
        logger.error("Failed to load data. Exiting.")
        return
    
    # Prepare data
    X_train, X_test, y_train, y_test, feature_names = prepare_data(df)
    if X_train is None:
        logger.error("Failed to prepare data. Exiting.")
        return
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    if X_train_scaled is None:
        logger.error("Failed to scale features. Exiting.")
        return
    
    # Train model
    model = train_model(X_train_scaled, y_train)
    if model is None:
        logger.error("Failed to train model. Exiting.")
        return
    
    # Evaluate model
    results = evaluate_model(model, X_test_scaled, y_test, feature_names)
    if results is None:
        logger.error("Failed to evaluate model. Exiting.")
        return
    
    # Plot results
    plot_results(results, results_dir)
    
    # Save model
    save_model(model, scaler, feature_names, models_dir)
    
    logger.info("Model training and evaluation completed successfully.")


if __name__ == "__main__":
    main()