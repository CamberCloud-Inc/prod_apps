#!/usr/bin/env python3
"""
Biomni Tool: Analyze Cytokine Production In Cd4 Tcells
Wraps: biomni.tool.immunology.analyze_cytokine_production_in_cd4_tcells
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
        description='Analyze Cytokine Production In Cd4 Tcells'
    )
    parser.add_argument('--fcs_files_dict', help='Dictionary mapping sample IDs to FCS file paths (JSON dict)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_cytokine_production_in_cd4_tcells

    # Parse fcs_files_dict
    fcs_files_dict = json.loads(args.fcs_files_dict) if args.fcs_files_dict else None

    result = analyze_cytokine_production_in_cd4_tcells(
        fcs_files_dict=fcs_files_dict,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cytokine_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
