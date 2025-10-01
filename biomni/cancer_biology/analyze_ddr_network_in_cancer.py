#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_ddr_network_in_cancer tool
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
    from biomni.tool.cancer_biology import analyze_ddr_network_in_cancer
    if len(sys.argv) != 2:
        print("Usage: analyze_ddr_network_in_cancer.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        params = json.load(f)

    expression_data_path = params['expression_data_path']
    mutation_data_path = params['mutation_data_path']
    output_dir = params.get('output_dir', './results')

    result = analyze_ddr_network_in_cancer(
        expression_data_path=expression_data_path,
        mutation_data_path=mutation_data_path,
        output_dir=output_dir
    )

    print(result)


if __name__ == '__main__':
    main()
