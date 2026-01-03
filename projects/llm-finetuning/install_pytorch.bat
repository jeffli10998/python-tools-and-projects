@echo off
echo ============================================
echo Installing PyTorch with CUDA 11.8 Support
echo ============================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo Installing PyTorch with CUDA 11.8...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if %errorlevel% neq 0 (
    echo Failed to install PyTorch with CUDA
    echo Trying CPU version as fallback...
    python -m pip install torch torchvision torchaudio
)

echo.
echo Installing ML packages...
python -m pip install transformers tokenizers accelerate peft datasets
if %errorlevel% neq 0 (
    echo Some ML packages failed to install
    echo You can install them manually later
)

echo.
echo Attempting to install bitsandbytes...
python -m pip install bitsandbytes
if %errorlevel% neq 0 (
    echo bitsandbytes failed to install (common on Windows)
    echo This is optional for basic functionality
)

echo.
echo Testing PyTorch CUDA...
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else "N/A"}'); print(f'GPU count: {torch.cuda.device_count()}'); print(f'GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"}')"

echo.
echo Running system check...
python train.py --check-only

echo.
echo ============================================
echo Installation completed!
echo ============================================
echo.
echo If PyTorch CUDA is not working, try:
echo 1. Update your NVIDIA drivers
echo 2. Install CUDA 11.8 from NVIDIA website
echo 3. Restart your computer
echo.
pause