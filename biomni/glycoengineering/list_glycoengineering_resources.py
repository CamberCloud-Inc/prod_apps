#!/usr/bin/env python3
"""
Camber wrapper for list_glycoengineering_resources from biomni.tool.glycoengineering
Curate and summarize external glycoengineering tools and resources.
"""

import sys
import json
from biomni.tool.glycoengineering import list_glycoengineering_resources



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
    # Read input from stdin (even though no parameters are needed)
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    try:
        # Call the tool function
        result = list_glycoengineering_resources()

        # Output result as JSON
        output = {
            "result": result
        }
        print(json.dumps(output, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
