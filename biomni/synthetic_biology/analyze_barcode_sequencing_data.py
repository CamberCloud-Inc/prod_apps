#!/usr/bin/env python3
"""
Camber app wrapper for analyze_barcode_sequencing_data from biomni.tool.synthetic_biology
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
    from biomni.tool.synthetic_biology import analyze_barcode_sequencing_data
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    input_file = input_data.get("input_file")
    barcode_pattern = input_data.get("barcode_pattern")
    flanking_seq_5prime = input_data.get("flanking_seq_5prime")
    flanking_seq_3prime = input_data.get("flanking_seq_3prime")
    min_count = input_data.get("min_count", 5)
    output_dir = input_data.get("output_dir", "./results")

    # Call the function
    result = analyze_barcode_sequencing_data(
        input_file=input_file,
        barcode_pattern=barcode_pattern,
        flanking_seq_5prime=flanking_seq_5prime,
        flanking_seq_3prime=flanking_seq_3prime,
        min_count=min_count,
        output_dir=output_dir
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
