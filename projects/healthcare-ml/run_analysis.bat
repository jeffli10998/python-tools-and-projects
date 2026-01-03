@echo off
echo Healthcare Linear Regression Analysis
echo ===================================

echo Setting up environment...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements.
    exit /b 1
)

:: Create necessary directories
echo Creating directories...
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed
if not exist models mkdir models
if not exist results mkdir results
if not exist logs mkdir logs

:: Run the analysis pipeline
echo Running analysis pipeline...
python src\run_analysis.py
if %errorlevel% neq 0 (
    echo Error: Analysis pipeline failed.
    exit /b 1
)

echo Analysis completed successfully!
echo Results are available in the 'results' directory.

:: Deactivate virtual environment
call venv\Scripts\deactivate

pause