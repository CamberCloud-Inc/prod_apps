#!/usr/bin/env python3
"""
Analyze Circular Dichroism Spectra

Analyzes circular dichroism (CD) spectroscopy data to determine secondary structure and thermal stability.
"""

import sys
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
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_circular_dichroism_spectra
    if len(sys.argv) != 2:
        print("Usage: analyze_circular_dichroism_spectra.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    sample_name = inputs['sample_name']
    sample_type = inputs['sample_type']
    wavelength_data = inputs['wavelength_data']
    cd_signal_data = inputs['cd_signal_data']
    temperature_data = inputs.get('temperature_data')
    thermal_cd_data = inputs.get('thermal_cd_data')
    output_dir = inputs.get('output_dir', './')

    result = analyze_circular_dichroism_spectra(
        sample_name=sample_name,
        sample_type=sample_type,
        wavelength_data=wavelength_data,
        cd_signal_data=cd_signal_data,
        temperature_data=temperature_data,
        thermal_cd_data=thermal_cd_data,
        output_dir=output_dir
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
