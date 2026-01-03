import os
import pandas as pd
import numpy as np
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()


def setup_kaggle_credentials():
    """
    Set up Kaggle API credentials.
    
    You need to have a Kaggle account and download your API credentials from your account settings.
    Place the kaggle.json file in ~/.kaggle/ or set KAGGLE_USERNAME and KAGGLE_KEY environment variables.
    """
    try:
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        logger.info("Kaggle API authenticated successfully")
        return api
    except Exception as e:
        logger.error(f"Error authenticating Kaggle API: {e}")
        logger.info("Please ensure you have set up your Kaggle credentials correctly.")
        logger.info("You can set KAGGLE_USERNAME and KAGGLE_KEY environment variables or place kaggle.json in ~/.kaggle/")
        return None


def create_data_directory(data_dir="../data"):
    """
    Create data directory if it doesn't exist.
    
    Args:
        data_dir (str): Path to the data directory
    """
    os.makedirs(data_dir, exist_ok=True)
    raw_dir = os.path.join(data_dir, "raw")
    processed_dir = os.path.join(data_dir, "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    logger.info(f"Created data directories: {raw_dir} and {processed_dir}")
    return raw_dir, processed_dir


def download_who_health_data(api, raw_dir):
    """
    Download WHO Global Health Expenditure dataset from Kaggle.
    
    This is a mock function that simulates downloading data from Kaggle.
    In a real scenario, you would use the Kaggle API to download the dataset.
    
    Args:
        api: Authenticated Kaggle API instance
        raw_dir (str): Directory to save the raw data
    """
    try:
        # In a real scenario, you would use:
        # api.dataset_download_files('worldbank/global-health-expenditure', path=raw_dir, unzip=True)
        
        # For this mock example, we'll create synthetic data instead
        logger.info("Creating mock WHO Global Health Expenditure dataset...")
        
        # Create a list of countries
        countries = [
            "United States", "United Kingdom", "Germany", "France", "Japan", 
            "Canada", "Australia", "China", "India", "Brazil", "South Africa", 
            "Mexico", "Russia", "Italy", "Spain", "South Korea", "Singapore", 
            "Sweden", "Norway", "Denmark", "Finland", "Netherlands", "Belgium", 
            "Switzerland", "Austria", "Poland", "Turkey", "Indonesia", "Thailand", 
            "Malaysia"
        ]
        
        # Create years from 2000 to 2020
        years = list(range(2000, 2021))
        
        # Create indicators
        indicators = [
            "Health expenditure per capita (current US$)",
            "Health expenditure, total (% of GDP)",
            "Out-of-pocket health expenditure (% of total expenditure on health)",
            "Life expectancy at birth, total (years)",
            "Hospital beds (per 1,000 people)",
            "Physicians (per 1,000 people)",
            "GDP per capita (current US$)",
            "Unemployment, total (% of total labor force)",
            "Population, total",
            "Urban population (% of total)"
        ]
        
        # Create empty list to store data
        data = []
        
        # Generate mock data
        np.random.seed(42)  # For reproducibility
        for country in countries:
            for year in years:
                for indicator in indicators:
                    # Generate realistic values based on the indicator
                    if indicator == "Health expenditure per capita (current US$)":
                        value = np.random.normal(2000, 1500)
                    elif indicator == "Health expenditure, total (% of GDP)":
                        value = np.random.normal(8, 3)
                    elif indicator == "Out-of-pocket health expenditure (% of total expenditure on health)":
                        value = np.random.normal(20, 10)
                    elif indicator == "Life expectancy at birth, total (years)":
                        value = np.random.normal(75, 5)
                    elif indicator == "Hospital beds (per 1,000 people)":
                        value = np.random.normal(3, 1)
                    elif indicator == "Physicians (per 1,000 people)":
                        value = np.random.normal(2.5, 1)
                    elif indicator == "GDP per capita (current US$)":
                        value = np.random.normal(25000, 15000)
                    elif indicator == "Unemployment, total (% of total labor force)":
                        value = np.random.normal(6, 3)
                    elif indicator == "Population, total":
                        value = np.random.normal(50000000, 100000000)
                    elif indicator == "Urban population (% of total)":
                        value = np.random.normal(70, 15)
                    
                    # Ensure values are realistic (no negative values for most indicators)
                    if indicator not in ["Population, total", "GDP per capita (current US$)"]:
                        value = max(0, value)
                    
                    # Add some trends over time
                    if indicator == "Life expectancy at birth, total (years)":
                        value += (year - 2000) * 0.1  # Slight increase over time
                    elif indicator == "Health expenditure per capita (current US$)":
                        value += (year - 2000) * 50  # Increase over time
                    
                    # Add country-specific adjustments
                    if country in ["United States", "Switzerland", "Norway"]:
                        if indicator == "Health expenditure per capita (current US$)":
                            value *= 1.5  # Higher health expenditure
                    elif country in ["India", "Indonesia", "Brazil"]:
                        if indicator == "Health expenditure per capita (current US$)":
                            value *= 0.3  # Lower health expenditure
                    
                    data.append({
                        "Country": country,
                        "Year": year,
                        "Indicator": indicator,
                        "Value": value
                    })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        output_file = os.path.join(raw_dir, "who_health_expenditure.csv")
        df.to_csv(output_file, index=False)
        logger.info(f"Mock data saved to {output_file}")
        
        return output_file
    except Exception as e:
        logger.error(f"Error downloading/creating WHO health data: {e}")
        return None


def process_health_data(raw_file, processed_dir):
    """
    Process the WHO health data.
    
    Args:
        raw_file (str): Path to the raw data file
        processed_dir (str): Directory to save the processed data
    """
    try:
        # Read the raw data
        df = pd.read_csv(raw_file)
        logger.info(f"Read raw data from {raw_file}")
        
        # Select relevant indicators for our analysis
        relevant_indicators = [
            "Health expenditure per capita (current US$)",
            "Health expenditure, total (% of GDP)",
            "Life expectancy at birth, total (years)",
            "Hospital beds (per 1,000 people)",
            "Physicians (per 1,000 people)",
            "GDP per capita (current US$)",
            "Unemployment, total (% of total labor force)",
            "Urban population (% of total)"
        ]
        
        df_filtered = df[df['Indicator'].isin(relevant_indicators)]
        
        # Pivot the data to have indicators as columns
        df_pivot = df_filtered.pivot_table(
            index=['Country', 'Year'], 
            columns='Indicator', 
            values='Value'
        ).reset_index()
        
        # Rename columns for easier access
        df_pivot.columns.name = None
        df_pivot = df_pivot.rename(columns={
            "Health expenditure per capita (current US$)": "health_exp_per_capita",
            "Health expenditure, total (% of GDP)": "health_exp_pct_gdp",
            "Life expectancy at birth, total (years)": "life_expectancy",
            "Hospital beds (per 1,000 people)": "hospital_beds",
            "Physicians (per 1,000 people)": "physicians",
            "GDP per capita (current US$)": "gdp_per_capita",
            "Unemployment, total (% of total labor force)": "unemployment",
            "Urban population (% of total)": "urban_population"
        })
        
        # Save processed data
        output_file = os.path.join(processed_dir, "processed_health_data.csv")
        df_pivot.to_csv(output_file, index=False)
        logger.info(f"Processed data saved to {output_file}")
        
        # Print data summary
        logger.info(f"Data shape: {df_pivot.shape}")
        logger.info(f"Data columns: {df_pivot.columns.tolist()}")
        logger.info(f"Sample data:\n{df_pivot.head()}")
        
        return output_file
    except Exception as e:
        logger.error(f"Error processing health data: {e}")
        return None


def main():
    """
    Main function to download and process WHO health data.
    """
    # Setup Kaggle credentials
    api = setup_kaggle_credentials()
    if api is None:
        logger.warning("Proceeding without Kaggle API authentication. Will create mock data only.")
    
    # Create data directories
    raw_dir, processed_dir = create_data_directory()
    
    # Download WHO health data
    raw_file = download_who_health_data(api, raw_dir)
    if raw_file is None:
        logger.error("Failed to download/create WHO health data. Exiting.")
        return
    
    # Process health data
    processed_file = process_health_data(raw_file, processed_dir)
    if processed_file is None:
        logger.error("Failed to process health data. Exiting.")
        return
    
    logger.info("Data download and processing completed successfully.")


if __name__ == "__main__":
    main()