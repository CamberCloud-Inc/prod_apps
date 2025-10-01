#!/usr/bin/env python3
"""
Prepare input data for nnUNet processing.
"""

import argparse
import sys
import json
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
    parser = argparse.ArgumentParser(
        description='Prepare input data for nnUNet processing'
    )
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import prepare_input_for_nnunet

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    input_path = config['input_path']
    output_dir = config['output_dir']
    case_name = config.get('case_name', 'BRAT')

    result = prepare_input_for_nnunet(
        input_path=input_path,
        output_dir=output_dir,
        case_name=case_name
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'nnunet_preparation_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "prepared_dir": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
