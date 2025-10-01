#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_autosite
Runs AutoSite to identify potential binding sites in a protein.
"""

import sys
import json
from biomni.tool.pharmacology import run_autosite


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
        print(json.dumps({"error": "Usage: run_autosite.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        pdb_file = args.get('pdb_file')
        output_dir = args.get('output_dir')
        spacing = args.get('spacing', 1.0)

        if not pdb_file or not output_dir:
            print(json.dumps({"error": "Missing required parameters: pdb_file, output_dir"}))
            sys.exit(1)

        result = run_autosite(
            pdb_file=pdb_file,
            output_dir=output_dir,
            spacing=spacing
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
