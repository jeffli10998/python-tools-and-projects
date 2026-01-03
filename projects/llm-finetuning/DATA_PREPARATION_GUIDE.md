# Data Preparation Guide - UTF-8 and Multi-Encoding Support

## Overview

The data preparation system has been enhanced to handle various text encodings and provide robust data processing for your LLM fine-tuning project.

## Key Improvements

### 1. Multi-Encoding Support
The system now automatically detects and handles multiple text encodings:
- **UTF-8** (primary)
- **UTF-8-BOM** (UTF-8 with Byte Order Mark)
- **Latin-1** (ISO-8859-1)
- **CP1252** (Windows-1252)
- **GBK** (Chinese encoding)
- **GB2312** (Simplified Chinese)

### 2. Robust Error Handling
- Files with encoding issues are processed with fallback encodings
- Invalid records are filtered out automatically
- Processing continues even if individual files fail
- Detailed logging shows which encoding was used for each file

### 3. Data Validation and Cleaning
- Automatic removal of empty or invalid records
- Text trimming and normalization
- Validation ensures all records have required fields
- Warning messages for filtered records

## Your Data Directory

**Location**: `C:\py_workspace\learning\llm-training-project\llm_env\your_data`

### Current Status
✅ **2,728 valid training records** prepared successfully  
✅ **Multi-encoding support** handles your diverse text files  
✅ **Automatic data cleaning** removes invalid entries  
✅ **System ready** for training

## Supported File Formats

### 1. Text Files (.txt)
- Automatically splits content by double newlines
- Creates instruction-response pairs
- Handles multiple encodings automatically
- Example: `knowledge.txt`, `data_science.txt`

### 2. CSV Files (.csv)
- Requires `instruction` and `response` columns
- Alternative column names supported:
  - `question` → `instruction`
  - `answer` → `response`
  - `input` → `instruction`
  - `output` → `response`
  - `prompt` → `instruction`
  - `completion` → `response`

### 3. JSON Files (.json)
- Array of objects with instruction/response fields
- Supports additional metadata fields
- Example: `sample_structured_data.json`

### 4. JSONL Files (.jsonl)
- One JSON object per line
- Most efficient for large datasets
- Example: `sample_lora_knowledge.jsonl`

## Usage Commands

### Basic Data Preparation
```bash
# Process all files in your data directory
python scripts/prepare_data.py

# Process specific file or directory
python scripts/prepare_data.py --input path/to/your/data

# Create sample data for testing
python scripts/prepare_data.py --create-sample
```

### Training Commands
```bash
# Check system readiness
python train.py --check-only

# Start training with your data
python train.py

# Training with specific data source
python train.py --data-source path/to/your/data

# Create sample data and train
python train.py --create-sample
```

## Data Quality Tips

### 1. Text Encoding
- ✅ **UTF-8 preferred** but other encodings supported
- ✅ **Mixed encodings** in same directory handled automatically
- ✅ **Chinese, European, and other character sets** supported

### 2. Content Quality
- **Clear instructions**: Make questions specific and actionable
- **Comprehensive responses**: Provide detailed, accurate answers
- **Diverse examples**: Include various topics and question types
- **Consistent format**: Maintain similar response styles

### 3. Dataset Size
- **Minimum**: 50-100 examples for basic fine-tuning
- **Recommended**: 500-1000+ examples for good results
- **Current**: 2,728 examples (excellent for training!)

## File Processing Results

Based on your recent data preparation:

| File Type | Files Processed | Records Generated | Status |
|-----------|----------------|-------------------|--------|
| TXT | Multiple | 2,700+ | ✅ Success |
| CSV | 1 | 5 | ✅ Success |
| JSON | 1 | 3 | ✅ Success |
| JSONL | 1 | 3 | ✅ Success |
| **Total** | **Multiple** | **2,728** | ✅ **Ready** |

## Next Steps

### 1. Review Prepared Data
```bash
# Check the prepared training data
head -n 5 data/training_data.jsonl
```

### 2. Start Training
```bash
# Begin fine-tuning with your data
python train.py
```

### 3. Monitor Progress
- Training logs: `training.log`
- Model outputs: `outputs/` directory
- Training summary: `outputs/training_summary.json`

### 4. Evaluate Results
```bash
# Evaluate trained model
python train.py --evaluate

# Interactive testing
python train.py --interactive
```

## Troubleshooting

### Encoding Issues
- **Problem**: "UnicodeDecodeError" messages
- **Solution**: ✅ **Already fixed** - automatic encoding detection

### Empty Records
- **Problem**: "missing or empty field" errors
- **Solution**: ✅ **Already fixed** - automatic filtering and cleaning

### File Format Issues
- **Problem**: Unsupported file formats
- **Solution**: Convert to .txt, .csv, .json, or .jsonl

### Performance Tips
- **Large files**: Split into smaller chunks for faster processing
- **Memory usage**: Process files individually if needed
- **GPU training**: Ensure CUDA is available (✅ GTX 1060 detected)

## Advanced Configuration

### Custom Data Processing
Edit `scripts/prepare_data.py` to customize:
- Text chunking strategies
- Instruction templates
- Data validation rules
- Output formatting

### Training Configuration
Edit `configs/lora_config.yaml` to adjust:
- Learning rate
- Batch size
- Training epochs
- LoRA parameters

---

**Status**: ✅ **Ready for Training**  
**Data**: 2,728 validated records  
**System**: GTX 1060 with CUDA support  
**Next**: Run `python train.py` to start fine-tuning!