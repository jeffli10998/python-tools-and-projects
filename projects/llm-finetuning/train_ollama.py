#!/usr/bin/env python3
"""
Ollama Model Fine-tuning Main Script
This script provides a complete pipeline for fine-tuning models for Ollama deployment
"""

import os
import sys
import argparse
import logging
import psutil
import torch
from pathlib import Path

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from finetune_ollama import OllamaFineTuner

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaTrainingManager:
    def __init__(self, config_path: str = "./configs/ollama_config.yaml"):
        """Initialize the Ollama training manager."""
        self.config_path = config_path
        
    def check_system_requirements(self):
        """Check if system meets requirements for training."""
        logger.info("Checking system requirements...")
        
        # Check GPU
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"GPU: {gpu_name} ({gpu_memory:.1f} GB memory)")
            
            if gpu_memory < 4.0:
                logger.warning("GPU memory is less than 4GB. Training may be slow or fail.")
                return False
        else:
            logger.warning("No CUDA GPU detected. Training will be very slow on CPU.")
            return False
        
        # Check system RAM
        ram_gb = psutil.virtual_memory().total / 1024**3
        logger.info(f"System RAM: {ram_gb:.1f} GB")
        
        if ram_gb < 8.0:
            logger.warning("System RAM is less than 8GB. Training may fail.")
            return False
        
        # Check disk space
        disk_usage = psutil.disk_usage('.')
        free_gb = disk_usage.free / 1024**3
        logger.info(f"Free disk space: {free_gb:.1f} GB")
        
        if free_gb < 10.0:
            logger.warning("Less than 10GB free disk space. Training may fail.")
            return False
        
        logger.info("✓ System requirements check passed")
        return True
    
    def check_ollama_installation(self):
        """Check if Ollama is installed and running."""
        logger.info("Checking Ollama installation...")
        
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
            logger.info("✓ Ollama is installed and accessible")
            
            # Show available models
            if result.stdout.strip():
                logger.info("Available Ollama models:")
                for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                    if line.strip():
                        logger.info(f"  - {line.split()[0]}")
            else:
                logger.warning("No Ollama models found. You may need to pull a model first.")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Ollama command failed: {e}")
            return False
        except FileNotFoundError:
            logger.error("Ollama not found. Please install Ollama first.")
            logger.info("Install from: https://ollama.ai/")
            return False
    
    def check_training_data(self):
        """Check if training data exists and is valid."""
        logger.info("Checking training data...")
        
        data_path = "./data/training_data.jsonl"
        if not os.path.exists(data_path):
            logger.error(f"Training data not found: {data_path}")
            logger.info("Please prepare your training data first.")
            return False
        
        # Check data format
        try:
            import json
            with open(data_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line:
                    data = json.loads(first_line)
                    if 'instruction' not in data or 'response' not in data:
                        logger.error("Training data must have 'instruction' and 'response' fields")
                        return False
                    
            logger.info("✓ Training data format is valid")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in training data: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking training data: {e}")
            return False
    
    def run_training(self, ollama_model: str = "dolphin-llama3:8b", output_name: str = None, check_only: bool = False):
        """Run the complete training pipeline."""
        logger.info("Starting Ollama fine-tuning pipeline...")
        
        # System checks
        if not self.check_system_requirements():
            logger.error("System requirements not met. Aborting.")
            return False
        
        if not self.check_ollama_installation():
            logger.error("Ollama installation check failed. Aborting.")
            return False
        
        if not self.check_training_data():
            logger.error("Training data check failed. Aborting.")
            return False
        
        if check_only:
            logger.info("✓ All checks passed. Ready for training.")
            return True
        
        # Initialize fine-tuner
        try:
            fine_tuner = OllamaFineTuner(self.config_path, ollama_model)
            fine_tuner.run_full_pipeline(output_name)
            
            logger.info("🎉 Fine-tuning completed successfully!")
            logger.info(f"Your custom model is ready to use with Ollama.")
            return True
            
        except KeyboardInterrupt:
            logger.info("Training interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False
    
    def list_ollama_models(self):
        """List available Ollama models."""
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
            print("Available Ollama models:")
            print(result.stdout)
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Fine-tune models for Ollama deployment")
    parser.add_argument("--config", default="./configs/ollama_config.yaml", help="Configuration file path")
    parser.add_argument("--ollama-model", default="dolphin-llama3:8b", help="Base Ollama model to fine-tune")
    parser.add_argument("--output-name", help="Name for the fine-tuned model")
    parser.add_argument("--check-only", action="store_true", help="Only run system checks")
    parser.add_argument("--list-models", action="store_true", help="List available Ollama models")
    
    args = parser.parse_args()
    
    # Initialize training manager
    trainer = OllamaTrainingManager(args.config)
    
    if args.list_models:
        trainer.list_ollama_models()
        return
    
    # Run training
    success = trainer.run_training(
        ollama_model=args.ollama_model,
        output_name=args.output_name,
        check_only=args.check_only
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()