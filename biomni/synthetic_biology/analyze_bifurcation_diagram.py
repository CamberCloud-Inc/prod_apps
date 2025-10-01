#!/usr/bin/env python3
"""
Camber app wrapper for analyze_bifurcation_diagram from biomni.tool.synthetic_biology
"""

import sys
import json
import numpy as np
from biomni.tool.synthetic_biology import analyze_bifurcation_diagram



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
    time_series_data = np.array(input_data.get("time_series_data"))
    parameter_values = np.array(input_data.get("parameter_values"))
    system_name = input_data.get("system_name", "Dynamical System")
    output_dir = input_data.get("output_dir", "./")

    # Call the function
    result = analyze_bifurcation_diagram(
        time_series_data=time_series_data,
        parameter_values=parameter_values,
        system_name=system_name,
        output_dir=output_dir
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
