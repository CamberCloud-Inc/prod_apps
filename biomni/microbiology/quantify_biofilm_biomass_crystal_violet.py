#!/usr/bin/env python3
"""
Quantify biofilm biomass using the crystal violet staining method.
"""

import sys
import json
from biomni.tool.microbiology import quantify_biofilm_biomass_crystal_violet



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
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    absorbance_readings = input_data.get('absorbance_readings')
    control_wells = input_data.get('control_wells')
    sample_names = input_data.get('sample_names')

    # Call the function
    result = quantify_biofilm_biomass_crystal_violet(
        absorbance_readings=absorbance_readings,
        control_wells=control_wells,
        sample_names=sample_names
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
