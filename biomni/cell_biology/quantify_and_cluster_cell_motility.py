#!/usr/bin/env python3
"""
Camber wrapper for quantify_and_cluster_cell_motility from Biomni
"""

import json
import sys




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
    from biomni.tool.cell_biology import quantify_and_cluster_cell_motility
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    image_sequence_path = input_data.get("image_sequence_path", "")
    output_dir = input_data.get("output_dir", "./results")
    num_clusters = input_data.get("num_clusters", 3)

    # Call the function
    result = quantify_and_cluster_cell_motility(
        image_sequence_path=image_sequence_path,
        output_dir=output_dir,
        num_clusters=num_clusters
    )

    # Output result as JSON
    output = {
        "research_log": result
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
