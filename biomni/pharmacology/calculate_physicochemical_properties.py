#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.calculate_physicochemical_properties
Calculates physicochemical properties of molecules.
"""

import sys
import json
from biomni.tool.pharmacology import calculate_physicochemical_properties


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
        print(json.dumps({"error": "Usage: calculate_physicochemical_properties.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        smiles_string = args.get('smiles_string')

        if not smiles_string:
            print(json.dumps({"error": "Missing required parameter: smiles_string"}))
            sys.exit(1)

        result = calculate_physicochemical_properties(
            smiles_string=smiles_string
        )

        print(json.dumps({"result": result}))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
