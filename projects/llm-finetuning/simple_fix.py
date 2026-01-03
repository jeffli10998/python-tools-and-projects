#!/usr/bin/env python3
"""
Simple Fix Script for LLM Fine-tuning Project
Addresses pip command execution issues on Windows
"""

import os
import sys
import subprocess

def run_pip_install(package):
    """Run pip install with proper error handling."""
    try:
        # Use different approaches to run pip
        commands = [
            [sys.executable, "-m", "pip", "install", package],
            ["pip", "install", package],
            ["python", "-m", "pip", "install", package]
        ]
        
        for cmd in commands:
            try:
                print(f"Trying: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print(f"✓ Successfully installed {package}")
                    return True
                else:
                    print(f"Command failed with return code {result.returncode}")
                    if result.stderr:
                        print(f"Error: {result.stderr[:100]}...")
            except FileNotFoundError:
                print(f"Command not found: {' '.join(cmd)}")
                continue
            except subprocess.TimeoutExpired:
                print(f"Command timed out: {' '.join(cmd)}")
                continue
            except Exception as e:
                print(f"Exception: {e}")
                continue
        
        print(f"✗ Failed to install {package}")
        return False
        
    except Exception as e:
        print(f"✗ Error installing {package}: {e}")
        return False

def check_and_install_pip():
    """Check if pip is working and try to fix it."""
    print("Checking pip installation...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ pip is working: {result.stdout.strip()}")
            return True
        else:
            print("✗ pip is not working properly")
    except Exception as e:
        print(f"✗ Error checking pip: {e}")
    
    # Try to install/upgrade pip
    print("Attempting to fix pip...")
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                      capture_output=True, text=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, text=True)
        print("✓ pip fix attempted")
        return True
    except Exception as e:
        print(f"✗ Failed to fix pip: {e}")
        return False

def install_essential_packages():
    """Install essential packages one by one."""
    print("\n" + "="*50)
    print("INSTALLING ESSENTIAL PACKAGES")
    print("="*50)
    
    # Essential packages in order of importance
    packages = [
        "pip",
        "setuptools",
        "wheel",
        "numpy",
        "psutil",
        "tqdm",
        "colorama",
        "pyyaml",
        "requests",
        "transformers",
        "tokenizers",
        "accelerate",
        "peft",
        "datasets"
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"\nInstalling {package}...")
        if run_pip_install(package):
            success_count += 1
        else:
            print(f"Skipping {package} - will try later")
    
    print(f"\nInstalled {success_count}/{len(packages)} packages")
    return success_count > len(packages) * 0.5  # 50% success rate

def verify_imports():
    """Verify that key packages can be imported."""
    print("\n" + "="*50)
    print("VERIFYING IMPORTS")
    print("="*50)
    
    test_imports = {
        'numpy': 'import numpy',
        'psutil': 'import psutil',
        'tqdm': 'import tqdm',
        'yaml': 'import yaml',
        'requests': 'import requests',
        'torch': 'import torch',
        'transformers': 'import transformers'
    }
    
    working_packages = []
    failed_packages = []
    
    for name, import_cmd in test_imports.items():
        try:
            exec(import_cmd)
            print(f"✓ {name} - OK")
            working_packages.append(name)
        except ImportError:
            print(f"✗ {name} - Failed")
            failed_packages.append(name)
        except Exception as e:
            print(f"✗ {name} - Error: {e}")
            failed_packages.append(name)
    
    print(f"\nWorking: {len(working_packages)} packages")
    print(f"Failed: {len(failed_packages)} packages")
    
    if failed_packages:
        print(f"Failed packages: {failed_packages}")
    
    return len(working_packages) >= 4  # At least 4 core packages working

def create_minimal_requirements():
    """Create a minimal requirements file that works."""
    print("\nCreating minimal requirements file...")
    
    minimal_reqs = """
# Minimal requirements that should work
numpy>=1.21.0
psutil>=5.8.0
tqdm>=4.60.0
colorama>=0.4.4
pyyaml>=5.4.0
requests>=2.25.0

# Install PyTorch separately:
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# ML packages (install after PyTorch):
# pip install transformers tokenizers accelerate peft datasets
"""
    
    try:
        with open('requirements_minimal.txt', 'w') as f:
            f.write(minimal_reqs)
        print("✓ Created requirements_minimal.txt")
        return True
    except Exception as e:
        print(f"✗ Failed to create minimal requirements: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("LLM Fine-tuning Project - SIMPLE FIX")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Step 1: Check and fix pip
    if not check_and_install_pip():
        print("\n⚠ Could not fix pip. Try running as administrator.")
        return False
    
    # Step 2: Install essential packages
    if not install_essential_packages():
        print("\n⚠ Most packages failed to install.")
        print("\nTry these manual steps:")
        print("1. Run as administrator")
        print("2. Use: python -m pip install --user <package>")
        print("3. Create virtual environment")
        return False
    
    # Step 3: Verify imports
    if verify_imports():
        print("\n✓ Core packages are working!")
        
        # Step 4: Install PyTorch with CUDA
        print("\nInstalling PyTorch with CUDA...")
        pytorch_cmd = "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
        if run_pip_install(pytorch_cmd):
            print("✓ PyTorch with CUDA installed")
        
        # Step 5: Create minimal requirements
        create_minimal_requirements()
        
        print("\n🎉 Simple fix completed!")
        print("\nNext steps:")
        print("1. Test: python train.py --check-only")
        print("2. Install remaining packages manually if needed")
        return True
    else:
        print("\n⚠ Core packages still not working.")
        print("\nRecommended solutions:")
        print("1. Create virtual environment:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate")
        print("   python -m pip install --upgrade pip")
        print("\n2. Or try installing with --user flag:")
        print("   python -m pip install --user numpy psutil tqdm")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)