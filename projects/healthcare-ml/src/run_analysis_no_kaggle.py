#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script to run the entire healthcare linear regression analysis pipeline.

This script orchestrates the entire workflow:
1. Creates and processes the mock data
2. Trains and evaluates the linear regression model
3. Generates visualizations and saves results
"""

import os
import logging
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.linear_model import LinearRegression

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Import project modules
from download_data_no_kaggle import main as download_data
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
    
    # Create absolute paths for directories
    base_dir = project_root
    dirs = ["data/raw", "data/processed", "models", "results"]
    
    # Create necessary directories with absolute paths
    dir_paths = {}
    for dir_path in dirs:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        dir_paths[dir_path] = full_path
    
    # Update paths with absolute paths
    for key, rel_path in PATHS.items():
        if rel_path.startswith('../'):
            # Convert relative path to absolute path
            abs_path = os.path.join(base_dir, rel_path[3:])
            PATHS[key] = abs_path
    
    logger.info(f"Using project root: {project_root}")
    logger.info(f"Data directory: {PATHS['raw_data_dir']}")
    logger.info(f"Results directory: {PATHS['results_dir']}")
    logger.info(f"Models directory: {PATHS['models_dir']}")
    
    # Step 1: Download and process data
    logger.info("Step 1: Creating and processing mock data")
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