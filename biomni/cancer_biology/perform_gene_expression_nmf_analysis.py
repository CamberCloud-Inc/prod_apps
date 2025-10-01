#!/usr/bin/env python3
"""
Wrapper for Biomni perform_gene_expression_nmf_analysis tool
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
    from biomni.tool.cancer_biology import perform_gene_expression_nmf_analysis
    if len(sys.argv) != 2:
        print("Usage: perform_gene_expression_nmf_analysis.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        params = json.load(f)

    expression_data_path = params['expression_data_path']
    n_components = params.get('n_components', 5)
    output_dir = params.get('output_dir', './results')

    result = perform_gene_expression_nmf_analysis(
        expression_data_path=expression_data_path,
        n_components=n_components,
        output_dir=output_dir
    )

    print(result)


if __name__ == '__main__':
    main()
