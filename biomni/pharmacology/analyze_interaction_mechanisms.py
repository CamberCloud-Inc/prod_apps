#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_interaction_mechanisms
Analyzes drug-drug interaction mechanisms.
"""

import sys
import json
from biomni.tool.pharmacology import analyze_interaction_mechanisms


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
        print(json.dumps({"error": "Usage: analyze_interaction_mechanisms.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_pair = args.get('drug_pair')
        detailed_analysis = args.get('detailed_analysis', True)
        data_lake_path = args.get('data_lake_path')

        if not drug_pair:
            print(json.dumps({"error": "Missing required parameter: drug_pair"}))
            sys.exit(1)

        result = analyze_interaction_mechanisms(
            drug_pair=drug_pair,
            detailed_analysis=detailed_analysis,
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
