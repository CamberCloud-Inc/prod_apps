#!/usr/bin/env python3
"""
Camber wrapper for download_synapse_data from biomni.tool.support_tools
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
    from biomni.tool.support_tools import download_synapse_data
    """Main function for Camber app execution"""
    if len(sys.argv) != 7:
        print(json.dumps({
            "error": "Usage: download_synapse_data.py <entity_ids> <download_location> <follow_link> <recursive> <timeout> <entity_type>"
        }))
        sys.exit(1)

    entity_ids_str = sys.argv[1]
    download_location = sys.argv[2]
    follow_link = sys.argv[3].lower() == "true"
    recursive = sys.argv[4].lower() == "true"
    timeout = int(sys.argv[5])
    entity_type = sys.argv[6]

    # Parse entity_ids - can be a single string or JSON list
    try:
        entity_ids = json.loads(entity_ids_str)
    except json.JSONDecodeError:
        entity_ids = entity_ids_str

    try:
        result = download_synapse_data(
            entity_ids=entity_ids,
            download_location=download_location,
            follow_link=follow_link,
            recursive=recursive,
            timeout=timeout,
            entity_type=entity_type
        )
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
