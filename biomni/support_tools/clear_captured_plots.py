#!/usr/bin/env python3
"""
Camber wrapper for clear_captured_plots from biomni.tool.support_tools
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
    from biomni.tool.support_tools import clear_captured_plots
    """Main function for Camber app execution"""
    if len(sys.argv) != 1:
        print(json.dumps({
            "error": "Usage: clear_captured_plots.py (no arguments required)"
        }))
        sys.exit(1)

    try:
        clear_captured_plots()
        print(json.dumps({
            "success": True,
            "result": "Captured plots cleared successfully"
        }, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
