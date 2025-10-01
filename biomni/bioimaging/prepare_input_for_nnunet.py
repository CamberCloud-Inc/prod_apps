#!/usr/bin/env python3
"""
Prepare input data for nnUNet processing.
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
    from biomni.tool.bioimaging import prepare_input_for_nnunet
    if len(sys.argv) != 2:
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)

    input_path = config['input_path']
    output_dir = config['output_dir']
    case_name = config.get('case_name', 'BRAT')

    result = prepare_input_for_nnunet(
        input_path=input_path,
        output_dir=output_dir,
        case_name=case_name
    )

    print(json.dumps({
        "prepared_dir": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
