#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.query_drug_interactions
Queries drug-drug interactions.
"""

import sys
import json
from biomni.tool.pharmacology import query_drug_interactions


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
        print(json.dumps({"error": "Usage: query_drug_interactions.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_names = args.get('drug_names')
        interaction_types = args.get('interaction_types')
        severity_levels = args.get('severity_levels')
        data_lake_path = args.get('data_lake_path')

        if not drug_names:
            print(json.dumps({"error": "Missing required parameter: drug_names"}))
            sys.exit(1)

        result = query_drug_interactions(
            drug_names=drug_names,
            interaction_types=interaction_types,
            severity_levels=severity_levels,
            data_lake_path=data_lake_path
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
