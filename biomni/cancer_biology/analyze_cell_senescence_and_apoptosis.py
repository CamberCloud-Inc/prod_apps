#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_cell_senescence_and_apoptosis tool
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['FlowCytometryTools', 'biomni', 'gseapy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze cell senescence and apoptosis from FCS file'
    )
    parser.add_argument('fcs_file_path', help='Path to the FCS file containing flow cytometry data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import analyze_cell_senescence_and_apoptosis

    result = analyze_cell_senescence_and_apoptosis(fcs_file_path=args.fcs_file_path)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'senescence_apoptosis_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
