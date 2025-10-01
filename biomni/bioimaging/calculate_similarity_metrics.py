#!/usr/bin/env python3
"""
Calculate similarity metrics between two medical images.
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
    from biomni.tool.bioimaging import calculate_similarity_metrics
    if len(sys.argv) != 2:
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)

    image1_path = config['image1_path']
    image2_path = config['image2_path']

    result = calculate_similarity_metrics(
        image1_path=image1_path,
        image2_path=image2_path
    )

    print(json.dumps({
        "metrics": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
