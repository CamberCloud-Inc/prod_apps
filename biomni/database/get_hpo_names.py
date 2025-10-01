#!/usr/bin/env python3
"""
Biomni Tool: Get Hpo Names
Wraps: biomni.tool.database.get_hpo_names
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'biopython']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Get Hpo Names'
    )
    parser.add_argument('--hpo_terms', required=True, help='Comma-separated list of HPO term IDs')
    parser.add_argument('--data_lake_path', help='Path to data lake (optional)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import get_hpo_names

    result = get_hpo_names(
        hpo_terms=args.hpo_terms,
        data_lake_path=args.data_lake_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'hpo_names.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
