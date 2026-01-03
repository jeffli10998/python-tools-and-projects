#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to generate visualizations from the healthcare data.

This script creates various plots to visualize the relationships
between healthcare indicators and life expectancy.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Import project modules
from utils import setup_logging, load_and_preprocess_data, plot_correlation_matrix
from config import PATHS, VISUALIZATION


def create_time_series_plots(df, output_dir):
    """
    Create time series plots for key indicators.
    
    Args:
        df (pd.DataFrame): Input data
        output_dir (str): Directory to save the plots
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style=VISUALIZATION['style'])
        
        # Select a few countries for better visualization
        countries = ['United States', 'United Kingdom', 'Germany', 'Japan', 'Brazil']
        df_selected = df[df['Country'].isin(countries)]
        
        # List of indicators to plot
        indicators = [
            'life_expectancy',
            'health_exp_per_capita',
            'health_exp_pct_gdp',
            'hospital_beds',
            'physicians'
        ]
        
        # Create time series plots for each indicator
        for indicator in indicators:
            plt.figure(figsize=VISUALIZATION['figure_size_medium'])
            
            for country in countries:
                country_data = df_selected[df_selected['Country'] == country]
                plt.plot(country_data['Year'], country_data[indicator], marker='o', label=country)
            
            plt.title(f'{indicator.replace("_", " ").title()} Over Time', fontsize=16)
            plt.xlabel('Year')
            plt.ylabel(indicator.replace('_', ' ').title())
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save the plot
            output_file = os.path.join(output_dir, f'{indicator}_time_series.png')
            plt.savefig(output_file)
            plt.close()
            
            logging.info(f"Time series plot for {indicator} saved to {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Error creating time series plots: {e}")
        return False


def create_scatter_matrix(df, output_dir):
    """
    Create a scatter matrix of key indicators.
    
    Args:
        df (pd.DataFrame): Input data
        output_dir (str): Directory to save the plots
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style=VISUALIZATION['style'])
        
        # Select key indicators
        indicators = [
            'life_expectancy',
            'health_exp_per_capita',
            'health_exp_pct_gdp',
            'hospital_beds',
            'physicians',
            'gdp_per_capita'
        ]
        
        # Create scatter matrix
        plt.figure(figsize=(14, 14))
        scatter_matrix = pd.plotting.scatter_matrix(
            df[indicators], 
            figsize=VISUALIZATION['figure_size_large'],
            diagonal='kde',
            alpha=VISUALIZATION['alpha'],
            marker='o',
            grid=True
        )
        
        # Rotate axis labels
        for ax in scatter_matrix.flatten():
            ax.xaxis.label.set_rotation(45)
            ax.yaxis.label.set_rotation(0)
            ax.yaxis.label.set_ha('right')
        
        plt.tight_layout()
        
        # Save the plot
        output_file = os.path.join(output_dir, 'scatter_matrix.png')
        plt.savefig(output_file)
        plt.close()
        
        logging.info(f"Scatter matrix saved to {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Error creating scatter matrix: {e}")
        return False


def create_boxplots(df, output_dir):
    """
    Create boxplots for key indicators by country.
    
    Args:
        df (pd.DataFrame): Input data
        output_dir (str): Directory to save the plots
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style=VISUALIZATION['style'])
        
        # Select top 10 countries by GDP per capita
        top_countries = df.groupby('Country')['gdp_per_capita'].mean().nlargest(10).index.tolist()
        df_top = df[df['Country'].isin(top_countries)]
        
        # List of indicators to plot
        indicators = [
            'life_expectancy',
            'health_exp_per_capita',
            'health_exp_pct_gdp',
            'hospital_beds',
            'physicians'
        ]
        
        # Create boxplots for each indicator
        for indicator in indicators:
            plt.figure(figsize=VISUALIZATION['figure_size_medium'])
            
            sns.boxplot(x='Country', y=indicator, data=df_top)
            plt.title(f'{indicator.replace("_", " ").title()} by Country', fontsize=16)
            plt.xlabel('Country')
            plt.ylabel(indicator.replace('_', ' ').title())
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Save the plot
            output_file = os.path.join(output_dir, f'{indicator}_boxplot.png')
            plt.savefig(output_file)
            plt.close()
            
            logging.info(f"Boxplot for {indicator} saved to {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Error creating boxplots: {e}")
        return False


def create_heatmap(df, output_dir):
    """
    Create a heatmap of correlations between indicators.
    
    Args:
        df (pd.DataFrame): Input data
        output_dir (str): Directory to save the plots
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style=VISUALIZATION['style'])
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in ['Year']]
        
        # Create correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        plt.figure(figsize=VISUALIZATION['figure_size_medium'])
        sns.heatmap(
            corr_matrix, 
            annot=True, 
            cmap=VISUALIZATION['cmap'], 
            fmt='.2f', 
            linewidths=0.5
        )
        plt.title('Correlation Matrix of Healthcare Indicators', fontsize=16)
        plt.tight_layout()
        
        # Save the plot
        output_file = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(output_file)
        plt.close()
        
        logging.info(f"Correlation heatmap saved to {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Error creating heatmap: {e}")
        return False


def create_pairplot(df, output_dir):
    """
    Create a pairplot of key indicators.
    
    Args:
        df (pd.DataFrame): Input data
        output_dir (str): Directory to save the plots
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the style
        sns.set(style=VISUALIZATION['style'])
        
        # Select key indicators
        indicators = [
            'life_expectancy',
            'health_exp_per_capita',
            'health_exp_pct_gdp',
            'hospital_beds',
            'physicians'
        ]
        
        # Sample data for faster plotting (if dataset is large)
        if len(df) > 1000:
            df_sample = df.sample(1000, random_state=42)
        else:
            df_sample = df
        
        # Create pairplot
        pairplot = sns.pairplot(
            df_sample[indicators], 
            diag_kind='kde',
            plot_kws={'alpha': VISUALIZATION['alpha']}
        )
        pairplot.fig.suptitle('Pairwise Relationships Between Healthcare Indicators', y=1.02, fontsize=16)
        plt.tight_layout()
        
        # Save the plot
        output_file = os.path.join(output_dir, 'pairplot.png')
        plt.savefig(output_file)
        plt.close()
        
        logging.info(f"Pairplot saved to {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Error creating pairplot: {e}")
        return False


def main():
    """
    Main function to generate visualizations.
    """
    # Set up logging
    logger = setup_logging()
    logger.info("Starting visualization generation")
    
    # Load data
    data_file = PATHS['processed_data_file']
    df = load_and_preprocess_data(data_file, logger)
    if df is None:
        logger.error("Failed to load data. Exiting.")
        return
    
    # Create output directory
    output_dir = PATHS['results_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate visualizations
    logger.info("Generating visualizations...")
    
    # Create time series plots
    create_time_series_plots(df, output_dir)
    
    # Create scatter matrix
    create_scatter_matrix(df, output_dir)
    
    # Create boxplots
    create_boxplots(df, output_dir)
    
    # Create heatmap
    create_heatmap(df, output_dir)
    
    # Create pairplot
    create_pairplot(df, output_dir)
    
    logger.info(f"All visualizations saved to {output_dir}")
    print(f"\nVisualizations generated successfully and saved to {output_dir}")


if __name__ == "__main__":
    main()