"""
Camber wrapper for biomni.tool.database.query_gnomad
"""

from biomni.tool.database import query_gnomad
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

def main(prompt=None, gene_symbol=None, verbose=True):
    
    install_dependencies()
    """
    Wrapper for query_gnomad from biomni.tool.database
    
    Query gnomAD for variants in a gene using natural language or direct gene symbol.

    Parameters
    ----------
    prompt (str, required): Natural language query about genetic variants
    gene_symbol (str, optional): Gene symbol (e.g., "BRCA1")
    verbose (bool): Whether to print verbose output

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Examples
    --------
    - Direct gene: query_gnomad(gene_symbol="BRCA1")
    - Natural language: 
    """
    result = query_gnomad(prompt=prompt, gene_symbol=gene_symbol, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_gnomad')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--gene_symbol', type=str, default=None, help='gene_symbol')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
