#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.perform_mwas_cyp2c19_metabolizer_status
Performs methylation-wide association study (MWAS) for CYP2C19 metabolizer status.
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
    from biomni.tool.pharmacology import perform_mwas_cyp2c19_metabolizer_status
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: perform_mwas_cyp2c19_metabolizer_status.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        methylation_data_path = args.get('methylation_data_path')
        metabolizer_status_path = args.get('metabolizer_status_path')
        covariates_path = args.get('covariates_path')
        pvalue_threshold = args.get('pvalue_threshold', 0.05)
        output_file = args.get('output_file', 'significant_cpg_sites.csv')

        if not methylation_data_path or not metabolizer_status_path:
            print(json.dumps({"error": "Missing required parameters: methylation_data_path, metabolizer_status_path"}))
            sys.exit(1)

        result = perform_mwas_cyp2c19_metabolizer_status(
            methylation_data_path=methylation_data_path,
            metabolizer_status_path=metabolizer_status_path,
            covariates_path=covariates_path,
            pvalue_threshold=pvalue_threshold,
            output_file=output_file
        )

        print(json.dumps({"result": result}))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}"))
        sys.exit(1)

if __name__ == "__main__":
    main()
