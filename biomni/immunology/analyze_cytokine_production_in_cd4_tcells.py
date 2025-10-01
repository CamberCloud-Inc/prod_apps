#!/usr/bin/env python3
"""
Camber wrapper for analyze_cytokine_production_in_cd4_tcells from biomni.tool.immunology
"""

import argparse
import sys
import json
import os



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
        description='Analyze cytokine production in CD4 T cells from flow cytometry data'
    )
    parser.add_argument('input_file', help='JSON file with FCS file paths')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    fcs_files_dict = input_data['fcs_files_dict']

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_cytokine_production_in_cd4_tcells

    result = analyze_cytokine_production_in_cd4_tcells(
        fcs_files_dict=fcs_files_dict,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cytokine_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
