#!/usr/bin/env python3
"""
Camber wrapper for advanced_web_search_claude from biomni.tool.literature
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
    from biomni.tool.literature import advanced_web_search_claude
    """Main function for Camber app execution"""
    if len(sys.argv) != 4:
        print(json.dumps({
            "error": "Usage: advanced_web_search_claude.py <query> <max_searches> <max_retries>"
        }))
        sys.exit(1)

    query = sys.argv[1]
    max_searches = int(sys.argv[2])
    max_retries = int(sys.argv[3])

    try:
        result = advanced_web_search_claude(query=query, max_searches=max_searches, max_retries=max_retries)
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
