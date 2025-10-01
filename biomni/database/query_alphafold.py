"""
Camber wrapper for biomni.tool.database.query_alphafold
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

def main(uniprot_id, endpoint="prediction", residue_range=None, download=False, output_dir=None, file_format="pdb", model_version="v4", model_number=1):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_alphafold
    """
    Wrapper for query_alphafold from biomni.tool.database
    
    Query the AlphaFold Database API for protein structure predictions.

    Parameters
    ----------
    uniprot_id (str): UniProt accession ID (e.g., "P12345")
    endpoint (str, optional): Specific AlphaFold API endpoint to query:
                            "prediction", "summary", or "annotations"
    residue_range (str, optional): Specific residue range in format "start-end" (e.g., "1-100")
    download (bool): Whether to download structure files
    output_dir (str, optional): Directory to s
    """
    result = query_alphafold(uniprot_id=uniprot_id, endpoint=endpoint, residue_range=residue_range, download=download, output_dir=output_dir, file_format=file_format, model_version=model_version, model_number=model_number)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_alphafold')
    parser.add_argument('--uniprot_id', type=str, required=True, help='uniprot_id')
    parser.add_argument('--endpoint', type=str, default="prediction", help='endpoint')
    parser.add_argument('--residue_range', type=str, default=None, help='residue_range')
    parser.add_argument('--download', type=bool, default=False, help='download')
    parser.add_argument('--output_dir', type=str, default=None, help='output_dir')
    parser.add_argument('--file_format', type=str, default="pdb", help='file_format')
    parser.add_argument('--model_version', type=str, default="v4", help='model_version')
    parser.add_argument('--model_number', type=int, default=1, help='model_number')
    
    args = parser.parse_args()
    main(**vars(args))
