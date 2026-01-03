#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script to run the entire healthcare linear regression analysis pipeline.

This script orchestrates the entire workflow:
1. Downloads and processes the data
2. Trains and evaluates the linear regression model
3. Generates visualizations and saves results
"""

import os
import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Import project modules
from download_data import main as download_data
from model import load_data, prepare_data, scale_features, train_model, evaluate_model, plot_results, save_model
from utils import setup_logging, create_directories
from config import PATHS, LOGGING, DATA_PROCESSING


def run_pipeline():
    """
    Run the complete analysis pipeline.
    """
    # Set up logging
    logger = setup_logging()
    logger.info("Starting healthcare linear regression analysis pipeline")
    
    # Create necessary directories
    create_directories()
    
    # Step 1: Download and process data
    logger.info("Step 1: Downloading and processing data")
    download_data()
    
    # Step 2: Train and evaluate model
    logger.info("Step 2: Training and evaluating model")
    
    # Load processed data
    data_file = PATHS['processed_data_file']
    df = load_data(data_file)
    if df is None:
        logger.error("Failed to load data. Exiting.")
        return
    
    # Prepare data for modeling
    X_train, X_test, y_train, y_test, feature_names = prepare_data(
        df, 
        target_col=DATA_PROCESSING['target_column'],
        test_size=DATA_PROCESSING['test_size'],
        random_state=DATA_PROCESSING['random_state']
    )
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
    
    # Step 3: Generate visualizations and save results
    logger.info("Step 3: Generating visualizations and saving results")
    
    # Create results directory if it doesn't exist
    os.makedirs(PATHS['results_dir'], exist_ok=True)
    
    # Plot results
    plot_results(results, PATHS['results_dir'])
    
    # Save model
    save_model(model, scaler, feature_names, PATHS['models_dir'])
    
    logger.info("Healthcare linear regression analysis pipeline completed successfully")
    
    # Print summary of results
    print("\nAnalysis Results Summary:")
    print(f"  R² Score: {results['r2']:.4f}")
    print(f"  RMSE: {results['rmse']:.4f}")
    print("\nTop 3 most important features:")
    
    # Get top 3 features by coefficient magnitude
    if results['coefficients']:
        sorted_coefs = sorted(results['coefficients'].items(), key=lambda x: abs(x[1]), reverse=True)
        for i, (feature, coef) in enumerate(sorted_coefs[:3]):
            print(f"  {i+1}. {feature}: {coef:.4f}")
    
    print(f"\nVisualizations saved to: {PATHS['results_dir']}")
    print(f"Model saved to: {PATHS['models_dir']}")


if __name__ == "__main__":
    run_pipeline()