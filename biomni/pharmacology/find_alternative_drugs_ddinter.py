#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.find_alternative_drugs_ddinter
Finds alternative drugs to avoid contraindicated interactions.
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
    from biomni.tool.pharmacology import find_alternative_drugs_ddinter
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: find_alternative_drugs_ddinter.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        target_drug = args.get('target_drug')
        contraindicated_drugs = args.get('contraindicated_drugs')
        therapeutic_class = args.get('therapeutic_class')
        data_lake_path = args.get('data_lake_path')

        if not target_drug or not contraindicated_drugs:
            print(json.dumps({"error": "Missing required parameters: target_drug, contraindicated_drugs"}))
            sys.exit(1)

        result = find_alternative_drugs_ddinter(
            target_drug=target_drug,
            contraindicated_drugs=contraindicated_drugs,
            therapeutic_class=therapeutic_class,
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
