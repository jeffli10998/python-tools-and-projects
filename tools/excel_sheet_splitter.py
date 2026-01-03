import pandas as pd
import os
from pathlib import Path

def split_excel_by_sheets(input_file_path, output_directory=None):
    """
    Split an Excel file into separate files based on sheet names.
    
    Args:
        input_file_path (str): Path to the input Excel file
        output_directory (str, optional): Directory to save the split files. 
                                        If None, uses the same directory as input file.
    """
    try:
        # Convert to Path object for easier handling
        input_path = Path(input_file_path)
        
        # Check if input file exists
        if not input_path.exists():
            print(f"Error: File '{input_file_path}' not found.")
            return
        
        # Set output directory
        if output_directory is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Read all sheets from the Excel file
        print(f"Reading Excel file: {input_file_path}")
        excel_file = pd.ExcelFile(input_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Found {len(sheet_names)} sheets: {sheet_names}")
        
        # Process each sheet
        for sheet_name in sheet_names:
            try:
                # Read the sheet
                df = pd.read_excel(input_file_path, sheet_name=sheet_name)
                
                # Clean sheet name for filename (remove invalid characters)
                clean_sheet_name = clean_filename(sheet_name)
                
                # Create output filename
                output_filename = f"{clean_sheet_name}.xlsx"
                output_path = output_dir / output_filename
                
                # Save the sheet as a separate Excel file
                df.to_excel(output_path, index=False, sheet_name=sheet_name)
                
                print(f"✓ Created: {output_path} (from sheet '{sheet_name}')")
                
            except Exception as e:
                print(f"✗ Error processing sheet '{sheet_name}': {e}")
        
        print(f"\nCompleted! Files saved in: {output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")

def clean_filename(filename):
    """
    Clean filename by removing or replacing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Characters that are invalid in filenames
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters with underscore
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_sheet"
    
    return filename

def split_excel_to_csv(input_file_path, output_directory=None):
    """
    Alternative function to split Excel sheets into CSV files.
    
    Args:
        input_file_path (str): Path to the input Excel file
        output_directory (str, optional): Directory to save the CSV files
    """
    try:
        # Convert to Path object
        input_path = Path(input_file_path)
        
        # Check if input file exists
        if not input_path.exists():
            print(f"Error: File '{input_file_path}' not found.")
            return
        
        # Set output directory
        if output_directory is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Read all sheets
        print(f"Reading Excel file: {input_file_path}")
        excel_file = pd.ExcelFile(input_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Found {len(sheet_names)} sheets: {sheet_names}")
        
        # Process each sheet
        for sheet_name in sheet_names:
            try:
                # Read the sheet
                df = pd.read_excel(input_file_path, sheet_name=sheet_name)
                
                # Clean sheet name for filename
                clean_sheet_name = clean_filename(sheet_name)
                
                # Create output filename
                output_filename = f"{clean_sheet_name}.csv"
                output_path = output_dir / output_filename
                
                # Save as CSV
                df.to_csv(output_path, index=False)
                
                print(f"✓ Created: {output_path} (from sheet '{sheet_name}')")
                
            except Exception as e:
                print(f"✗ Error processing sheet '{sheet_name}': {e}")
        
        print(f"\nCompleted! CSV files saved in: {output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Example 1: Split to Excel files
    input_file = "your_excel_file.xlsx"  # Replace with your file path
    
    print("Option 1: Split into separate Excel files")
    split_excel_by_sheets(input_file)
    
    print("\n" + "="*50 + "\n")
    
    print("Option 2: Split into CSV files")
    split_excel_to_csv(input_file)
    
    # Example with custom output directory
    # split_excel_by_sheets(input_file, "output_folder")

    # Split Excel file into separate Excel files
split_excel_by_sheets("table_1.xlsx")

# Split Excel file into CSV files
split_excel_to_csv("table_1.xlsx")

# Specify custom output directory
split_excel_by_sheets("table_1.xlsx", "output_folder")