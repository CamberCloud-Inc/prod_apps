#!/usr/bin/env python3
"""
Camber wrapper for query_arxiv from biomni.tool.literature
"""

import sys
import json
from biomni.tool.literature import query_arxiv



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
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "Usage: query_arxiv.py <query> <max_papers>"
        }))
        sys.exit(1)

    query = sys.argv[1]
    max_papers = int(sys.argv[2])

    try:
        result = query_arxiv(query=query, max_papers=max_papers)
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
