#!/usr/bin/env python3
"""
Camber app wrapper for analyze_bacterial_growth_rate from biomni.tool.synthetic_biology
"""

import sys
import json
from biomni.tool.synthetic_biology import analyze_bacterial_growth_rate



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
    time_points = input_data.get("time_points")
    od_measurements = input_data.get("od_measurements")
    strain_name = input_data.get("strain_name", "Unknown strain")
    output_dir = input_data.get("output_dir", "./")

    # Call the function
    result = analyze_bacterial_growth_rate(
        time_points=time_points,
        od_measurements=od_measurements,
        strain_name=strain_name,
        output_dir=output_dir
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
