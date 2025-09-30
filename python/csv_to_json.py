import csv
import json
import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert CSV data to JSON format')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for JSON file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nReading CSV file: {input_path}")

    # Read CSV and convert to JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            # Use DictReader to get rows as dictionaries
            csv_reader = csv.DictReader(f)
            rows = list(csv_reader)

            if not rows:
                print("Error: CSV file is empty or has no data rows")
                sys.exit(1)

            print(f"CSV validation: PASSED")
            print(f"Found {len(rows)} data rows")
            print(f"Found {len(csv_reader.fieldnames)} columns: {', '.join(csv_reader.fieldnames)}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.json"
    output_path = os.path.join(args.output_dir, output_filename)

    print(f"\nConverting CSV to JSON...")

    # Write JSON
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        print(f"JSON file saved to: {output_path}")
        print(f"Converted {len(rows)} records to JSON array")

    except Exception as e:
        print(f"Error writing JSON file: {e}")
        sys.exit(1)

    print("\nCSV to JSON conversion completed successfully!")


if __name__ == "__main__":
    main()