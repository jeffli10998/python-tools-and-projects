@echo off
echo Healthcare Linear Regression - Data Download
echo =======================================

echo Running data download script...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

:: Run the download script
python src\download_data.py
if %errorlevel% neq 0 (
    echo Error: Data download failed.
    exit /b 1
)

echo Data download completed successfully!
echo Processed data is available in the 'data/processed' directory.

pause