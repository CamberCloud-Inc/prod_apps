#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_radiolabeled_antibody_biodistribution
Analyzes radiolabeled antibody biodistribution.
"""

import sys
import json
from biomni.tool.pharmacology import analyze_radiolabeled_antibody_biodistribution


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
        print(json.dumps({"error": "Usage: analyze_radiolabeled_antibody_biodistribution.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        time_points = args.get('time_points')
        tissue_data = args.get('tissue_data')

        if not time_points or not tissue_data:
            print(json.dumps({"error": "Missing required parameters: time_points, tissue_data"}))
            sys.exit(1)

        result = analyze_radiolabeled_antibody_biodistribution(
            time_points=time_points,
            tissue_data=tissue_data
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
