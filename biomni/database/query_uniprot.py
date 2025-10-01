"""
Camber wrapper for biomni.tool.database.query_uniprot
"""

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

def main(prompt=None, endpoint=None, max_results=5):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_uniprot
    """
    Wrapper for query_uniprot from biomni.tool.database
    
    Query the UniProt REST API using either natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about proteins (e.g., "Find information about human insulin")
    endpoint (str, optional): Full or partial UniProt API endpoint URL to query directly
                            (e.g., "https://rest.uniprot.org/uniprotkb/P01308")
    max_results (int): Maximum number of results to return

    Returns
    -------
    dict: Dictionary con
    """
    result = query_uniprot(prompt=prompt, endpoint=endpoint, max_results=max_results)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_uniprot')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--max_results', type=int, default=5, help='max_results')
    
    args = parser.parse_args()
    main(**vars(args))
