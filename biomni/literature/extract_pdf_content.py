#!/usr/bin/env python3
"""
Camber wrapper for extract_pdf_content from biomni.tool.literature
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
    from biomni.tool.literature import extract_pdf_content
    """Main function for Camber app execution"""
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "Usage: extract_pdf_content.py <url>"
        }))
        sys.exit(1)

    url = sys.argv[1]

    try:
        result = extract_pdf_content(url=url)
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
