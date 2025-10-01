#!/usr/bin/env python3
"""
Camber wrapper for search_google from biomni.tool.literature
"""

import sys
import json
from biomni.tool.literature import search_google



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
    if len(sys.argv) != 4:
        print(json.dumps({
            "error": "Usage: search_google.py <query> <num_results> <language>"
        }))
        sys.exit(1)

    query = sys.argv[1]
    num_results = int(sys.argv[2])
    language = sys.argv[3]

    try:
        result = search_google(query=query, num_results=num_results, language=language)
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
