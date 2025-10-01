#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.query_fda_adverse_events
Queries FDA adverse events database.
"""

import sys
import json
from biomni.tool.pharmacology import query_fda_adverse_events


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
        print(json.dumps({"error": "Usage: query_fda_adverse_events.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_name = args.get('drug_name')
        date_range = args.get('date_range')
        severity_filter = args.get('severity_filter')
        outcome_filter = args.get('outcome_filter')
        limit = args.get('limit', 100)

        if not drug_name:
            print(json.dumps({"error": "Missing required parameter: drug_name"}))
            sys.exit(1)

        # Convert date_range to tuple if it's a list
        if date_range and isinstance(date_range, list):
            date_range = tuple(date_range)

        result = query_fda_adverse_events(
            drug_name=drug_name,
            date_range=date_range,
            severity_filter=severity_filter,
            outcome_filter=outcome_filter,
            limit=limit
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
