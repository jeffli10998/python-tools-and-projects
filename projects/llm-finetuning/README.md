# LLM Fine-tuning with LoRA for NVIDIA GTX 1060

This project provides a complete pipeline for fine-tuning Large Language Models (LLMs) using LoRA (Low-Rank Adaptation) techniques, specifically optimized for NVIDIA GTX 1060 graphics cards with 6GB VRAM.

## 🎯 Project Overview

This fine-tuning pipeline allows you to:
- Fine-tune Ollama models locally using your own data
- Use LoRA techniques for memory-efficient training
- Optimize performance for GTX 1060 (6GB VRAM)
- Process various data formats (TXT, CSV, JSON, JSONL)
- Monitor training progress and evaluate results
- Deploy fine-tuned models for inference

## 📁 Project Structure

```
llm-finetuning-project/
├── configs/
│   └── lora_config.yaml          # LoRA training configuration
├── data/
│   └── (your training data)      # Training data directory
├── models/
│   └── (downloaded models)       # Base models storage
├── outputs/
│   ├── logs/                     # Training logs
│   ├── checkpoints/              # Model checkpoints
│   └── final_model/              # Final trained model
├── scripts/
│   ├── finetune_lora.py          # Main LoRA fine-tuning script
│   ├── prepare_data.py           # Data preparation utilities
│   └── evaluate_model.py         # Model evaluation tools
├── train.py                      # Main training orchestrator
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. System Requirements

**Hardware:**
- NVIDIA GTX 1060 (6GB VRAM) or better
- 8GB+ System RAM (16GB recommended)
- 10GB+ free disk space

**Software:**
- Windows 10/11
- Python 3.8+
- CUDA 11.8+ (compatible with PyTorch)
- Ollama installed and running

### 2. Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\py_workspace\learning\llm-finetuning-project
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify system compatibility:**
   ```bash
   python train.py --check-only
   ```

### 3. Prepare Your Data

#### Option A: Use Sample Data (for testing)
```bash
python train.py --create-sample
```

#### Option B: Use Your Own Data

1. **Place your data in the `data/` directory**
   - Supported formats: `.txt`, `.csv`, `.json`, `.jsonl`
   - For multiple files, create subdirectories

2. **Prepare data for training:**
   ```bash
   python train.py --data-source data/your_data_file.txt
   # or for a directory
   python train.py --data-source data/your_data_directory/
   ```

#### Data Format Requirements

Your data should be in instruction-response format. Examples:

**Text files (.txt):**
```
Instruction: What is machine learning?
Response: Machine learning is a subset of artificial intelligence...

Instruction: Explain neural networks.
Response: Neural networks are computing systems inspired by...
```

**JSON files (.json):**
```json
[
  {
    "instruction": "What is machine learning?",
    "response": "Machine learning is a subset of artificial intelligence..."
  },
  {
    "instruction": "Explain neural networks.",
    "response": "Neural networks are computing systems inspired by..."
  }
]
```

### 4. Configure Training

Edit `configs/lora_config.yaml` to customize training parameters:

```yaml
# Key parameters for GTX 1060 optimization
model:
  load_in_8bit: true              # Essential for 6GB VRAM
  
lora:
  r: 16                           # LoRA rank (lower = less memory)
  lora_alpha: 32                  # LoRA scaling parameter
  
training:
  per_device_train_batch_size: 1  # Small batch size for memory
  gradient_accumulation_steps: 8   # Simulate larger batches
  max_steps: 1000                 # Adjust based on data size
  learning_rate: 2e-4             # Conservative learning rate
  fp16: true                      # Half precision for memory savings
```

### 5. Start Training

#### Basic Training
```bash
python train.py
```

#### Training with Custom Data
```bash
python train.py --data-source data/my_training_data.jsonl
```

#### Training with Evaluation
```bash
python train.py --evaluate
```

#### Interactive Training (with chat interface)
```bash
python train.py --interactive
```

## 📊 Monitoring Training

### Real-time Monitoring

During training, monitor:
- **GPU Memory Usage**: Should stay under 6GB
- **Training Loss**: Should decrease over time
- **System Resources**: CPU and RAM usage

### Log Files

- `training.log`: Detailed training logs
- `outputs/logs/`: TensorBoard logs (if enabled)
- `outputs/training_summary.json`: Final training statistics

### TensorBoard (Optional)

If TensorBoard logging is enabled:
```bash
tensorboard --logdir outputs/logs
```

## 🔧 Advanced Usage

### Custom Configuration

Create custom config files for different experiments:

```bash
# Copy default config
cp configs/lora_config.yaml configs/my_experiment.yaml

