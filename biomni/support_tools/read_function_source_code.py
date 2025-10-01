#!/usr/bin/env python3
"""Biomni Tool: Read Function Source Code
Wraps: biomni.tool.support_tools.read_function_source_code
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Read the source code of a biomni function'
    )
    parser.add_argument('input_file', help='JSON file with input parameters (must contain "function_name")')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Read input file with parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract function_name from input data
    function_name = input_data.get('function_name')
    if not function_name:
        raise ValueError("Input file must contain 'function_name' field")

    # Import after dependencies are installed
    from biomni.tool.support_tools import read_function_source_code

    result = read_function_source_code(function_name=function_name)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'source_code.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
