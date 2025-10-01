#!/usr/bin/env python3
"""
Analyze Endolysosomal Calcium Dynamics

Analyze calcium dynamics in endo-lysosomal compartments using ELGA/ELGA1 probe data.
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
    from biomni.tool.physiology import analyze_endolysosomal_calcium_dynamics
    if len(sys.argv) != 2:
        print("Usage: analyze_endolysosomal_calcium_dynamics.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    time_points = inputs['time_points']
    luminescence_values = inputs['luminescence_values']
    treatment_time = inputs.get('treatment_time')
    cell_type = inputs.get('cell_type', '')
    treatment_name = inputs.get('treatment_name', '')
    output_file = inputs.get('output_file', 'calcium_analysis_results.txt')

    result = analyze_endolysosomal_calcium_dynamics(
        time_points=time_points,
        luminescence_values=luminescence_values,
        treatment_time=treatment_time,
        cell_type=cell_type,
        treatment_name=treatment_name,
        output_file=output_file
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
