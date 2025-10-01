"""
Camber wrapper for biomni.tool.database.blast_sequence
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

def main(sequence, database, program):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import blast_sequence
    """
    Wrapper for blast_sequence from biomni.tool.database
    
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
    result = blast_sequence(sequence=sequence, database=database, program=program)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='blast_sequence')
    parser.add_argument('--sequence', type=str, required=True, help='sequence')
    parser.add_argument('--database', type=str, required=True, help='database')
    parser.add_argument('--program', type=float, required=True, help='program')
    
    args = parser.parse_args()
    main(**vars(args))
