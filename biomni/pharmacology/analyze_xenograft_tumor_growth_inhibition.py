#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_xenograft_tumor_growth_inhibition
Analyzes xenograft tumor growth inhibition data.
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
    from biomni.tool.pharmacology import analyze_xenograft_tumor_growth_inhibition
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: analyze_xenograft_tumor_growth_inhibition.py '<json_args>'"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])

        data_path = args.get('data_path')
        time_column = args.get('time_column')
        volume_column = args.get('volume_column')
        group_column = args.get('group_column')
        subject_column = args.get('subject_column')
        output_dir = args.get('output_dir', './results')

        if not data_path or not time_column or not volume_column or not group_column or not subject_column:
            print(json.dumps({"error": "Missing required parameters: data_path, time_column, volume_column, group_column, subject_column"}))
            sys.exit(1)

        result = analyze_xenograft_tumor_growth_inhibition(
            data_path=data_path,
            time_column=time_column,
            volume_column=volume_column,
            group_column=group_column,
            subject_column=subject_column,
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
