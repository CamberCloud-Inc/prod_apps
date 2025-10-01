#!/usr/bin/env python3
"""
Quantify biofilm biomass using the crystal violet staining method.
"""

import sys
import json
import argparse
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
        description='Quantify biofilm biomass using the crystal violet staining method.'
    )
    parser.add_argument('--absorbance-readings', type=str, required=True, help='Absorbance readings from crystal violet assay (JSON string)')
    parser.add_argument('--control-wells', type=str, required=True, help='Control well absorbance readings (JSON string)')
    parser.add_argument('--sample-names', type=str, required=True, help='Sample identifiers (JSON string)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import quantify_biofilm_biomass_crystal_violet

    # Parse JSON string parameters
    absorbance_readings = json.loads(args.absorbance_readings)
    control_wells = json.loads(args.control_wells)
    sample_names = json.loads(args.sample_names)

    # Call the function
    result = quantify_biofilm_biomass_crystal_violet(
        absorbance_readings=absorbance_readings,
        control_wells=control_wells,
        sample_names=sample_names
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'biofilm_quantification_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
