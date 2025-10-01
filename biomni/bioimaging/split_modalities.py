#!/usr/bin/env python3
"""
Split 4D NIfTI medical imaging file into separate modality files.
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'nibabel']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Split 4D NIfTI medical imaging file into separate modality files'
    )
    parser.add_argument('--input_file', required=True, help='Path to the input 4D NIfTI file')
    parser.add_argument('--output_dir', required=True, help='Directory for separated modality files')
    parser.add_argument('--case_name', default='BRAT', help='Identifier prefix for naming output files')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import split_modalities

    result = split_modalities(
        input_file=args.input_file,
        output_dir=args.output_dir,
        case_name=args.case_name
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'split_modalities_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "output_dir": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
