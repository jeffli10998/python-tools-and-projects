@echo off
echo ============================================================
echo LLM Fine-tuning Project - Setup Fix for Windows
echo ============================================================
echo.

echo This script will fix the setup issues you encountered:
echo - Install PyTorch with CUDA support
echo - Fix dependency compatibility issues
echo - Verify system requirements
echo.

pause

echo.
echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Running setup fix...
python fix_setup.py

echo.
echo Step 3: Testing the installation...
python train.py --check-only

echo.
echo ============================================================
echo Setup fix completed!
echo ============================================================
echo.
echo If you still have issues, try creating a virtual environment:
echo   python fix_setup.py --create-venv
echo   venv\Scripts\activate
echo   python fix_setup.py
echo.
pause