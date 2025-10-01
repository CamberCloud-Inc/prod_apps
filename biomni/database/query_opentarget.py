"""
Camber wrapper for biomni.tool.database.query_opentarget
"""

from biomni.tool.database import query_opentarget
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

def main(prompt=None, query=None, variables=None, verbose=False):
    
    install_dependencies()
    """
    Wrapper for query_opentarget from biomni.tool.database
    
    Query the OpenTargets Platform API using natural language or a direct GraphQL query.

    Parameters
    ----------
    prompt (str, required): Natural language query about drug targets, diseases, and mechanisms
    query (str, optional): Direct GraphQL query string
    variables (dict, optional): Variables for the GraphQL query
    verbose (bool): Whether to return detailed results

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
    
    """
    result = query_opentarget(prompt=prompt, query=query, variables=variables, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_opentarget')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--query', type=str, default=None, help='query')
    parser.add_argument('--variables', type=str, default=None, help='variables')
    parser.add_argument('--verbose', type=bool, default=False, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
