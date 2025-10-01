#!/usr/bin/env python3
"""
Camber wrapper for find_n_glycosylation_motifs from biomni.tool.glycoengineering
Scan a protein sequence for N-linked glycosylation sequons (N-X-[S/T]).
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
    from biomni.tool.glycoengineering import find_n_glycosylation_motifs

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Find N-glycosylation motifs in protein sequence')
    parser.add_argument('input_file', help='Path to input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    sequence = input_data.get("sequence")
    allow_overlap = input_data.get("allow_overlap", False)

    # Validate required parameters
    if not sequence:
        print(json.dumps({
            "error": "Missing required parameter: sequence"
        }))
        sys.exit(1)

    try:
        # Call the tool function
        result = find_n_glycosylation_motifs(
            sequence=sequence,
            allow_overlap=allow_overlap
        )

        # Write output to file
        os.makedirs(args.output, exist_ok=True)
        output_file = os.path.join(args.output, 'glycosylation_motifs.json')
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
