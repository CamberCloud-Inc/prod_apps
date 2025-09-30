import json
import csv
import sys
import os
import argparse


def flatten_json(data, parent_key='', sep='_'):
    """Flatten nested JSON structure"""
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            if isinstance(item, (dict, list)):
                items.extend(flatten_json(item, new_key, sep=sep).items())
            else:
                items.append((new_key, item))
    return dict(items)


def main():
    parser = argparse.ArgumentParser(description='Convert JSON data to CSV format')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for CSV file (default: ./)')

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

    print(f"\nReading JSON file: {input_path}")

    # Read and parse JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("JSON validation: PASSED")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.csv"
    output_path = os.path.join(args.output_dir, output_filename)

    print(f"\nConverting JSON to CSV...")

    # Handle different JSON structures
    try:
        if isinstance(data, list):
            # Array of objects
            if not data:
                print("Error: Empty JSON array")
                sys.exit(1)

            # Flatten each object
            flattened_data = [flatten_json(item) for item in data]

            # Get all unique keys
            all_keys = set()
            for item in flattened_data:
                all_keys.update(item.keys())
            fieldnames = sorted(all_keys)

            # Write CSV
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)

            print(f"Converted {len(data)} records to CSV")

        elif isinstance(data, dict):
            # Single object - flatten and write as one row
            flattened = flatten_json(data)
            fieldnames = sorted(flattened.keys())

            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(flattened)

            print(f"Converted 1 record to CSV")
        else:
            print(f"Error: Unsupported JSON structure (expected object or array)")
            sys.exit(1)

        print(f"CSV file saved to: {output_path}")
        print(f"Number of columns: {len(fieldnames)}")

    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

    print("\nJSON to CSV conversion completed successfully!")


if __name__ == "__main__":
    main()