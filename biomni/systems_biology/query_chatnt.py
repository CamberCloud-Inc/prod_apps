#!/usr/bin/env python3
"""
Wrapper for Biomni query_chatnt tool
"""
import sys
import argparse
import os
import json


def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Query ChatNT using Biomni'
    )
    parser.add_argument('input_file', help='JSON file with query parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    question = input_data.get('question')
    sequence = input_data.get('sequence')
    device = input_data.get('device', 0)

    # Import after dependencies are installed
    from biomni.tool.systems_biology import query_chatnt

    result = query_chatnt(question, sequence, device)

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'chatnt_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
