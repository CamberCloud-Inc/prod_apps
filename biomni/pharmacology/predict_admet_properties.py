#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.predict_admet_properties
Predicts ADMET properties for a list of compounds.
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
    from biomni.tool.pharmacology import predict_admet_properties
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: predict_admet_properties.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        smiles_list = args.get('smiles_list')
        ADMET_model_type = args.get('ADMET_model_type', 'MPNN')

        if not smiles_list:
            print(json.dumps({"error": "Missing required parameter: smiles_list"}))
            sys.exit(1)

        result = predict_admet_properties(
            smiles_list=smiles_list,
            ADMET_model_type=ADMET_model_type
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
