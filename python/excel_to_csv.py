import argparse
import os
import sys
import subprocess

try:
    import pandas as pd
except ImportError:
    print("pandas not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import pandas as pd
    
def excel_to_dataframe_and_csv(input_file: str, output_folder: str):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        sys.exit(1)

    output_csv_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".csv")
    try:
        df.to_csv(output_csv_path, index=False)
        print(f"CSV saved to: {output_csv_path}")
    except Exception as e:
        print(f"Error saving CSV: {e}")
        sys.exit(1)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Excel file to CSV and load into DataFrame.")
    parser.add_argument("input_file", help="Path to the input Excel file (.xlsx or .xls)")
    parser.add_argument("output_folder", help="Path to the output folder where CSV will be saved")
    args = parser.parse_args()

    excel_to_dataframe_and_csv(args.input_file, args.output_folder)
