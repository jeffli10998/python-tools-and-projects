#!/usr/bin/env python3
"""
Setup Script for LLM Fine-tuning Project
Helps users set up their environment and verify system compatibility
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("  Required: Python 3.8 or higher")
        return False

def check_cuda():
    """Check CUDA installation."""
    print("\nChecking CUDA installation...")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✓ NVIDIA GPU detected")
            # Extract CUDA version from nvidia-smi output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'CUDA Version:' in line:
                    cuda_version = line.split('CUDA Version:')[1].strip().split()[0]
                    print(f"✓ CUDA Version: {cuda_version}")
                    break
            return True
        else:
            print("✗ nvidia-smi command failed")
            return False
    except FileNotFoundError:
        print("✗ nvidia-smi not found - NVIDIA drivers may not be installed")
        return False
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        return False

def check_ollama():
    """Check if Ollama is installed and running."""
    print("\nChecking Ollama installation...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✓ Ollama is installed and running")
            models = result.stdout.strip().split('\n')[1:]  # Skip header
            if models and models[0].strip():
                print(f"✓ Available models: {len(models)}")
                for model in models[:3]:  # Show first 3 models
                    model_name = model.split()[0] if model.strip() else "Unknown"
                    print(f"  - {model_name}")
                if len(models) > 3:
                    print(f"  ... and {len(models) - 3} more")
            else:
                print("! No models found - you may need to download a model")
                print("  Example: ollama pull llama2:7b")
            return True
        else:
            print("✗ Ollama command failed")
            print("  Make sure Ollama is installed and running")
            return False
    except FileNotFoundError:
        print("✗ Ollama not found")
        print("  Please install Ollama from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    print("\nChecking disk space...")
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free / (1024**3)
        total_gb = total / (1024**3)
        
        print(f"✓ Total disk space: {total_gb:.1f} GB")
        print(f"✓ Free disk space: {free_gb:.1f} GB")
        
        if free_gb >= 10:
            print("✓ Sufficient disk space available")
            return True
        else:
            print("⚠ Warning: Less than 10GB free space")
            print("  Recommended: At least 10GB for models and outputs")
            return False
    except Exception as e:
        print(f"✗ Error checking disk space: {e}")
        return False

def create_directories():
    """Create necessary project directories."""
    print("\nCreating project directories...")
    directories = [
        "data",
        "models", 
        "outputs",
        "outputs/logs",
        "outputs/checkpoints",
        "outputs/final_model"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {directory}/")
        except Exception as e:
            print(f"✗ Failed to create {directory}/: {e}")
            return False
    
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")
    
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False
    
    try:
        print("Installing packages (this may take a few minutes)...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print("✗ Failed to install dependencies")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def verify_pytorch_cuda():
    """Verify PyTorch CUDA installation."""
    print("\nVerifying PyTorch CUDA support...")
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("✓ CUDA is available in PyTorch")
            print(f"✓ CUDA device count: {torch.cuda.device_count()}")
            if torch.cuda.device_count() > 0:
                device_name = torch.cuda.get_device_name(0)
                memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"✓ GPU: {device_name}")
                print(f"✓ GPU Memory: {memory_gb:.1f} GB")
                
                if memory_gb >= 4:
                    print("✓ Sufficient GPU memory for LoRA training")
                    return True
                else:
                    print("⚠ Warning: Less than 4GB GPU memory")
                    print("  Training may be limited")
                    return False
        else:
            print("✗ CUDA is not available in PyTorch")
            print("  You may need to reinstall PyTorch with CUDA support")
            return False
    except ImportError:
        print("✗ PyTorch not installed")
        print("  Run: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        return False
    except Exception as e:
        print(f"✗ Error verifying PyTorch: {e}")
        return False

def create_sample_config():
    """Create a sample configuration if none exists."""
    config_path = Path("configs/lora_config.yaml")
    if config_path.exists():
        print(f"✓ Configuration file already exists: {config_path}")
        return True
    
    print("\nCreating sample configuration...")
    try:
        # The config file should already exist from previous setup
        if config_path.exists():
            print(f"✓ Configuration ready: {config_path}")
            return True
        else:
            print(f"⚠ Configuration file not found: {config_path}")
            print("  Please ensure configs/lora_config.yaml exists")
            return False
    except Exception as e:
        print(f"✗ Error with configuration: {e}")
        return False

def run_system_check():
    """Run the system compatibility check."""
    print("\nRunning system compatibility check...")
    try:
        result = subprocess.run([sys.executable, 'train.py', '--check-only'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ System compatibility check passed")
            return True
        else:
            print("✗ System compatibility check failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error running system check: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("LLM Fine-tuning Project Setup")
    print("=" * 60)
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Working directory: {os.getcwd()}")
    
    # Track setup progress
    checks = [
        ("Python Version", check_python_version),
        ("CUDA Installation", check_cuda),
        ("Ollama Installation", check_ollama),
        ("Disk Space", check_disk_space),
        ("Project Directories", create_directories),
        ("Python Dependencies", install_dependencies),
        ("PyTorch CUDA", verify_pytorch_cuda),
        ("Configuration", create_sample_config),
        ("System Check", run_system_check)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            results[check_name] = check_func()
        except KeyboardInterrupt:
            print("\n\nSetup interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Unexpected error in {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SETUP SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Prepare your training data:")
        print("   python train.py --create-sample  # For testing")
        print("   python train.py --data-source data/your_data.txt  # For real data")
        print("\n2. Start training:")
        print("   python train.py")
        print("\n3. Evaluate results:")
        print("   python train.py --evaluate --interactive")
        print("\nFor more information, see README.md")
    else:
        print(f"\n⚠ Setup incomplete: {total - passed} issues need to be resolved")
        print("\nPlease address the failed checks above before proceeding.")
        print("See README.md for troubleshooting guidance.")
    
    # Save setup results
    setup_results = {
        'timestamp': str(subprocess.run(['date', '/t'], capture_output=True, text=True, shell=True).stdout.strip()),
        'platform': platform.system(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'checks': results,
        'success': passed == total
    }
    
    try:
        with open('setup_results.json', 'w') as f:
            json.dump(setup_results, f, indent=2)
        print(f"\nSetup results saved to: setup_results.json")
    except Exception as e:
        print(f"Warning: Could not save setup results: {e}")

if __name__ == "__main__":
    main()