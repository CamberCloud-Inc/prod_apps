#!/usr/bin/env python3
"""
Camber app wrapper for identify_fas_functional_domains from biomni.tool.synthetic_biology
"""

import sys
import json
from biomni.tool.synthetic_biology import identify_fas_functional_domains



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
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    sequence = input_data.get("sequence")
    sequence_type = input_data.get("sequence_type", "protein")
    output_file = input_data.get("output_file", "fas_domains_report.txt")

    # Call the function
    result = identify_fas_functional_domains(
        sequence=sequence,
        sequence_type=sequence_type,
        output_file=output_file
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
