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
    parser.add_argument('-s', '--sequence', required=True, help='Protein sequence to analyze')
    parser.add_argument('-w', '--window', type=int, default=7,
                        help='Sliding window size for S/T enrichment calculation (default: 7)')
    parser.add_argument('-m', '--min-st-fraction', type=float, default=0.4,
                        help='Minimum S/T fraction to consider as hotspot (default: 0.4)')
    parser.add_argument('-d', '--disallow-proline-next', action='store_true', default=True,
                        help='Exclude S/T residues followed by proline (default: True)')
    parser.add_argument('--allow-proline-next', dest='disallow_proline_next', action='store_false',
                        help='Allow S/T residues followed by proline')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    try:
        # Call the tool function
        result = predict_o_glycosylation_hotspots(
            sequence=args.sequence,
            window=args.window,
            min_st_fraction=args.min_st_fraction,
            disallow_proline_next=args.disallow_proline_next
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
