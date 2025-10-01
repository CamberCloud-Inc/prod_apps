#!/usr/bin/env python3
"""
Camber app wrapper for engineer_bacterial_genome_for_therapeutic_delivery from biomni.tool.synthetic_biology
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
    from biomni.tool.synthetic_biology import engineer_bacterial_genome_for_therapeutic_delivery
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    bacterial_genome_file = input_data.get("bacterial_genome_file")
    genetic_parts = input_data.get("genetic_parts")

    # Call the function
    result = engineer_bacterial_genome_for_therapeutic_delivery(
        bacterial_genome_file=bacterial_genome_file,
        genetic_parts=genetic_parts
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
