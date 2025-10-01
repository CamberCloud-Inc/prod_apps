#!/usr/bin/env python3
"""
Camber wrapper for get_captured_plots from biomni.tool.support_tools
"""

import sys
import json
from biomni.tool.support_tools import get_captured_plots



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
    if len(sys.argv) != 1:
        print(json.dumps({
            "error": "Usage: get_captured_plots.py (no arguments required)"
        }))
        sys.exit(1)

    try:
        result = get_captured_plots()
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
