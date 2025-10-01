#!/usr/bin/env python3
"""
Analyze Enzyme Kinetics Assay

Performs in vitro enzyme kinetics assay and analyzes the dose-dependent effects of modulators.
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
    from biomni.tool.biochemistry import analyze_enzyme_kinetics_assay
    if len(sys.argv) != 2:
        print("Usage: analyze_enzyme_kinetics_assay.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    enzyme_name = inputs['enzyme_name']
    substrate_concentrations = inputs['substrate_concentrations']
    enzyme_concentration = inputs['enzyme_concentration']
    modulators = inputs.get('modulators')
    time_points = inputs.get('time_points')
    output_dir = inputs.get('output_dir', './')

    result = analyze_enzyme_kinetics_assay(
        enzyme_name=enzyme_name,
        substrate_concentrations=substrate_concentrations,
        enzyme_concentration=enzyme_concentration,
        modulators=modulators,
        time_points=time_points,
        output_dir=output_dir
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
