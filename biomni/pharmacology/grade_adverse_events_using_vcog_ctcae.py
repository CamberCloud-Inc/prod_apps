#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.grade_adverse_events_using_vcog_ctcae
Grades adverse events using VCOG-CTCAE criteria.
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
    from biomni.tool.pharmacology import grade_adverse_events_using_vcog_ctcae
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: grade_adverse_events_using_vcog_ctcae.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        clinical_data_file = args.get('clinical_data_file')

        if not clinical_data_file:
            print(json.dumps({"error": "Missing required parameter: clinical_data_file"}))
            sys.exit(1)

        result = grade_adverse_events_using_vcog_ctcae(
            clinical_data_file=clinical_data_file
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
