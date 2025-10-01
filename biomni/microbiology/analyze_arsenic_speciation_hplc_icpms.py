#!/usr/bin/env python3
"""
Analyzes arsenic speciation in liquid samples using HPLC-ICP-MS technique.
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
    from biomni.tool.microbiology import analyze_arsenic_speciation_hplc_icpms
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    sample_data = input_data.get('sample_data')
    sample_name = input_data.get('sample_name', 'Unknown Sample')
    calibration_data = input_data.get('calibration_data')

    # Call the function
    result = analyze_arsenic_speciation_hplc_icpms(
        sample_data=sample_data,
        sample_name=sample_name,
        calibration_data=calibration_data
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
