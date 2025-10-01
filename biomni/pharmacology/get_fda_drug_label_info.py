#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.get_fda_drug_label_info
Retrieves FDA drug label information.
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
    from biomni.tool.pharmacology import get_fda_drug_label_info
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: get_fda_drug_label_info.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_name = args.get('drug_name')
        sections = args.get('sections')

        if not drug_name:
            print(json.dumps({"error": "Missing required parameter: drug_name"}))
            sys.exit(1)

        result = get_fda_drug_label_info(
            drug_name=drug_name,
            sections=sections
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
