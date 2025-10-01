"""
Camber wrapper for biomni.tool.database.query_ensembl
"""

from biomni.tool.database import query_ensembl
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

def main(prompt=None, endpoint=None, verbose=True):
    
    install_dependencies()
    """
    Wrapper for query_ensembl from biomni.tool.database
    
    Query the Ensembl REST API using natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about genomic data
    endpoint (str, optional): Direct API endpoint to query (e.g., "lookup/symbol/human/BRCA2") or full URL
    verbose (bool): Whether to return detailed results

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
    --------
    - Natural language: query_ensembl("Get
    """
    result = query_ensembl(prompt=prompt, endpoint=endpoint, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_ensembl')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
