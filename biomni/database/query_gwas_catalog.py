"""
Camber wrapper for biomni.tool.database.query_gwas_catalog
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

def main(prompt=None, endpoint=None, max_results=3):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_gwas_catalog
    """
    Wrapper for query_gwas_catalog from biomni.tool.database
    
    Query the GWAS Catalog API using natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about GWAS data
    endpoint (str, optional): Full API endpoint to query (e.g., "https://www.ebi.ac.uk/gwas/rest/api/studies?diseaseTraitId=EFO_0001360")
    max_results (int): Maximum number of results to return

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
    --------
    - Natu
    """
    result = query_gwas_catalog(prompt=prompt, endpoint=endpoint, max_results=max_results)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_gwas_catalog')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--max_results', type=int, default=3, help='max_results')
    
    args = parser.parse_args()
    main(**vars(args))
