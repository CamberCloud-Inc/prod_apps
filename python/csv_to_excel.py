import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Convert CSV to formatted Excel workbook')
    parser.add_argument('csv_path', help='Path to the CSV file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for Excel file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received csv_path argument: {args.csv_path}")

    # Expand user path if provided
    csv_path = os.path.expanduser(args.csv_path)
    print(f"Expanded csv_path: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at: {csv_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read CSV file
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"CSV has {len(df)} rows and {len(df.columns)} columns")

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_path = os.path.join(args.output_dir, f"{base_name}.xlsx")

    # Write to Excel with formatting
    print(f"Converting to Excel: {output_path}")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Data']

        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"Excel conversion completed! Output: {output_path}")


if __name__ == "__main__":
    main()