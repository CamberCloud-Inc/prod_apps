#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.estimate_alpha_particle_radiotherapy_dosimetry
Estimates alpha particle radiotherapy dosimetry.
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
    from biomni.tool.pharmacology import estimate_alpha_particle_radiotherapy_dosimetry
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: estimate_alpha_particle_radiotherapy_dosimetry.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        biodistribution_data = args.get('biodistribution_data')
        radiation_parameters = args.get('radiation_parameters')
        output_file = args.get('output_file', 'dosimetry_results.csv')

        if not biodistribution_data or not radiation_parameters:
            print(json.dumps({"error": "Missing required parameters: biodistribution_data, radiation_parameters"}))
            sys.exit(1)

        result = estimate_alpha_particle_radiotherapy_dosimetry(
            biodistribution_data=biodistribution_data,
            radiation_parameters=radiation_parameters,
            output_file=output_file
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
