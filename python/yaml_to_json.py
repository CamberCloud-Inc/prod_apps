import subprocess
import sys
import json
import os
import argparse

# Install PyYAML if needed
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])

import yaml


def main():
    parser = argparse.ArgumentParser(description='Convert YAML files to JSON format')
    parser.add_argument('input_file', help='Path to the input YAML file')
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

    print(f"\nReading YAML file: {input_path}")

    # Read and parse YAML
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is None:
            print("Error: YAML file is empty")
            sys.exit(1)

        print("YAML validation: PASSED")

    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    # Handle .yml and .yaml extensions
    if input_filename.endswith('.yml') or input_filename.endswith('.yaml'):
        output_filename = f"{base_name}.json"
    else:
        output_filename = f"{input_filename}.json"

    output_path = os.path.join(args.output_dir, output_filename)

    print(f"\nConverting YAML to JSON...")

    # Write JSON with custom serializer for dates and other types
    def json_serializer(obj):
        """Convert non-serializable objects to strings"""
        if hasattr(obj, 'isoformat'):  # datetime, date, time objects
            return obj.isoformat()
        return str(obj)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=json_serializer)
        print(f"JSON file saved to: {output_path}")

    except Exception as e:
        print(f"Error writing JSON file: {e}")
        sys.exit(1)

    # Print data structure info
    if isinstance(data, dict):
        print(f"Converted YAML object with {len(data)} top-level keys")
    elif isinstance(data, list):
        print(f"Converted YAML array with {len(data)} items")
    else:
        print(f"Converted YAML value")

    print("\nYAML to JSON conversion completed successfully!")


if __name__ == "__main__":
    main()