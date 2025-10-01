#!/usr/bin/env python3
"""
Analyze ATP Luminescence Assay

Analyze luminescence-based ATP concentration.
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
    from biomni.tool.pathology import analyze_atp_luminescence_assay
    if len(sys.argv) != 2:
        print("Usage: analyze_atp_luminescence_assay.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    data_file = inputs['data_file']
    standard_curve_file = inputs['standard_curve_file']
    normalization_method = inputs.get('normalization_method', 'cell_count')
    normalization_data = inputs.get('normalization_data', None)

    result = analyze_atp_luminescence_assay(
        data_file=data_file,
        standard_curve_file=standard_curve_file,
        normalization_method=normalization_method,
        normalization_data=normalization_data
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
