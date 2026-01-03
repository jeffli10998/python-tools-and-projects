# Healthcare Linear Regression Analysis

This project analyzes the relationship between healthcare indicators and life expectancy using linear regression. It uses mock data based on the World Health Organization's Global Health Expenditure database to predict life expectancy based on economic and healthcare system variables.

## Project Structure

```
healthcare_linear_regression/
├── data/
│   ├── raw/             # Raw data downloaded from Kaggle (mock)
│   └── processed/       # Processed data ready for analysis
├── models/              # Saved model files
├── notebooks/           # Jupyter notebooks for analysis
├── results/             # Visualizations and analysis results
├── src/                 # Source code
│   ├── config.py        # Configuration settings
│   ├── download_data.py # Script to download and prepare data
│   ├── model.py         # Linear regression model implementation
│   ├── utils.py         # Utility functions
│   └── visualize.py     # Visualization functions
└── README.md            # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1.  Clone this repository or download the project files.

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv_healthcare
    .\venv_healthcare\Scripts\activate # On Windows
    ```

3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up Kaggle API credentials (if using real Kaggle data):
    - Create a Kaggle account if you don't have one
    - Go to your account settings and download the kaggle.json file
    - Place the file in ~/.kaggle/ directory or set KAGGLE_USERNAME and KAGGLE_KEY environment variables

## Usage

### 1. Data Preparation

First, ensure your data is prepared. You can run the data download script to create mock healthcare data:

```bash
python src/download_data.py
```

This script will:
- Create mock data based on WHO Global Health Expenditure patterns.
- Process the data for analysis.
- Save the processed data to `data/processed/processed_health_data.csv`.

### 2. Interactive Analysis with Jupyter Notebook

The primary way to interact with this project, build the model, and analyze outputs is through the Jupyter notebook.

1.  **Activate your virtual environment**:
    ```bash
    .\venv_healthcare\Scripts\activate # On Windows
    ```

2.  **Open the Jupyter notebook** in your Trae AI environment. If you encounter issues with kernel selection, ensure you have installed `ipykernel` in your virtual environment and registered it:
    ```bash
    pip install ipykernel
    python -m ipykernel install --user --name=venv_healthcare --display-name "Python (Healthcare Project)"
    ```
    Then restart Trae AI and select the "Python (Healthcare Project)" kernel.

3.  **Navigate to `notebooks/Healthcare_Analysis.ipynb`**.

4.  **Run all cells sequentially** within the notebook. The notebook is structured to guide you through:
    - **Data Loading and Exploration**: Loading the processed dataset and displaying its head, info, and descriptive statistics.
    - **Data Visualization**: Generating various plots (time series, scatter matrices, boxplots, heatmaps, pairplots) to understand the relationships between different healthcare indicators. These visualizations are saved to the `results/` directory.
    - **Model Training and Evaluation**:
        - Selecting features and the target variable (`life_expectancy`).
        - Splitting data into training and testing sets.
        - Scaling features using `StandardScaler`.
        - Training a Linear Regression model.
        - Evaluating the model using Mean Squared Error (MSE) and R-squared (R2) metrics.
        - Saving the trained model to the `models/` directory.
    - **Model Analysis**:
        - Visualizing actual vs. predicted life expectancy to assess model fit.
        - Plotting the distribution of residuals to check for model assumptions.
    - **Loading Saved Model**: Demonstrating how to load a previously saved model.

## Model Building Process and Outputs Explained

The `Healthcare_Analysis.ipynb` notebook provides a step-by-step guide to the model building process:

### Data Loading and Preprocessing
- **Input**: Raw data (mock `who_health_expenditure.csv`) is processed by `src/download_data.py` into `data/processed/processed_health_data.csv`.
- **Notebook Action**: The notebook loads `processed_health_data.csv` using `utils.load_data`.
- **Outputs**: Display of `df.head()`, `df.info()`, and `df.describe()` to show the structure and summary statistics of the clean, ready-to-use data.

### Data Visualization
- **Notebook Action**: Utilizes functions from `src/visualize.py` to generate various plots.
- **Outputs**:
    - **Time Series Plots**: Show trends of relevant indicators over time, saved in `results/`.
    - **Scatter Matrix**: Illustrates pairwise relationships between selected features, saved in `results/`.
    - **Boxplots**: Displays the distribution and potential outliers for each indicator, saved in `results/`.
    - **Correlation Heatmap**: Visualizes the correlation matrix of features, helping identify strong relationships, saved in `results/`.
    - **Pairplot**: Provides a comprehensive view of univariate distributions and pairwise relationships, saved in `results/`.

### Model Training
- **Input**: Processed data (`df`).
- **Notebook Action**:
    - Features are selected (all columns except 'life_expectancy' based on `config.COLUMN_MAPPINGS`).
    - Data is split into training and testing sets (`X_train`, `X_test`, `y_train`, `y_test`).
    - Features are scaled using `StandardScaler` to normalize their range.
    - A `LinearRegression` model is trained using `model.train_model` from `src/model.py`.
- **Outputs**: A trained `LinearRegression` model, which is then saved as `models/linear_regression_model.pkl` using `utils.save_model`.

### Model Evaluation
- **Input**: Trained model and test data (`X_test`, `y_test`).
- **Notebook Action**: The trained model makes predictions on the test set. `utils.evaluate_model` calculates performance metrics.
- **Outputs**:
    - **Mean Squared Error (MSE)**: A measure of the average squared difference between the estimated values and the actual value. Lower MSE indicates better fit.
    - **R-squared (R2)**: Represents the proportion of the variance in the dependent variable that is predictable from the independent variables. Higher R2 indicates a better fit.

### Model Analysis
- **Input**: Actual test values (`y_test`) and model predictions.
- **Notebook Action**: Visualizations are generated to analyze the model's performance and assumptions.
- **Outputs**:
    - **Actual vs. Predicted Plot**: A scatter plot comparing the actual life expectancy values against the model's predictions. A perfect model would show points lying perfectly on a 45-degree line.
    - **Residuals Distribution Plot**: A histogram of the differences between actual and predicted values (residuals). Ideally, residuals should be normally distributed around zero, indicating that the model's errors are random and unbiased.

## Analysis Features

This project analyzes the relationship between:

### Target Variable
- Life expectancy at birth (years)

### Predictor Variables
- Health expenditure per capita (current US$)
- Health expenditure as percentage of GDP
- Hospital beds per 1,000 people
- Physicians per 1,000 people
- GDP per capita (current US$)
- Unemployment rate
- Urban population percentage

## Results

The analysis provides insights into:

1.  The relationship between healthcare spending and life expectancy
2.  The impact of economic factors on health outcomes
3.  The relative importance of different healthcare system indicators
4.  Predictions of life expectancy based on economic and healthcare variables

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- World Health Organization for the original data that inspired this mock dataset
- Kaggle for providing access to datasets