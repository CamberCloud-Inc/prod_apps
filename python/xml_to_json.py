import subprocess
import sys
import os
import argparse
import json

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "xmltodict"])

import xmltodict


def main():
    parser = argparse.ArgumentParser(description='Transform XML documents to JSON')
    parser.add_argument('xml_path', help='Path to the XML file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for JSON file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received xml_path argument: {args.xml_path}")

    # Expand user path if provided
    xml_path = os.path.expanduser(args.xml_path)
    print(f"Expanded xml_path: {xml_path}")

    if not os.path.exists(xml_path):
        print(f"Error: XML file not found at: {xml_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read and parse XML file
    print(f"Reading XML file: {xml_path}")
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()

    print(f"Parsing XML to JSON...")
    json_data = xmltodict.parse(xml_content)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(xml_path))[0]
    output_path = os.path.join(args.output_dir, f"{base_name}.json")

    # Write to JSON file with pretty formatting
    print(f"Writing JSON file: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)

    print(f"XML to JSON conversion completed! Output: {output_path}")


if __name__ == "__main__":
    main()