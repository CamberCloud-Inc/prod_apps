#!/usr/bin/env python3
"""
Analyze Circular Dichroism Spectra

Analyzes circular dichroism (CD) spectroscopy data to determine secondary structure and thermal stability.
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze circular dichroism (CD) spectroscopy data'
    )
    parser.add_argument('--sample_name', required=True, help='Identifier for the protein or sample being analyzed')
    parser.add_argument('--sample_type', required=True, help='Type of sample (e.g., "protein", "peptide", "DNA", "RNA")')
    parser.add_argument('--wavelength_data', required=True, help='Wavelength values in nanometers (comma-separated)')
    parser.add_argument('--cd_signal_data', required=True, help='CD signal values corresponding to each wavelength (comma-separated)')
    parser.add_argument('--temperature_data', help='Temperature values in Kelvin for thermal denaturation (comma-separated, optional)')
    parser.add_argument('--thermal_cd_data', help='CD signal values at specific wavelength across temperatures (comma-separated, optional)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_circular_dichroism_spectra

    # Convert comma-separated strings to arrays of numbers
    wavelength_data = [float(x.strip()) for x in args.wavelength_data.split(',')]
    cd_signal_data = [float(x.strip()) for x in args.cd_signal_data.split(',')]

    temperature_data = None
    if args.temperature_data:
        temperature_data = [float(x.strip()) for x in args.temperature_data.split(',')]

    thermal_cd_data = None
    if args.thermal_cd_data:
        thermal_cd_data = [float(x.strip()) for x in args.thermal_cd_data.split(',')]

    result = analyze_circular_dichroism_spectra(
        sample_name=args.sample_name,
        sample_type=args.sample_type,
        wavelength_data=wavelength_data,
        cd_signal_data=cd_signal_data,
        temperature_data=temperature_data,
        thermal_cd_data=thermal_cd_data,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cd_analysis_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
