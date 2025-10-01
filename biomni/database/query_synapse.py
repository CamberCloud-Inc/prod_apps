"""
Camber wrapper for biomni.tool.database.query_synapse
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

def main(prompt=None, query_term=None, return_fields=None, max_results=20, query_type="dataset", verbose=True):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_synapse
    """
    Wrapper for query_synapse from biomni.tool.database
    
    Query Synapse REST API for biomedical datasets and files.

    Synapse is a platform for sharing and analyzing biomedical data, particularly
    genomics and clinical research datasets. Supports optional authentication via
    SYNAPSE_AUTH_TOKEN environment variable for access to private datasets.

    Parameters
    ----------
    prompt : str, optional
        Natural language query about biomedical data (e.g., "Find drug screening datasets")
    query_term : str or list of str, optional
     
    """
    result = query_synapse(prompt=prompt, query_term=query_term, return_fields=return_fields, max_results=max_results, query_type=query_type, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_synapse')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--query_term', type=str, default=None, help='query_term')
    parser.add_argument('--return_fields', type=str, default=None, help='return_fields')
    parser.add_argument('--max_results', type=int, default=20, help='max_results')
    parser.add_argument('--query_type', type=str, default="dataset", help='query_type')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
