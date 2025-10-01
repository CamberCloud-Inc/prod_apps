#!/usr/bin/env python3
"""
Biomni Tool: Analyze Bacterial Growth Curve
Wraps: biomni.tool.immunology.analyze_bacterial_growth_curve
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Bacterial Growth Curve'
    )
    parser.add_argument('--time_points', help='Array of time measurements (JSON array)')
    parser.add_argument('--od_values', help='Array of optical density measurements (JSON array)')
    parser.add_argument('--strain_name', help='Name or identifier of the bacterial strain')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_bacterial_growth_curve

    # Parse JSON arrays if provided
    time_points = json.loads(args.time_points) if args.time_points else None
    od_values = json.loads(args.od_values) if args.od_values else None

    result = analyze_bacterial_growth_curve(
        time_points=time_points,
        od_values=od_values,
        strain_name=args.strain_name,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'growth_curve_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
