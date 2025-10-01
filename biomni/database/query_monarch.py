"""
Camber wrapper for biomni.tool.database.query_monarch
"""

from biomni.tool.database import query_monarch
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

def main(prompt=None, endpoint=None, max_results=2, verbose=False):
    
    install_dependencies()
    """
    Wrapper for query_monarch from biomni.tool.database
    
    Query the Monarch Initiative API using natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, optional): Natural language query about genes, diseases, phenotypes, etc.
    endpoint (str, optional): Direct Monarch API endpoint or full URL
    max_results (int): Maximum number of results to return (if supported by endpoint)
    verbose (bool): Whether to return detailed results

    Returns
    -------
    dict: Dictionary containing the query results or error infor
    """
    result = query_monarch(prompt=prompt, endpoint=endpoint, max_results=max_results, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_monarch')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--max_results', type=int, default=2, help='max_results')
    parser.add_argument('--verbose', type=bool, default=False, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
