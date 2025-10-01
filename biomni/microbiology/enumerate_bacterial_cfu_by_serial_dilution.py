#!/usr/bin/env python3
"""
Quantify bacterial concentration (CFU/mL) using serial dilutions and spot plating.
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
    from biomni.tool.microbiology import enumerate_bacterial_cfu_by_serial_dilution
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    initial_sample_volume_ml = input_data.get('initial_sample_volume_ml', 1.0)
    estimated_concentration = input_data.get('estimated_concentration', 1e8)
    dilution_factor = input_data.get('dilution_factor', 10)
    num_dilutions = input_data.get('num_dilutions', 8)
    spots_per_dilution = input_data.get('spots_per_dilution', 3)
    output_file = input_data.get('output_file', 'cfu_enumeration_results.csv')

    # Call the function
    result = enumerate_bacterial_cfu_by_serial_dilution(
        initial_sample_volume_ml=initial_sample_volume_ml,
        estimated_concentration=estimated_concentration,
        dilution_factor=dilution_factor,
        num_dilutions=num_dilutions,
        spots_per_dilution=spots_per_dilution,
        output_file=output_file
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
