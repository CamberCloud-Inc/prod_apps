#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.get_fda_drug_label_info
Retrieves FDA drug label information.
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
        description='Retrieves FDA drug label information'
    )
    parser.add_argument('--drug-name', required=True, help='Name of drug to retrieve label information')
    parser.add_argument('--sections', help='Specific label sections to retrieve (JSON array, e.g., ["indications_and_usage", "warnings"])')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse parameters
    drug_name = args.drug_name
    sections = json.loads(args.sections) if args.sections else None

    # Import after dependencies are installed
    from biomni.tool.pharmacology import get_fda_drug_label_info

    result = get_fda_drug_label_info(
        drug_name=drug_name,
        sections=sections
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fda_label_info_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