# Edit your config
# ... modify parameters ...

# Train with custom config
python train.py --config configs/my_experiment.yaml
```

### Batch Processing Multiple Datasets

```bash
# Process multiple data sources
python scripts/prepare_data.py --input data/dataset1/ --output data/combined_training.jsonl
python scripts/prepare_data.py --input data/dataset2/ --output data/combined_training.jsonl --append

# Train on combined data
python train.py --data-source data/combined_training.jsonl
```

### Model Evaluation

```bash
# Evaluate trained model
python scripts/evaluate_model.py --base-model meta-llama/Llama-2-7b-hf --lora-model outputs/ --mode interactive

# Benchmark performance
python scripts/evaluate_model.py --base-model meta-llama/Llama-2-7b-hf --lora-model outputs/ --mode benchmark
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory
```
RuntimeError: CUDA out of memory
```

**Solutions:**
- Reduce `per_device_train_batch_size` to 1
- Increase `gradient_accumulation_steps`
- Enable `load_in_8bit: true`
- Reduce `max_seq_length`
- Lower LoRA rank (`r` parameter)

#### 2. Slow Training
```
Training is very slow
```

**Solutions:**
- Enable `fp16: true`
- Increase `per_device_train_batch_size` if memory allows
- Reduce `max_seq_length`
- Use `dataloader_num_workers: 0` on Windows

#### 3. Model Not Loading
```
Error loading base model
```

**Solutions:**
- Check Ollama is running: `ollama list`
- Verify model name in config
- Ensure sufficient disk space
- Check internet connection for model download

#### 4. Data Format Errors
```
Data validation failed
```

**Solutions:**
- Check data format matches requirements
- Ensure proper encoding (UTF-8)
- Validate JSON syntax
- Check for empty or malformed entries

### Performance Optimization

#### For GTX 1060 (6GB VRAM):

```yaml
# Optimal settings for 6GB VRAM
model:
  load_in_8bit: true
  device_map: "auto"

lora:
  r: 8                    # Lower rank for less memory
  lora_alpha: 16
  target_modules: ["q_proj", "v_proj"]  # Fewer modules

training:
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 16
  max_seq_length: 512     # Shorter sequences
  fp16: true
  dataloader_num_workers: 0
```

#### For Better GPUs (8GB+ VRAM):

```yaml
# Enhanced settings for more VRAM
lora:
  r: 16
  lora_alpha: 32
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj"]

training:
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  max_seq_length: 1024
```

## 📈 Expected Results

### Training Time
- **Small dataset (100-500 samples)**: 30-60 minutes
- **Medium dataset (500-2000 samples)**: 1-3 hours
- **Large dataset (2000+ samples)**: 3-8 hours

### Memory Usage
- **Base model loading**: ~3-4GB VRAM
- **Training peak**: ~5-5.5GB VRAM
- **System RAM**: ~4-8GB

### Quality Expectations
- **Noticeable improvement**: 100+ high-quality samples
- **Good performance**: 500+ samples
- **Excellent results**: 1000+ samples

## 🔄 Next Steps

### After Training

1. **Evaluate your model:**
   ```bash
   python train.py --evaluate --interactive
   ```

2. **Test with your specific use cases:**
   ```bash
   python scripts/evaluate_model.py --mode interactive
   ```

3. **Deploy for production use:**
   - Export model for Ollama
   - Create API endpoints
   - Integrate with applications

### Iterative Improvement

1. **Collect more data** based on model weaknesses
2. **Adjust hyperparameters** for better performance
3. **Experiment with different base models**
4. **Fine-tune on specific domains**

## 📚 Additional Resources

- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft)
- [Ollama Documentation](https://ollama.ai/docs)
- [PyTorch Documentation](https://pytorch.org/docs/)

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review log files in `outputs/logs/`
3. Verify system requirements
4. Check GPU memory usage with `nvidia-smi`

## 📄 License

This project is provided as-is for educational and research purposes.

---

**Happy Fine-tuning! 🚀**