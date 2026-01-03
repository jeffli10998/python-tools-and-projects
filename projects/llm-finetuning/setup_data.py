#!/usr/bin/env python3
"""
Data Setup Helper for LLM Fine-tuning Project
Creates sample data files and guides user through data preparation
"""

import os
import json
import csv
from pathlib import Path

def create_data_directory():
    """Create the data directory structure."""
    data_dir = "C:\\py_workspace\\learning\\llm-training-project\\llm_env\\your_data"
    os.makedirs(data_dir, exist_ok=True)
    print(f"✓ Created data directory: {data_dir}")
    return data_dir

def create_sample_txt_file(data_dir):
    """Create a sample TXT file."""
    sample_content = """Machine learning is a powerful technology that enables computers to learn from data.

Deep learning is a subset of machine learning that uses neural networks with multiple layers.

Natural language processing helps computers understand and generate human language.

Computer vision allows machines to interpret and analyze visual information from images and videos.

Reinforcement learning teaches agents to make decisions through trial and error in an environment."""
    
    txt_path = os.path.join(data_dir, "sample_knowledge.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    print(f"✓ Created sample TXT file: {txt_path}")

def create_sample_csv_file(data_dir):
    """Create a sample CSV file with instruction-response pairs."""
    csv_data = [
        {
            "instruction": "What is artificial intelligence?",
            "response": "Artificial intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans."
        },
        {
            "instruction": "Explain machine learning in simple terms.",
            "response": "Machine learning is a method of teaching computers to learn patterns from data without being explicitly programmed for every task."
        },
        {
            "instruction": "What are neural networks?",
            "response": "Neural networks are computing systems inspired by biological neural networks, consisting of interconnected nodes that process information."
        },
        {
            "instruction": "How does deep learning work?",
            "response": "Deep learning uses neural networks with multiple layers to automatically learn complex patterns and representations from large amounts of data."
        },
        {
            "instruction": "What is the purpose of fine-tuning?",
            "response": "Fine-tuning adapts a pre-trained model to perform better on specific tasks by training it on task-specific data while preserving general knowledge."
        }
    ]
    
    csv_path = os.path.join(data_dir, "sample_qa_pairs.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['instruction', 'response'])
        writer.writeheader()
        writer.writerows(csv_data)
    print(f"✓ Created sample CSV file: {csv_path}")

def create_sample_json_file(data_dir):
    """Create a sample JSON file."""
    json_data = [
        {
            "instruction": "Explain the concept of transfer learning.",
            "response": "Transfer learning is a technique where a model trained on one task is adapted for a related task, leveraging previously learned knowledge to improve performance and reduce training time.",
            "category": "machine_learning"
        },
        {
            "instruction": "What is the difference between classification and regression?",
            "response": "Classification predicts discrete categories or classes, while regression predicts continuous numerical values. Classification outputs labels, regression outputs numbers.",
            "category": "machine_learning"
        },
        {
            "instruction": "How do you evaluate a machine learning model?",
            "response": "Model evaluation involves using metrics like accuracy, precision, recall, F1-score for classification, or MSE, RMSE, MAE for regression, along with techniques like cross-validation.",
            "category": "evaluation"
        }
    ]
    
    json_path = os.path.join(data_dir, "sample_structured_data.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Created sample JSON file: {json_path}")

def create_sample_jsonl_file(data_dir):
    """Create a sample JSONL file."""
    jsonl_data = [
        {
            "instruction": "What is LoRA fine-tuning?",
            "response": "LoRA (Low-Rank Adaptation) is an efficient fine-tuning method that adds small trainable matrices to existing model layers, allowing adaptation with minimal computational resources."
        },
        {
            "instruction": "Why use LoRA instead of full fine-tuning?",
            "response": "LoRA reduces memory usage, training time, and storage requirements while maintaining performance, making it ideal for fine-tuning large models on consumer hardware."
        },
        {
            "instruction": "What hardware is needed for LoRA fine-tuning?",
            "response": "LoRA fine-tuning can work on consumer GPUs like GTX 1060 with 6GB VRAM, making it accessible compared to full fine-tuning which requires expensive hardware."
        }
    ]
    
    jsonl_path = os.path.join(data_dir, "sample_lora_knowledge.jsonl")
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for item in jsonl_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"✓ Created sample JSONL file: {jsonl_path}")

def create_data_format_guide(data_dir):
    """Create a guide explaining data formats."""
    guide_content = """# Data Format Guide for LLM Fine-tuning

## Supported File Formats

### 1. TXT Files (.txt)
- Plain text content separated by double newlines
- Each paragraph becomes a training example
- Automatically generates instruction-response pairs

### 2. CSV Files (.csv)
- Must have 'instruction' and 'response' columns
- Alternative column names: question/answer, input/output, prompt/completion
- Each row becomes one training example

### 3. JSON Files (.json)
- Array of objects with instruction and response fields
- Can include additional metadata fields
- Supports nested structures

### 4. JSONL Files (.jsonl)
- One JSON object per line
- Each line must have instruction and response fields
- Most efficient format for large datasets

## Data Quality Tips

1. **Clear Instructions**: Make instructions specific and clear
2. **Consistent Responses**: Ensure responses are accurate and helpful
3. **Diverse Examples**: Include various types of questions and scenarios
4. **Appropriate Length**: Keep responses focused but comprehensive
5. **Domain Relevance**: Use data relevant to your target use case

## Example Data Structure

```json
{
  "instruction": "What is machine learning?",
  "response": "Machine learning is a subset of AI that enables computers to learn from data without explicit programming.",
  "source": "optional_metadata"
}
```

## Next Steps

1. Add your own data files to this directory
2. Run: `python scripts/prepare_data.py` to process your data
3. Start training: `python train.py`
"""
    
    guide_path = os.path.join(data_dir, "DATA_FORMAT_GUIDE.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    print(f"✓ Created data format guide: {guide_path}")

def main():
    print("=" * 60)
    print("LLM Fine-tuning Data Setup Helper")
    print("=" * 60)
    
    # Create data directory
    data_dir = create_data_directory()
    
    # Create sample files
    print("\nCreating sample data files...")
    create_sample_txt_file(data_dir)
    create_sample_csv_file(data_dir)
    create_sample_json_file(data_dir)
    create_sample_jsonl_file(data_dir)
    create_data_format_guide(data_dir)
    
    print("\n" + "=" * 60)
    print("✅ Data setup completed!")
    print("=" * 60)
    
    print(f"\n📁 Your data directory: {data_dir}")
    print("\n📋 What's been created:")
    print("   • sample_knowledge.txt - Example text file")
    print("   • sample_qa_pairs.csv - Example CSV with Q&A pairs")
    print("   • sample_structured_data.json - Example JSON file")
    print("   • sample_lora_knowledge.jsonl - Example JSONL file")
    print("   • DATA_FORMAT_GUIDE.md - Complete formatting guide")
    
    print("\n🚀 Next steps:")
    print("   1. Review the sample files to understand the format")
    print("   2. Add your own training data to the directory")
    print("   3. Run: python scripts/prepare_data.py")
    print("   4. Start training: python train.py")
    
    print("\n💡 Tips:")
    print("   • Use diverse, high-quality instruction-response pairs")
    print("   • Aim for 100-1000+ examples for good results")
    print("   • Keep responses focused and accurate")
    print("   • Test with sample data first")

if __name__ == "__main__":
    main()