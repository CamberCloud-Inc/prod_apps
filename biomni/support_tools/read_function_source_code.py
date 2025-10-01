#!/usr/bin/env python3
"""
Camber wrapper for read_function_source_code from biomni.tool.support_tools
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
    from biomni.tool.support_tools import read_function_source_code
    """Main function for Camber app execution"""
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "Usage: read_function_source_code.py <function_name>"
        }))
        sys.exit(1)

    function_name = sys.argv[1]

    try:
        result = read_function_source_code(function_name=function_name)
        print(json.dumps({
            "success": True,
            "result": result
        }, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
