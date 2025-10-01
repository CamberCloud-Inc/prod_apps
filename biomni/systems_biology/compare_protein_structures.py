#!/usr/bin/env python3
"""
Wrapper for Biomni compare_protein_structures tool
"""
import sys
import argparse
import os


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
    parser = argparse.ArgumentParser(
        description='Compare protein structures using Biomni'
    )
    parser.add_argument('pdb_file1', help='Path to the first PDB structure file')
    parser.add_argument('pdb_file2', help='Path to the second PDB structure file')
    parser.add_argument('--chain-id1', default='A', help='Chain identifier for first structure (default: A)')
    parser.add_argument('--chain-id2', default='A', help='Chain identifier for second structure (default: A)')
    parser.add_argument('--output-prefix', default='protein_comparison', help='Prefix for output files (default: protein_comparison)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    pdb_file1 = args.pdb_file1
    pdb_file2 = args.pdb_file2
    chain_id1 = args.chain_id1
    chain_id2 = args.chain_id2
    output_prefix = args.output_prefix

    # Import after dependencies are installed
    from biomni.tool.systems_biology import compare_protein_structures

    result = compare_protein_structures(pdb_file1, pdb_file2, chain_id1, chain_id2, output_prefix)

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'comparison_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
