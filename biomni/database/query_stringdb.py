"""
Camber wrapper for biomni.tool.database.query_stringdb
"""

from biomni.tool.database import query_stringdb
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

def main(prompt=None, endpoint=None, download_image=False, output_dir=None, verbose=True):
    
    install_dependencies()
    """
    Wrapper for query_stringdb from biomni.tool.database
    
    Query the STRING protein interaction database using natural language or direct endpoint.

    Parameters
    ----------
    prompt (str, required): Natural language query about protein interactions
    endpoint (str, optional): Full URL to query directly (overrides prompt)
    download_image (bool): Whether to download image results (for image endpoints)
    output_dir (str, optional): Directory to save downloaded files (default: current directory)

    Returns
    -------
    dict: Dictionary c
    """
    result = query_stringdb(prompt=prompt, endpoint=endpoint, download_image=download_image, output_dir=output_dir, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_stringdb')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--download_image', type=bool, default=False, help='download_image')
    parser.add_argument('--output_dir', type=str, default=None, help='output_dir')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
