#!/usr/bin/env python3
"""
Wrapper for Biomni compare_protein_structures tool
"""
import sys


def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.systems_biology import compare_protein_structures
    if len(sys.argv) < 3:
        print("Usage: compare_protein_structures.py <pdb_file1> <pdb_file2> [chain_id1] [chain_id2] [output_prefix]")
        sys.exit(1)

    pdb_file1 = sys.argv[1]
    pdb_file2 = sys.argv[2]
    chain_id1 = sys.argv[3] if len(sys.argv) > 3 else "A"
    chain_id2 = sys.argv[4] if len(sys.argv) > 4 else "A"
    output_prefix = sys.argv[5] if len(sys.argv) > 5 else "protein_comparison"

    result = compare_protein_structures(pdb_file1, pdb_file2, chain_id1, chain_id2, output_prefix)
    print(result)

if __name__ == "__main__":
    main()
