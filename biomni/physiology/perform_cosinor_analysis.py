#!/usr/bin/env python3
"""
Perform Cosinor Analysis

Performs cosinor analysis on physiological time series data to characterize circadian rhythms.
"""

import sys
import json
from biomni.tool.physiology import perform_cosinor_analysis



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
        print("Usage: perform_cosinor_analysis.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    time_data = inputs['time_data']
    physiological_data = inputs['physiological_data']
    period = inputs.get('period', 24.0)

    result = perform_cosinor_analysis(
        time_data=time_data,
        physiological_data=physiological_data,
        period=period
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
