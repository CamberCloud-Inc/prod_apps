#!/usr/bin/env python3
"""Biomni Tool: Run Python REPL
Wraps: biomni.tool.support_tools.run_python_repl
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
        description='Execute Python commands in a REPL environment'
    )
    parser.add_argument('input_file', help='JSON file with input parameters (must contain "command")')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Read input file with parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract command from input data
    command = input_data.get('command')
    if not command:
        raise ValueError("Input file must contain 'command' field")

    # Import after dependencies are installed
    from biomni.tool.support_tools import run_python_repl

    result = run_python_repl(command=command)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'repl_result.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
