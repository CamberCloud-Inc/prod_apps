#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.docking_autodock_vina
Performs docking using AutoDock Vina with specified parameters.
"""

import sys
import json
from biomni.tool.pharmacology import docking_autodock_vina


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
        print(json.dumps({"error": "Usage: docking_autodock_vina.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        smiles_list = args.get('smiles_list')
        receptor_pdb_file = args.get('receptor_pdb_file')
        box_center = args.get('box_center')
        box_size = args.get('box_size')
        ncpu = args.get('ncpu', 1)

        if not smiles_list or not receptor_pdb_file or not box_center or not box_size:
            print(json.dumps({"error": "Missing required parameters: smiles_list, receptor_pdb_file, box_center, box_size"}))
            sys.exit(1)

        # Convert to tuple if needed
        box_center = tuple(box_center) if isinstance(box_center, list) else box_center
        box_size = tuple(box_size) if isinstance(box_size, list) else box_size

        result = docking_autodock_vina(
            smiles_list=smiles_list,
            receptor_pdb_file=receptor_pdb_file,
            box_center=box_center,
            box_size=box_size,
            ncpu=ncpu
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
