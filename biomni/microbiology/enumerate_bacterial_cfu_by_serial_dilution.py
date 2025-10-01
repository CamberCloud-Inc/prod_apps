#!/usr/bin/env python3
"""
Quantify bacterial concentration (CFU/mL) using serial dilutions and spot plating.
"""

import sys
import json
import argparse
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Quantify bacterial concentration (CFU/mL) using serial dilutions and spot plating.'
    )
    parser.add_argument('--initial-sample-volume-ml', type=float, default=1.0, help='Initial sample volume in milliliters')
    parser.add_argument('--estimated-concentration', type=float, default=1e8, help='Estimated bacterial concentration (CFU/mL)')
    parser.add_argument('--dilution-factor', type=int, default=10, help='Dilution factor between successive dilutions')
    parser.add_argument('--num-dilutions', type=int, default=8, help='Number of dilution steps')
    parser.add_argument('--spots-per-dilution', type=int, default=3, help='Number of spots plated per dilution')
    parser.add_argument('--output-file', type=str, default='cfu_enumeration_results.csv', help='Output CSV filename')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import enumerate_bacterial_cfu_by_serial_dilution

    # Call the function
    result = enumerate_bacterial_cfu_by_serial_dilution(
        initial_sample_volume_ml=args.initial_sample_volume_ml,
        estimated_concentration=args.estimated_concentration,
        dilution_factor=args.dilution_factor,
        num_dilutions=args.num_dilutions,
        spots_per_dilution=args.spots_per_dilution,
        output_file=args.output_file
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cfu_enumeration_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
