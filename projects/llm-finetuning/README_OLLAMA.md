# Ollama Model Fine-tuning

This project now supports fine-tuning your locally installed Ollama models using LoRA (Low-Rank Adaptation) for efficient training on consumer GPUs.

## Overview

The new Ollama fine-tuning approach allows you to:
- Fine-tune your existing Ollama models with custom data
- Create LoRA adapters that work with Ollama
- Deploy fine-tuned models directly to Ollama
- Maintain compatibility with your local Ollama installation

## Quick Start

### 1. Check System Requirements
```bash
python train_ollama.py --check-only
```

### 2. List Available Ollama Models
```bash
python train_ollama.py --list-models
```

### 3. Start Fine-tuning
```bash
python train_ollama.py --ollama-model dolphin-llama3:8b --output-name my-custom-assistant
```

## Configuration

Edit `configs/ollama_config.yaml` to customize your training:

```yaml
# Ollama specific configuration
ollama:
  base_model: "dolphin-llama3:8b"   # Your local Ollama model
  output_model_name: "custom-assistant"  # Name for your fine-tuned model
  system_prompt: "You are a helpful assistant that has been fine-tuned on custom data."

# Training configuration (optimized for GTX 1060)
training:
  num_train_epochs: 3
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 8
  learning_rate: 0.0002
```

## Supported Ollama Models

The fine-tuning script automatically detects and maps your Ollama models to compatible base models:

- `dolphin-llama3:8b` → Uses DialoGPT-medium (fallback)
- `llama3:8b` → Uses DialoGPT-medium (fallback)
- `llama2:7b` → Uses DialoGPT-medium (fallback)
- `mistral:7b` → Uses Mistral-7B-Instruct

*Note: For true Llama model fine-tuning, you need HuggingFace authentication. The current implementation uses open alternatives.*

## Training Data Format

Your training data should be in JSONL format with `instruction` and `response` fields:

```json
{"instruction": "What is machine learning?", "response": "Machine learning is a subset of artificial intelligence..."}
{"instruction": "Explain neural networks", "response": "Neural networks are computing systems inspired by biological neural networks..."}
```

## Deployment to Ollama

After training completes, the script automatically:

1. **Saves LoRA Adapter**: Creates a lightweight adapter file
2. **Generates Modelfile**: Creates an Ollama-compatible model configuration
3. **Provides Instructions**: Shows you how to deploy to Ollama

### Manual Deployment

If you need to deploy manually:

```bash
# Navigate to output directory
cd ./models/ollama_finetuned

# Create model in Ollama
ollama create my-custom-assistant -f Modelfile

# Run your fine-tuned model
ollama run my-custom-assistant
```

## System Requirements

- **GPU**: NVIDIA GPU with 4GB+ VRAM (tested on GTX 1060 6GB)
- **RAM**: 8GB+ system memory
- **Storage**: 10GB+ free disk space
- **Ollama**: Installed and running locally

## Files Structure

```
llm-finetuning-project/
├── train_ollama.py              # Main Ollama training script
├── scripts/
│   └── finetune_ollama.py       # Ollama fine-tuning implementation
├── configs/
│   └── ollama_config.yaml       # Ollama-specific configuration
├── data/
│   └── training_data.jsonl      # Your training data
└── models/
    └── ollama_finetuned/        # Output directory
        ├── lora_adapter/        # LoRA adapter files
        ├── Modelfile           # Ollama model configuration
        └── deployment_instructions.txt
```

## Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Install Ollama from https://ollama.ai/
   - Ensure `ollama` command is in your PATH

2. **"No Ollama models found"**
   - Pull a model first: `ollama pull dolphin-llama3:8b`
   - Check available models: `ollama list`

3. **GPU Memory Issues**
   - Reduce `per_device_train_batch_size` in config
   - Increase `gradient_accumulation_steps` to maintain effective batch size
   - Enable 4-bit quantization: set `load_in_4bit: true`

4. **Training Data Errors**
   - Ensure JSONL format with `instruction` and `response` fields
   - Check file encoding (should be UTF-8)
   - Validate JSON syntax

### Performance Tips

- **Memory Optimization**: Use 8-bit or 4-bit quantization
- **Speed**: Reduce `max_seq_length` for faster training
- **Quality**: Increase `num_train_epochs` for better results
- **Stability**: Lower `learning_rate` if training is unstable

## Advanced Usage

### Custom Model Mapping

To add support for new Ollama models, edit the `ollama_to_hf_mapping` in `scripts/finetune_ollama.py`:

```python
ollama_to_hf_mapping = {
    "your-model:tag": "huggingface/model-name",
    # Add your mappings here
}
```

### LoRA Configuration

Adjust LoRA parameters in `ollama_config.yaml`:

```yaml
lora:
  r: 16          # Rank (higher = more parameters, better quality)
  alpha: 32      # Scaling factor
  dropout: 0.1   # Regularization
```

## Contributing

To contribute to the Ollama fine-tuning functionality:

1. Test with different Ollama models
2. Improve model mapping accuracy
3. Add support for new architectures
4. Optimize memory usage
5. Enhance deployment automation

## License

This project is open source. Please check the main LICENSE file for details.