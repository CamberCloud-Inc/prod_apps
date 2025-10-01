#!/usr/bin/env python3
"""
Split 4D NIfTI medical imaging file into separate modality files.
"""

import sys
import json
from biomni.tool.bioimaging import split_modalities



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
    if len(sys.argv) != 2:
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)

    input_file = config['input_file']
    output_dir = config['output_dir']
    case_name = config.get('case_name', 'BRAT')

    result = split_modalities(
        input_file=input_file,
        output_dir=output_dir,
        case_name=case_name
    )

    print(json.dumps({
        "output_dir": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
