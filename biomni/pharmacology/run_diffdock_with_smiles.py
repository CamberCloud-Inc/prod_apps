#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_diffdock_with_smiles
Runs DiffDock inference for molecular docking using a Docker container.
"""

import sys
import json
from biomni.tool.pharmacology import run_diffdock_with_smiles


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
        print(json.dumps({"error": "Usage: run_diffdock_with_smiles.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        pdb_path = args.get('pdb_path')
        smiles_string = args.get('smiles_string')
        local_output_dir = args.get('local_output_dir')
        gpu_device = args.get('gpu_device', 0)
        use_gpu = args.get('use_gpu', True)

        if not pdb_path or not smiles_string or not local_output_dir:
            print(json.dumps({"error": "Missing required parameters: pdb_path, smiles_string, local_output_dir"}))
            sys.exit(1)

        result = run_diffdock_with_smiles(
            pdb_path=pdb_path,
            smiles_string=smiles_string,
            local_output_dir=local_output_dir,
            gpu_device=gpu_device,
            use_gpu=use_gpu
        )

        print(json.dumps({"result": result}))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
