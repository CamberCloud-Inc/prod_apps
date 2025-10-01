#!/usr/bin/env python3
"""
Analyze Hemodynamic Data

Analyzes raw blood pressure data to calculate key hemodynamic parameters.
"""

import sys
import json
from biomni.tool.physiology import analyze_hemodynamic_data



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
    if len(sys.argv) != 2:
        print("Usage: analyze_hemodynamic_data.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    pressure_data = inputs['pressure_data']
    sampling_rate = inputs['sampling_rate']
    output_file = inputs.get('output_file', 'hemodynamic_results.csv')

    result = analyze_hemodynamic_data(
        pressure_data=pressure_data,
        sampling_rate=sampling_rate,
        output_file=output_file
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
