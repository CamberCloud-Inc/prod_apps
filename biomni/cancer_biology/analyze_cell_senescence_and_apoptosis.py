#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_cell_senescence_and_apoptosis tool
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
    from biomni.tool.cancer_biology import analyze_cell_senescence_and_apoptosis
    if len(sys.argv) != 2:
        print("Usage: analyze_cell_senescence_and_apoptosis.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        params = json.load(f)

    fcs_file_path = params['fcs_file_path']

    result = analyze_cell_senescence_and_apoptosis(fcs_file_path=fcs_file_path)

    print(result)


if __name__ == '__main__':
    main()
