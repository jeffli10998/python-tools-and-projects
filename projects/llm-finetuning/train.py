#!/usr/bin/env python3
"""
Main Training Script for LoRA Fine-tuning on GTX 1060
Orchestrates the complete fine-tuning pipeline with monitoring and error handling
"""

import os
import sys
import argparse
import logging
import torch
import psutil
from pathlib import Path
from datetime import datetime
import json
import time

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / "scripts"))

from scripts.finetune_lora import LoRAFineTuner
from scripts.prepare_data import DataPreparator
from scripts.evaluate_model import ModelEvaluator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrainingOrchestrator:
    def __init__(self, config_path: str = "configs/lora_config.yaml"):
        """Initialize the training orchestrator."""
        self.config_path = config_path
        self.start_time = None
        self.training_stats = {}
        
    def check_system_requirements(self) -> bool:
        """Check if system meets requirements for training."""
        logger.info("Checking system requirements...")
        
        # Check CUDA availability
        if not torch.cuda.is_available():
            logger.error("CUDA is not available. GPU training is required.")
            return False
        
        # Check GPU memory
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {gpu_memory:.1f} GB")
        
        if gpu_memory < 4.0:  # Minimum 4GB for LoRA training
            logger.error("Insufficient GPU memory. At least 4GB required.")
            return False
        
        # Check RAM
        ram_gb = psutil.virtual_memory().total / 1024**3
        logger.info(f"System RAM: {ram_gb:.1f} GB")
        
        if ram_gb < 8.0:  # Minimum 8GB RAM recommended
            logger.warning("Low system RAM. At least 8GB recommended.")
        
        # Check disk space
        disk_usage = psutil.disk_usage('.')
        free_gb = disk_usage.free / 1024**3
        logger.info(f"Free disk space: {free_gb:.1f} GB")
        
        if free_gb < 10.0:  # Minimum 10GB for models and outputs
            logger.error("Insufficient disk space. At least 10GB required.")
            return False
        
        logger.info("System requirements check passed!")
        return True
    
    def setup_directories(self):
        """Ensure all required directories exist."""
        logger.info("Setting up directories...")
        
        directories = [
            "data",
            "models",
            "outputs",
            "outputs/logs",
            "outputs/checkpoints",
            "outputs/final_model"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {directory}")
    
    def prepare_training_data(self, data_source: str = None, create_sample: bool = False) -> bool:
        """Prepare training data."""
        logger.info("Preparing training data...")
        
        preparator = DataPreparator()
        
        # Use user's specified data directory as default
        if data_source is None:
            data_source = "C:\\py_workspace\\learning\\llm-training-project\\llm_env\\your_data"
            logger.info(f"Using default data directory: {data_source}")
        
        if create_sample:
            # Create sample data for demonstration
            sample_path = "data/training_data.jsonl"
            preparator.create_sample_data(sample_path)
            logger.info(f"Sample training data created: {sample_path}")
            return True
        
        elif data_source:
            # Process provided data source
            if os.path.exists(data_source):
                if os.path.isfile(data_source):
                    data = preparator.process_file(data_source)
                elif os.path.isdir(data_source):
                    data = preparator.process_directory(data_source)
                else:
                    logger.error(f"Invalid data source: {data_source}")
                    return False
                
                if preparator.validate_data(data):
                    output_path = "data/training_data.jsonl"
                    preparator.save_jsonl(data, output_path)
                    logger.info(f"Training data prepared: {output_path}")
                    return True
                else:
                    logger.error("Data validation failed")
                    return False
            else:
                logger.error(f"Data source not found: {data_source}")
                return False
        
        else:
            # Check if training data already exists
            training_data_path = "data/training_data.jsonl"
            if os.path.exists(training_data_path):
                logger.info(f"Using existing training data: {training_data_path}")
                return True
            else:
                logger.error("No training data found. Please provide --data-source or use --create-sample")
                return False
    
    def monitor_training_progress(self, output_dir: str):
        """Monitor training progress and log statistics."""
        logger.info("Monitoring training progress...")
        
        # This would be called periodically during training
        # For now, we'll just log system stats
        
        if torch.cuda.is_available():
            gpu_memory_used = torch.cuda.memory_allocated() / 1024**3
            gpu_memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            gpu_utilization = (gpu_memory_used / gpu_memory_total) * 100
            
            logger.info(f"GPU Memory Usage: {gpu_memory_used:.1f}/{gpu_memory_total:.1f} GB ({gpu_utilization:.1f}%)")
        
        # Log system memory usage
        memory = psutil.virtual_memory()
        logger.info(f"System Memory Usage: {memory.percent:.1f}%")
        
        # Log CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        logger.info(f"CPU Usage: {cpu_percent:.1f}%")
    
    def run_training(self) -> bool:
        """Run the actual training process."""
        logger.info("Starting LoRA fine-tuning...")
        
        try:
            # Initialize fine-tuner
            finetuner = LoRAFineTuner(self.config_path)
            
            # Record start time
            self.start_time = time.time()
            
            # Run fine-tuning
            finetuner.run_finetuning()
            
            # Record end time and calculate duration
            end_time = time.time()
            training_duration = end_time - self.start_time
            
            self.training_stats = {
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'end_time': datetime.fromtimestamp(end_time).isoformat(),
                'duration_seconds': training_duration,
                'duration_formatted': f"{training_duration // 3600:.0f}h {(training_duration % 3600) // 60:.0f}m {training_duration % 60:.0f}s"
            }
            
            logger.info(f"Training completed successfully in {self.training_stats['duration_formatted']}")
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False
    
    def evaluate_model(self, interactive: bool = False) -> bool:
        """Evaluate the trained model."""
        logger.info("Evaluating trained model...")
        
        try:
            # Check if model exists
            model_path = "outputs"
            if not os.path.exists(model_path):
                logger.error(f"Trained model not found: {model_path}")
                return False
            
            # Initialize evaluator
            evaluator = ModelEvaluator(
                base_model_path="microsoft/DialoGPT-medium",
                lora_model_path=model_path,
                use_8bit=True
            )
            
            # Load model
            evaluator.load_model()
            
            if interactive:
                # Start interactive chat
                evaluator.interactive_chat()
            else:
                # Run benchmark
                metrics = evaluator.benchmark_performance()
                
                # Save evaluation results
                eval_results = {
                    'evaluation_time': datetime.now().isoformat(),
                    'metrics': metrics,
                    'training_stats': self.training_stats
                }
                
                with open('outputs/evaluation_results.json', 'w') as f:
                    json.dump(eval_results, f, indent=2)
                
                logger.info("Evaluation completed and results saved")
            
            return True
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return False
    
    def cleanup_and_finalize(self):
        """Clean up temporary files and finalize training."""
        logger.info("Finalizing training...")
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Create training summary
        summary = {
            'training_completed': True,
            'config_used': self.config_path,
            'training_stats': self.training_stats,
            'system_info': {
                'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
                'gpu_memory_gb': torch.cuda.get_device_properties(0).total_memory / 1024**3 if torch.cuda.is_available() else 0,
                'system_memory_gb': psutil.virtual_memory().total / 1024**3,
                'python_version': sys.version,
                'pytorch_version': torch.__version__
            }
        }
        
        with open('outputs/training_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Training summary saved to outputs/training_summary.json")
        logger.info("Training pipeline completed successfully!")

def main():
    parser = argparse.ArgumentParser(description="LoRA Fine-tuning Pipeline for GTX 1060")
    parser.add_argument("--config", type=str, default="configs/lora_config.yaml", help="Configuration file path")
    parser.add_argument("--data-source", type=str, help="Path to training data (file or directory)")
    parser.add_argument("--create-sample", action="store_true", help="Create sample training data")
    parser.add_argument("--skip-training", action="store_true", help="Skip training (for testing)")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate model after training")
    parser.add_argument("--interactive", action="store_true", help="Start interactive chat after training")
    parser.add_argument("--check-only", action="store_true", help="Only check system requirements")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = TrainingOrchestrator(args.config)
    
    try:
        # Check system requirements
        if not orchestrator.check_system_requirements():
            logger.error("System requirements not met. Exiting.")
            sys.exit(1)
        
        if args.check_only:
            logger.info("System check completed. Ready for training!")
            return
        
        # Setup directories
        orchestrator.setup_directories()
        
        # Prepare training data
        if not orchestrator.prepare_training_data(args.data_source, args.create_sample):
            logger.error("Failed to prepare training data. Exiting.")
            sys.exit(1)
        
        # Run training
        if not args.skip_training:
            if not orchestrator.run_training():
                logger.error("Training failed. Exiting.")
                sys.exit(1)
        
        # Evaluate model
        if args.evaluate or args.interactive:
            orchestrator.evaluate_model(args.interactive)
        
        # Cleanup and finalize
        orchestrator.cleanup_and_finalize()
        
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()