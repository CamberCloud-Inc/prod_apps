#!/usr/bin/env python3
"""
Biomni Tool: BLAST Sequence
Wraps: biomni.tool.database.blast_sequence
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='BLAST a sequence against a database'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import blast_sequence

    result = blast_sequence(
        sequence=input_data.get('sequence'),
        database=input_data.get('database'),
        program=input_data.get('program')
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'blast_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
