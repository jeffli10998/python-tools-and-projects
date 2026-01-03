#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to make predictions using the trained linear regression model.

This script demonstrates how to:
1. Load the trained model
2. Preprocess new data
3. Make predictions
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
import logging

# Import project modules
from utils import setup_logging
from config import PATHS


def load_model_components():
    """
    Load the trained model, scaler, and feature names.
    
    Returns:
        tuple: model, scaler, feature_names
    """
    try:
        # Define paths
        model_path = PATHS['model_file']
        scaler_path = PATHS['scaler_file']
        feature_path = PATHS['feature_names_file']
        
        # Check if files exist
        for path in [model_path, scaler_path, feature_path]:
            if not os.path.exists(path):
                logging.error(f"File not found: {path}")
                return None, None, None
        
        # Load files
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(feature_path)
        
        logging.info("Model components loaded successfully")
        return model, scaler, feature_names
    except Exception as e:
        logging.error(f"Error loading model components: {e}")
        return None, None, None


def predict_life_expectancy(input_data, model, scaler, feature_names):
    """
    Make predictions using the trained model.
    
    Args:
        input_data (pd.DataFrame or dict): Input data with features
        model: Trained model
        scaler: Fitted scaler
        feature_names (list): Names of the features
    
    Returns:
        float: Predicted life expectancy
    """
    try:
        # Convert dict to DataFrame if necessary
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        # Check if all required features are present
        missing_features = [feat for feat in feature_names if feat not in input_data.columns]
        if missing_features:
            logging.error(f"Missing features: {missing_features}")
            return None
        
        # Select only the required features in the correct order
        X = input_data[feature_names]
        
        # Scale the features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = model.predict(X_scaled)
        
        return prediction[0]
    except Exception as e:
        logging.error(f"Error making prediction: {e}")
        return None


def main():
    """
    Main function to demonstrate prediction.
    """
    # Set up logging
    logger = setup_logging()
    
    # Load model components
    model, scaler, feature_names = load_model_components()
    if model is None:
        logger.error("Failed to load model components. Exiting.")
        return
    
    # Example input data (you can replace this with actual input)
    example_input = {
        'health_exp_per_capita': 3000,
        'health_exp_pct_gdp': 8.5,
        'hospital_beds': 3.2,
        'physicians': 2.8,
        'gdp_per_capita': 35000,
        'unemployment': 5.5,
        'urban_population': 75.0
    }
    
    # Make prediction
    predicted_life_expectancy = predict_life_expectancy(example_input, model, scaler, feature_names)
    
    if predicted_life_expectancy is not None:
        print("\nPrediction Example:")
        print("Input data:")
        for feature, value in example_input.items():
            print(f"  {feature}: {value}")
        print(f"\nPredicted life expectancy: {predicted_life_expectancy:.2f} years")
    else:
        print("Failed to make prediction. Check the logs for details.")


def interactive_prediction():
    """
    Interactive function to get user input and make predictions.
    """
    # Set up logging
    logger = setup_logging()
    
    # Load model components
    model, scaler, feature_names = load_model_components()
    if model is None:
        logger.error("Failed to load model components. Exiting.")
        return
    
    print("\nHealthcare Linear Regression - Life Expectancy Predictor")
    print("=======================================================\n")
    print("Enter values for the following features (press Enter to use default values):\n")
    
    # Default values
    defaults = {
        'health_exp_per_capita': 3000,
        'health_exp_pct_gdp': 8.5,
        'hospital_beds': 3.2,
        'physicians': 2.8,
        'gdp_per_capita': 35000,
        'unemployment': 5.5,
        'urban_population': 75.0
    }
    
    # Get user input
    user_input = {}
    for feature in feature_names:
        while True:
            try:
                value = input(f"{feature} (default: {defaults[feature]}): ")
                if value.strip() == "":
                    user_input[feature] = defaults[feature]
                    break
                else:
                    user_input[feature] = float(value)
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    # Make prediction
    predicted_life_expectancy = predict_life_expectancy(user_input, model, scaler, feature_names)
    
    if predicted_life_expectancy is not None:
        print("\nPrediction Result:")
        print(f"Predicted life expectancy: {predicted_life_expectancy:.2f} years")
    else:
        print("Failed to make prediction. Check the logs for details.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_prediction()
    else:
        main()