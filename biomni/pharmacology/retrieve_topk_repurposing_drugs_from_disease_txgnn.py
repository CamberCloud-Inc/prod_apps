#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.retrieve_topk_repurposing_drugs_from_disease_txgnn
Predicts top K drug repurposing candidates for a given disease using TxGNN.
"""

import sys
import json
from biomni.tool.pharmacology import retrieve_topk_repurposing_drugs_from_disease_txgnn


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
        print(json.dumps({"error": "Usage: retrieve_topk_repurposing_drugs_from_disease_txgnn.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        disease_name = args.get('disease_name')
        data_lake_path = args.get('data_lake_path')
        k = args.get('k', 5)

        if not disease_name or not data_lake_path:
            print(json.dumps({"error": "Missing required parameters: disease_name, data_lake_path"}))
            sys.exit(1)

        result = retrieve_topk_repurposing_drugs_from_disease_txgnn(
            disease_name=disease_name,
            data_lake_path=data_lake_path,
            k=k
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
