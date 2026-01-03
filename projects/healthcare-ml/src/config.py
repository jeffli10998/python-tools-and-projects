# Configuration settings for the healthcare linear regression project

# Data processing parameters
DATA_PROCESSING = {
    'test_size': 0.2,
    'random_state': 42,
    'target_column': 'life_expectancy',
    'exclude_columns': ['Country', 'Year'],
}

# Model parameters
MODEL_PARAMS = {
    'fit_intercept': True,
    'normalize': False,
}

# Visualization settings
VISUALIZATION = {
    'figure_size_large': (14, 10),
    'figure_size_medium': (12, 8),
    'figure_size_small': (10, 6),
    'style': 'whitegrid',
    'cmap': 'coolwarm',
    'line_color': 'red',
    'line_style': '--',
    'alpha': 0.6,
}

# File paths
PATHS = {
    'raw_data_dir': '../data/raw',
    'processed_data_dir': '../data/processed',
    'models_dir': '../models',
    'results_dir': '../results',
    'raw_data_file': '../data/raw/who_health_expenditure.csv',
    'processed_data_file': '../data/processed/processed_health_data.csv',
    'model_file': '../models/linear_regression_model.pkl',
    'scaler_file': '../models/scaler.pkl',
    'feature_names_file': '../models/feature_names.pkl',
}

# Logging settings
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': '../logs/healthcare_regression.log',
}

# Relevant indicators for analysis
RELEVANT_INDICATORS = [
    "Health expenditure per capita (current US$)",
    "Health expenditure, total (% of GDP)",
    "Life expectancy at birth, total (years)",
    "Hospital beds (per 1,000 people)",
    "Physicians (per 1,000 people)",
    "GDP per capita (current US$)",
    "Unemployment, total (% of total labor force)",
    "Urban population (% of total)"
]

# Column name mappings for processed data
COLUMN_MAPPINGS = {
    "Health expenditure per capita (current US$)": "health_exp_per_capita",
    "Health expenditure, total (% of GDP)": "health_exp_pct_gdp",
    "Life expectancy at birth, total (years)": "life_expectancy",
    "Hospital beds (per 1,000 people)": "hospital_beds",
    "Physicians (per 1,000 people)": "physicians",
    "GDP per capita (current US$)": "gdp_per_capita",
    "Unemployment, total (% of total labor force)": "unemployment",
    "Urban population (% of total)": "urban_population"
}