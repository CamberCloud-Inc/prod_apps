#!/usr/bin/env python3
"""
Camber wrapper for list_glycoengineering_resources from biomni.tool.glycoengineering
Curate and summarize external glycoengineering tools and resources.
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
    from biomni.tool.glycoengineering import list_glycoengineering_resources

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='List glycoengineering resources')
    parser.add_argument('input_file', help='Path to input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    # Read input from file (even though no parameters are needed)
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    try:
        # Call the tool function
        result = list_glycoengineering_resources()

        # Write output to file
        os.makedirs(args.output, exist_ok=True)
        output_file = os.path.join(args.output, 'glycoengineering_resources.json')
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
