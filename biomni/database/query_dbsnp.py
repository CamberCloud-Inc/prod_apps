"""
Camber wrapper for biomni.tool.database.query_dbsnp
"""

from biomni.tool.database import query_dbsnp
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

def main(prompt=None, search_term=None, max_results=3):
    
    install_dependencies()
    """
    Wrapper for query_dbsnp from biomni.tool.database
    
    Query the NCBI dbSNP database using natural language or a direct search term.

    Parameters
    ----------
    prompt (str, required): Natural language query about genetic variants/SNPs
    search_term (str, optional): Direct search term in dbSNP syntax
    max_results (int): Maximum number of results to return

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
    --------
    - Natural language: query_dbsnp("Find pathogenic variants 
    """
    result = query_dbsnp(prompt=prompt, search_term=search_term, max_results=max_results)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_dbsnp')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--search_term', type=str, default=None, help='search_term')
    parser.add_argument('--max_results', type=int, default=3, help='max_results')
    
    args = parser.parse_args()
    main(**vars(args))
