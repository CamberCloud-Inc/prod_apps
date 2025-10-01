#!/usr/bin/env python3
"""
Camber wrapper for analyze_bacterial_growth_curve from biomni.tool.immunology
"""

import argparse
import sys
import json
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
        description='Analyze bacterial growth curve from OD measurements'
    )
    parser.add_argument('input_file', help='JSON file with growth curve data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    time_points = input_data['time_points']
    od_values = input_data['od_values']
    strain_name = input_data['strain_name']

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_bacterial_growth_curve

    result = analyze_bacterial_growth_curve(
        time_points=time_points,
        od_values=od_values,
        strain_name=strain_name,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'growth_curve_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
