#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_3d_chondrogenic_aggregate_assay
Runs 3D chondrogenic aggregate assay.
"""

import sys
import json
from biomni.tool.pharmacology import run_3d_chondrogenic_aggregate_assay


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
        print(json.dumps({"error": "Usage: run_3d_chondrogenic_aggregate_assay.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        chondrocyte_cells = args.get('chondrocyte_cells')
        test_compounds = args.get('test_compounds')
        culture_duration_days = args.get('culture_duration_days', 21)
        measurement_intervals = args.get('measurement_intervals', 7)

        if not chondrocyte_cells or not test_compounds:
            print(json.dumps({"error": "Missing required parameters: chondrocyte_cells, test_compounds"}))
            sys.exit(1)

        result = run_3d_chondrogenic_aggregate_assay(
            chondrocyte_cells=chondrocyte_cells,
            test_compounds=test_compounds,
            culture_duration_days=culture_duration_days,
            measurement_intervals=measurement_intervals
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
