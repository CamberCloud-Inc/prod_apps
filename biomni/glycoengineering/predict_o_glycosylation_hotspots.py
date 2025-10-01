#!/usr/bin/env python3
"""
Camber wrapper for predict_o_glycosylation_hotspots from biomni.tool.glycoengineering
Heuristic O-glycosylation hotspot scoring.
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
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.glycoengineering import predict_o_glycosylation_hotspots

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Predict O-glycosylation hotspots')
    parser.add_argument('input_file', help='Path to input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    sequence = input_data.get("sequence")
    window = input_data.get("window", 7)
    min_st_fraction = input_data.get("min_st_fraction", 0.4)
    disallow_proline_next = input_data.get("disallow_proline_next", True)

    # Validate required parameters
    if not sequence:
        print(json.dumps({
            "error": "Missing required parameter: sequence"
        }))
        sys.exit(1)

    try:
        # Call the tool function
        result = predict_o_glycosylation_hotspots(
            sequence=sequence,
            window=window,
            min_st_fraction=min_st_fraction,
            disallow_proline_next=disallow_proline_next
        )

        # Write output to file
        os.makedirs(args.output, exist_ok=True)
        output_file = os.path.join(args.output, 'o_glycosylation_hotspots.json')
        with open(output_file, 'w') as f:
            json.dump({"result": result}, f, indent=2)

        print(f"Results written to {output_file}")

    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
