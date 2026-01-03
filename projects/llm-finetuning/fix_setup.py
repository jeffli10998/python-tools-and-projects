#!/usr/bin/env python3
"""
Fix Setup Script for LLM Fine-tuning Project
Addresses Windows and Python 3.13 compatibility issues
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
            return False
    except Exception as e:
        print(f"✗ Error during {description}: {e}")
        return False

def check_python_version():
    """Check Python version compatibility."""
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python version not compatible (requires 3.8+)")
        return False

def install_pytorch_cuda():
    """Install PyTorch with CUDA support."""
    print("\n" + "="*50)
    print("INSTALLING PYTORCH WITH CUDA SUPPORT")
    print("="*50)
    
    # Uninstall existing PyTorch first
    print("\nUninstalling existing PyTorch...")
    uninstall_cmd = f"{sys.executable} -m pip uninstall torch torchvision torchaudio -y"
    subprocess.run(uninstall_cmd, shell=True, capture_output=True)
    
    # Install PyTorch with CUDA 11.8 support
    pytorch_cmd = (
        f"{sys.executable} -m pip install torch torchvision torchaudio "
        "--index-url https://download.pytorch.org/whl/cu118"
    )
    
    return run_command(pytorch_cmd, "Installing PyTorch with CUDA support")

def install_basic_dependencies():
    """Install basic dependencies first."""
    print("\n" + "="*50)
    print("INSTALLING BASIC DEPENDENCIES")
    print("="*50)
    
    # Install essential packages first
    essential_packages = [
        "numpy>=1.24.0,<2.0.0",
        "psutil>=5.9.0,<6.0.0",
        "tqdm>=4.65.0,<5.0.0",
        "colorama>=0.4.6,<1.0.0",
        "pyyaml>=6.0,<7.0.0",
        "requests>=2.31.0,<3.0.0",
        "typing-extensions>=4.0.0,<5.0.0",
        "chardet>=5.0.0,<6.0.0"
    ]
    
    for package in essential_packages:
        cmd = f"{sys.executable} -m pip install '{package}'"
        if not run_command(cmd, f"Installing {package.split('>=')[0]}"):
            print(f"Warning: Failed to install {package}")
    
    return True

def install_ml_dependencies():
    """Install ML-specific dependencies."""
    print("\n" + "="*50)
    print("INSTALLING ML DEPENDENCIES")
    print("="*50)
    
    ml_packages = [
        "transformers>=4.35.0,<5.0.0",
        "tokenizers>=0.14.0,<1.0.0",
        "datasets>=2.14.0,<3.0.0",
        "accelerate>=0.24.0,<1.0.0",
        "peft>=0.6.0,<1.0.0",
        "scipy>=1.11.0,<2.0.0",
        "pandas>=2.0.0,<3.0.0",
        "tensorboard>=2.14.0,<3.0.0",
        "sentencepiece>=0.1.99,<1.0.0",
        "jsonlines>=3.1.0,<4.0.0",
        "httpx>=0.24.0,<1.0.0"
    ]
    
    success_count = 0
    for package in ml_packages:
        cmd = f"{sys.executable} -m pip install '{package}'"
        if run_command(cmd, f"Installing {package.split('>=')[0]}"):
            success_count += 1
        else:
            print(f"Warning: Failed to install {package}")
    
    print(f"\nML Dependencies: {success_count}/{len(ml_packages)} installed successfully")
    return success_count > len(ml_packages) * 0.8  # 80% success rate

def try_install_bitsandbytes():
    """Try to install bitsandbytes (may fail on Windows)."""
    print("\n" + "="*50)
    print("ATTEMPTING BITSANDBYTES INSTALLATION")
    print("="*50)
    
    print("Note: bitsandbytes may not work on Windows. This is optional.")
    
    # Try different approaches
    approaches = [
        f"{sys.executable} -m pip install bitsandbytes>=0.41.0",
        f"{sys.executable} -m pip install bitsandbytes --no-deps",
        f"{sys.executable} -m pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.1-py3-none-win_amd64.whl"
    ]
    
    for i, cmd in enumerate(approaches, 1):
        print(f"\nTrying approach {i}...")
        if run_command(cmd, f"Installing bitsandbytes (approach {i})"):
            return True
    
    print("\n⚠ bitsandbytes installation failed. This is common on Windows.")
    print("  Training will work without it, but may use more memory.")
    return False

def verify_installation():
    """Verify the installation works."""
    print("\n" + "="*50)
    print("VERIFYING INSTALLATION")
    print("="*50)
    
    # Test PyTorch CUDA
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("✓ CUDA is available")
            print(f"✓ CUDA device count: {torch.cuda.device_count()}")
            if torch.cuda.device_count() > 0:
                print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
                memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"✓ GPU Memory: {memory_gb:.1f} GB")
        else:
            print("✗ CUDA is not available")
            return False
    except ImportError as e:
        print(f"✗ PyTorch import failed: {e}")
        return False
    
    # Test other key packages
    test_packages = ['transformers', 'peft', 'datasets', 'accelerate', 'psutil']
    failed_packages = []
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✓ {package} imported successfully")
        except ImportError:
            print(f"✗ {package} import failed")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠ Some packages failed to import: {failed_packages}")
        return False
    
    print("\n✓ All core packages verified successfully!")
    return True

def create_virtual_environment():
    """Create and activate virtual environment."""
    print("\n" + "="*50)
    print("VIRTUAL ENVIRONMENT SETUP")
    print("="*50)
    
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists: {venv_path}")
        return True
    
    # Create virtual environment
    cmd = f"{sys.executable} -m venv {venv_path}"
    if run_command(cmd, "Creating virtual environment"):
        print(f"\n✓ Virtual environment created: {venv_path}")
        print("\nTo activate it, run:")
        print(f"  {venv_path}\\Scripts\\activate")
        return True
    
    return False

def main():
    """Main fix setup function."""
    print("=" * 60)
    print("LLM Fine-tuning Project - SETUP FIX")
    print("=" * 60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check if we should create virtual environment
    if len(sys.argv) > 1 and sys.argv[1] == "--create-venv":
        if not create_virtual_environment():
            print("Failed to create virtual environment")
            return False
        print("\nPlease activate the virtual environment and run this script again.")
        return True
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies step by step
    steps = [
        ("Basic Dependencies", install_basic_dependencies),
        ("PyTorch with CUDA", install_pytorch_cuda),
        ("ML Dependencies", install_ml_dependencies),
        ("BitsAndBytes (Optional)", try_install_bitsandbytes),
        ("Verification", verify_installation)
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except KeyboardInterrupt:
            print("\n\nSetup interrupted by user")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error in {step_name}: {e}")
            results[step_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SETUP FIX SUMMARY")
    print("="*60)
    
    for step_name, result in results.items():
        status = "✓ SUCCESS" if result else "✗ FAILED"
        print(f"{step_name:<30} {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    if success_count >= total_count - 1:  # Allow BitsAndBytes to fail
        print("\n🎉 Setup fix completed successfully!")
        print("\nNext steps:")
        print("1. Test the system: python train.py --check-only")
        print("2. Create sample data: python train.py --create-sample")
        print("3. Start training: python train.py")
        return True
    else:
        print(f"\n⚠ Setup fix incomplete: {total_count - success_count} critical issues remain")
        print("\nTry running with --create-venv to use a clean virtual environment:")
        print("  python fix_setup.py --create-venv")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)