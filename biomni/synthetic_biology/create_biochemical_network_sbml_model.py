#!/usr/bin/env python3
"""
Camber app wrapper for create_biochemical_network_sbml_model from biomni.tool.synthetic_biology
"""

import sys
import json
from biomni.tool.synthetic_biology import create_biochemical_network_sbml_model



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
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    reaction_network = input_data.get("reaction_network")
    kinetic_parameters = input_data.get("kinetic_parameters")
    output_file = input_data.get("output_file", "biochemical_model.xml")

    # Call the function
    result = create_biochemical_network_sbml_model(
        reaction_network=reaction_network,
        kinetic_parameters=kinetic_parameters,
        output_file=output_file
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
