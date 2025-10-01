#!/usr/bin/env python3
"""
Camber wrapper for run_python_repl from biomni.tool.support_tools
"""

import sys
import json
from biomni.tool.support_tools import run_python_repl



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
    """Main function for Camber app execution"""
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "Usage: run_python_repl.py <command>"
        }))
        sys.exit(1)

    command = sys.argv[1]

    try:
        result = run_python_repl(command=command)
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
