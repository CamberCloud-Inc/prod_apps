#!/usr/bin/env python3
"""
Analyze ITC Binding Thermodynamics

Analyzes isothermal titration calorimetry (ITC) data to determine binding affinity and thermodynamic parameters.
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
    from biomni.tool.biochemistry import analyze_itc_binding_thermodynamics
    if len(sys.argv) != 2:
        print("Usage: analyze_itc_binding_thermodynamics.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    itc_data_path = inputs.get('itc_data_path')
    itc_data = inputs.get('itc_data')
    temperature = inputs.get('temperature', 298.15)
    protein_concentration = inputs.get('protein_concentration')
    ligand_concentration = inputs.get('ligand_concentration')

    result = analyze_itc_binding_thermodynamics(
        itc_data_path=itc_data_path,
        itc_data=itc_data,
        temperature=temperature,
        protein_concentration=protein_concentration,
        ligand_concentration=ligand_concentration
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
