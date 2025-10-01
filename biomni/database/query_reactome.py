"""
Camber wrapper for biomni.tool.database.query_reactome
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

def main(prompt=None, endpoint=None, download=False, output_dir=None, verbose=True):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_reactome
    """
    Wrapper for query_reactome from biomni.tool.database
    
    Query the Reactome database using natural language or a direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about biological pathways
    endpoint (str, optional): Direct API endpoint or full URL
    download (bool): Whether to download pathway diagrams
    output_dir (str, optional): Directory to save downloaded files
    verbose (bool): Whether to return detailed results

    Returns
    -------
    dict: Dictionary containing the query results or
    """
    result = query_reactome(prompt=prompt, endpoint=endpoint, download=download, output_dir=output_dir, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_reactome')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--download', type=bool, default=False, help='download')
    parser.add_argument('--output_dir', type=str, default=None, help='output_dir')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
