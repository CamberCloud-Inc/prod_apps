#!/usr/bin/env python3
"""
Camber app wrapper for optimize_codons_for_heterologous_expression from biomni.tool.synthetic_biology
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
    from biomni.tool.synthetic_biology import optimize_codons_for_heterologous_expression
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    target_sequence = input_data.get("target_sequence")
    host_codon_usage = input_data.get("host_codon_usage")

    # Call the function
    result = optimize_codons_for_heterologous_expression(
        target_sequence=target_sequence,
        host_codon_usage=host_codon_usage
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
