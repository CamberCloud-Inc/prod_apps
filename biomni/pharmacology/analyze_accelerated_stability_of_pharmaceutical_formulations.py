#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_accelerated_stability_of_pharmaceutical_formulations
Analyzes accelerated stability of pharmaceutical formulations.
"""

import sys
import json
from biomni.tool.pharmacology import analyze_accelerated_stability_of_pharmaceutical_formulations


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
        print(json.dumps({"error": "Usage: analyze_accelerated_stability_of_pharmaceutical_formulations.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        formulations = args.get('formulations')
        storage_conditions = args.get('storage_conditions')
        time_points = args.get('time_points')

        if not formulations or not storage_conditions or not time_points:
            print(json.dumps({"error": "Missing required parameters: formulations, storage_conditions, time_points"}))
            sys.exit(1)

        result = analyze_accelerated_stability_of_pharmaceutical_formulations(
            formulations=formulations,
            storage_conditions=storage_conditions,
            time_points=time_points
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
