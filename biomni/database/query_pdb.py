"""
Camber wrapper for biomni.tool.database.query_pdb
"""

from biomni.tool.database import query_pdb
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

def main(prompt=None, query=None, max_results=3):
    
    install_dependencies()
    """
    Wrapper for query_pdb from biomni.tool.database
    
    Query the RCSB PDB database using natural language or a direct structured query.

    Parameters
    ----------
    prompt (str, required): Natural language query about protein structures
    query (dict, optional): Direct structured query in RCSB Search API format (overrides prompt)
    max_results (int): Maximum number of results to return

    Returns
    -------
    dict: Dictionary containing the structured query, search results, and identifiers

    Examples
    --------
    - Natural lang
    """
    result = query_pdb(prompt=prompt, query=query, max_results=max_results)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_pdb')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--query', type=str, default=None, help='query')
    parser.add_argument('--max_results', type=int, default=3, help='max_results')
    
    args = parser.parse_args()
    main(**vars(args))
