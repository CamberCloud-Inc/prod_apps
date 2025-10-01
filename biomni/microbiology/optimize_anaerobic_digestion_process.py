#!/usr/bin/env python3
"""
Optimize anaerobic digestion process conditions to maximize VFA production or methane yield.
"""

import sys
import json
from biomni.tool.microbiology import optimize_anaerobic_digestion_process



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
    waste_characteristics = input_data.get('waste_characteristics')
    operational_parameters = input_data.get('operational_parameters')
    target_output = input_data.get('target_output', 'methane_yield')
    optimization_method = input_data.get('optimization_method', 'rsm')

    # Call the function
    result = optimize_anaerobic_digestion_process(
        waste_characteristics=waste_characteristics,
        operational_parameters=operational_parameters,
        target_output=target_output,
        optimization_method=optimization_method
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
