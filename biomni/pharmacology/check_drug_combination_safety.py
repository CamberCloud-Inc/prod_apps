#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.check_drug_combination_safety
Checks safety of drug combinations.
"""

import sys
import json
from biomni.tool.pharmacology import check_drug_combination_safety


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
        print(json.dumps({"error": "Usage: check_drug_combination_safety.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_list = args.get('drug_list')
        include_mechanisms = args.get('include_mechanisms', True)
        include_management = args.get('include_management', True)
        data_lake_path = args.get('data_lake_path')

        if not drug_list:
            print(json.dumps({"error": "Missing required parameter: drug_list"}))
            sys.exit(1)

        result = check_drug_combination_safety(
            drug_list=drug_list,
            include_mechanisms=include_mechanisms,
            include_management=include_management,
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
