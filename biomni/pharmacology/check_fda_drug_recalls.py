#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.check_fda_drug_recalls
Checks FDA drug recalls database.
"""

import sys
import json
from biomni.tool.pharmacology import check_fda_drug_recalls


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
        print(json.dumps({"error": "Usage: check_fda_drug_recalls.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_name = args.get('drug_name')
        classification = args.get('classification')
        date_range = args.get('date_range')

        if not drug_name:
            print(json.dumps({"error": "Missing required parameter: drug_name"}))
            sys.exit(1)

        # Convert date_range to tuple if it's a list
        if date_range and isinstance(date_range, list):
            date_range = tuple(date_range)

        result = check_fda_drug_recalls(
            drug_name=drug_name,
            classification=classification,
            date_range=date_range
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
