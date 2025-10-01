#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.predict_binding_affinity_protein_1d_sequence
Predicts protein-ligand binding affinity.
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
    from biomni.tool.pharmacology import predict_binding_affinity_protein_1d_sequence
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: predict_binding_affinity_protein_1d_sequence.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        smiles_list = args.get('smiles_list')
        amino_acid_sequence = args.get('amino_acid_sequence')
        affinity_model_type = args.get('affinity_model_type', 'MPNN-CNN')

        if not smiles_list or not amino_acid_sequence:
            print(json.dumps({"error": "Missing required parameters: smiles_list, amino_acid_sequence"}))
            sys.exit(1)

        result = predict_binding_affinity_protein_1d_sequence(
            smiles_list=smiles_list,
            amino_acid_sequence=amino_acid_sequence,
            affinity_model_type=affinity_model_type
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
