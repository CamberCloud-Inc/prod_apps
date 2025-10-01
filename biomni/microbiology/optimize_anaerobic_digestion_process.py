#!/usr/bin/env python3
"""
Optimize anaerobic digestion process conditions to maximize VFA production or methane yield.
"""

import sys
import json
import argparse
import os



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
    parser = argparse.ArgumentParser(
        description='Optimize anaerobic digestion process conditions to maximize VFA production or methane yield.'
    )
    parser.add_argument('--waste-characteristics', type=str, required=True, help='Waste composition and characteristics (JSON string)')
    parser.add_argument('--operational-parameters', type=str, required=True, help='Operational parameters to optimize (JSON string)')
    parser.add_argument('--target-output', type=str, default='methane_yield', help='Target output to maximize (methane_yield or vfa_production)')
    parser.add_argument('--optimization-method', type=str, default='rsm', help='Optimization method to use (rsm, ga, etc.)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import optimize_anaerobic_digestion_process

    # Parse JSON string parameters
    waste_characteristics = json.loads(args.waste_characteristics)
    operational_parameters = json.loads(args.operational_parameters)

    # Call the function
    result = optimize_anaerobic_digestion_process(
        waste_characteristics=waste_characteristics,
        operational_parameters=operational_parameters,
        target_output=args.target_output,
        optimization_method=args.optimization_method
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'digestion_optimization_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
