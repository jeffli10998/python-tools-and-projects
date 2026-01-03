# Create this file to fix the document_processor.py
import os

# Read the current file
with open(r'c:\py_workspace\projects\llm-training\llm_embedding\core\document_processor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Write it back with proper encoding
with open(r'c:\py_workspace\projects\llm-training\llm_embedding\core\document_processor.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("File encoding fixed!")