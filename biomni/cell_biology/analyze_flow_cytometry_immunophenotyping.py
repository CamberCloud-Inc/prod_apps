#!/usr/bin/env python3
"""
Camber wrapper for analyze_flow_cytometry_immunophenotyping from Biomni
"""

import json
import sys

from biomni.tool.cell_biology import analyze_flow_cytometry_immunophenotyping



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
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    fcs_file_path = input_data.get("fcs_file_path", "")
    gating_strategy = input_data.get("gating_strategy", {})
    compensation_matrix = input_data.get("compensation_matrix")
    output_dir = input_data.get("output_dir", "./results")

    # Call the function
    result = analyze_flow_cytometry_immunophenotyping(
        fcs_file_path=fcs_file_path,
        gating_strategy=gating_strategy,
        compensation_matrix=compensation_matrix,
        output_dir=output_dir
    )

    # Output result as JSON
    output = {
        "research_log": result
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
