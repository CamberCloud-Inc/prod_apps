"""
Camber wrapper for biomni.tool.database.query_clinvar
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

def main(prompt=None, search_term=None, max_results=3):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_clinvar
    """
    Wrapper for query_clinvar from biomni.tool.database
    
    Take a natural language prompt and convert it to a structured ClinVar query.

    Parameters
    ----------
    prompt (str): Natural language query about genetic variants (e.g., "Find pathogenic BRCA1 variants")
    search_term (str): Direct search term in ClinVar syntax
    max_results (int): Maximum number of results to return

    Returns
    -------
    dict: Dictionary containing both the structured query and the ClinVar results
    """
    result = query_clinvar(prompt=prompt, search_term=search_term, max_results=max_results)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_clinvar')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--search_term', type=str, default=None, help='search_term')
    parser.add_argument('--max_results', type=int, default=3, help='max_results')
    
    args = parser.parse_args()
    main(**vars(args))
