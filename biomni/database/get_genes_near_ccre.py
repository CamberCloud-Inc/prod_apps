"""
Camber wrapper for biomni.tool.database.get_genes_near_ccre
"""

from biomni.tool.database import get_genes_near_ccre
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

def main(accession, assembly, chromosome, k=10) -> str:
    """Given a cCRE (Candidate cis-Regulatory Element), this function returns a string containing the
    steps it performs and the k nearest genes sorted by distance.

    Parameters
    ----------
    - accession (str):
    """
    Wrapper for get_genes_near_ccre from biomni.tool.database
    
    Query the ReMap database for regulatory elements and transcription factor binding sites.

    Parameters
    ----------
    prompt (str, required): Natural language query about transcription factors and binding sites
    endpoint (str, optional): Full API endpoint to query (e.g., "https://remap.univ-amu.fr/api/v1/catalogue/tf?tf=CTCF")
    verbose (bool): Whether to return detailed results

    Returns
    -------
    dict: Dictionary containing the query results or error information

    Exampl
    """
    result = get_genes_near_ccre(accession=accession, assembly=assembly, chromosome=chromosome, k=k)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='get_genes_near_ccre')
    parser.add_argument('--accession', type=str, required=True, help='accession')
    parser.add_argument('--assembly', type=str, required=True, help='assembly')
    parser.add_argument('--chromosome', type=str, required=True, help='chromosome')
    parser.add_argument('--k', type=int, default=10) -> str:
    """Given a cCRE (Candidate cis-Regulatory Element), this function returns a string containing the
    steps it performs and the k nearest genes sorted by distance.

    Parameters
    ----------
    - accession (str, help='k')
    
    args = parser.parse_args()
    main(**vars(args))
