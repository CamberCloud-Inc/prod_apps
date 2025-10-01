"""
Camber wrapper for biomni.tool.database.query_iucn
"""

from biomni.tool.database import query_iucn
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

def main(prompt=None, endpoint=None, token="", verbose=True):
    
    install_dependencies()
    """
    Wrapper for query_iucn from biomni.tool.database
    
    Query the IUCN Red List API using natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about species conservation status
    endpoint (str, optional): API endpoint name (e.g., "species/id/12392") or full URL
    token (str): IUCN API token - required for all queries
    verbose (bool): Whether to print verbose output

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
   
    """
    result = query_iucn(prompt=prompt, endpoint=endpoint, token=token, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_iucn')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--token', type=str, default="", help='token')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
