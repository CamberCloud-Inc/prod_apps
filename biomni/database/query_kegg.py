"""
Camber wrapper for biomni.tool.database.query_kegg
"""

from biomni.tool.database import query_kegg
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

def main(prompt, endpoint=None, verbose=True):
    
    install_dependencies()
    """
    Wrapper for query_kegg from biomni.tool.database
    
    Take a natural language prompt and convert it to a structured KEGG API query.

    Parameters
    ----------
    prompt (str): Natural language query about KEGG data (e.g., "Find human pathways related to glycolysis")
    endpoint (str, optional): Direct KEGG API endpoint to query
    verbose (bool): Whether to print verbose output

    Returns
    -------
    dict: Dictionary containing both the structured query and the KEGG results
    """
    result = query_kegg(prompt=prompt, endpoint=endpoint, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_kegg')
    parser.add_argument('--prompt', type=str, required=True, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
