#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_fda_safety_signals
Analyzes FDA safety signals for drugs.
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
    from biomni.tool.pharmacology import analyze_fda_safety_signals
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: analyze_fda_safety_signals.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        drug_list = args.get('drug_list')
        comparison_period = args.get('comparison_period')
        signal_threshold = args.get('signal_threshold', 2.0)

        if not drug_list:
            print(json.dumps({"error": "Missing required parameter: drug_list"}))
            sys.exit(1)

        # Convert comparison_period to tuple if it's a list
        if comparison_period and isinstance(comparison_period, list):
            comparison_period = tuple(comparison_period)

        result = analyze_fda_safety_signals(
            drug_list=drug_list,
            comparison_period=comparison_period,
            signal_threshold=signal_threshold
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
