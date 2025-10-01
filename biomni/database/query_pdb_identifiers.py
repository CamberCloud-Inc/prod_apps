"""
Camber wrapper for biomni.tool.database.query_pdb_identifiers
"""

from biomni.tool.database import query_pdb_identifiers
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

def main(identifiers, return_type="entry", download=False, attributes=None):
    
    install_dependencies()
    """
    Wrapper for query_pdb_identifiers from biomni.tool.database
    
    Retrieve detailed data and/or download files for PDB identifiers.

    Parameters
    ----------
    identifiers (list): List of PDB identifiers (from query_pdb)
    return_type (str): Type of results: "entry", "assembly", "polymer_entity", etc.
    download (bool): Whether to download PDB structure files
    attributes (list, optional): List of specific attributes to retrieve

    Returns
    -------
    dict: Dictionary containing the detailed data and file paths if downloaded

    Example:
  
    """
    result = query_pdb_identifiers(identifiers=identifiers, return_type=return_type, download=download, attributes=attributes)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_pdb_identifiers')
    parser.add_argument('--identifiers', type=str, required=True, help='identifiers')
    parser.add_argument('--return_type', type=str, default="entry", help='return_type')
    parser.add_argument('--download', type=bool, default=False, help='download')
    parser.add_argument('--attributes', type=str, default=None, help='attributes')
    
    args = parser.parse_args()
    main(**vars(args))
