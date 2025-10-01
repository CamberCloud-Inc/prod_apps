#!/usr/bin/env python3
"""
Camber wrapper for analyze_bacterial_growth_curve from biomni.tool.immunology
"""

import sys
import json
from biomni.tool.immunology import analyze_bacterial_growth_curve



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
    if len(sys.argv) < 4:
        print("Usage: analyze_bacterial_growth_curve.py <time_points_json> <od_values_json> <strain_name> [output_dir]")
        sys.exit(1)

    time_points = json.loads(sys.argv[1])
    od_values = json.loads(sys.argv[2])
    strain_name = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else "."

    result = analyze_bacterial_growth_curve(
        time_points=time_points,
        od_values=od_values,
        strain_name=strain_name,
        output_dir=output_dir
    )

    print(result)


if __name__ == "__main__":
    main()
