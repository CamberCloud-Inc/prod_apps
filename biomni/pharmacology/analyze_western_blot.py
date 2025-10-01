#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_western_blot
Analyzes western blot images.
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
    from biomni.tool.pharmacology import analyze_western_blot
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: analyze_western_blot.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        blot_image_path = args.get('blot_image_path')
        target_bands = args.get('target_bands')
        loading_control_band = args.get('loading_control_band')
        antibody_info = args.get('antibody_info')
        output_dir = args.get('output_dir', './results')

        if not blot_image_path or not target_bands or not loading_control_band or not antibody_info:
            print(json.dumps({"error": "Missing required parameters: blot_image_path, target_bands, loading_control_band, antibody_info"}))
            sys.exit(1)

        result = analyze_western_blot(
            blot_image_path=blot_image_path,
            target_bands=target_bands,
            loading_control_band=loading_control_band,
            antibody_info=antibody_info,
            output_dir=output_dir
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
