#!/usr/bin/env python3
"""Biomni Tool: Analyze Cas9 Mutation Outcomes
Wraps: biomni.tool.genetics.analyze_cas9_mutation_outcomes
"""
import subprocess
import sys
import argparse
import json
import os

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython", "pandas"])




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
    from biomni.tool.genetics import analyze_cas9_mutation_outcomes
    parser = argparse.ArgumentParser(description='Analyze and categorize mutations induced by Cas9 at target sites')
    parser.add_argument('reference_sequences', help='Path to JSON file with reference sequences (dict mapping seq_id to sequence)')
    parser.add_argument('edited_sequences', help='Path to JSON file with edited sequences (nested dict: {seq_id: {read_id: sequence}})')
    parser.add_argument('-c', '--cell-line-info', help='Path to JSON file with cell line information (optional)')
    parser.add_argument('-p', '--output-prefix', default='cas9_mutation_analysis',
                        help='Prefix for output files (default: cas9_mutation_analysis)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    print(f"Starting Cas9 mutation outcome analysis...")
    print(f"Reference sequences file: {args.reference_sequences}")
    print(f"Edited sequences file: {args.edited_sequences}")

    try:
        # Load reference sequences
        print("\nLoading reference sequences...")
        with open(args.reference_sequences, 'r') as f:
            reference_sequences = json.load(f)
        print(f"Loaded {len(reference_sequences)} reference sequences")

        # Load edited sequences
        print("Loading edited sequences...")
        with open(args.edited_sequences, 'r') as f:
            edited_sequences = json.load(f)
        print(f"Loaded edited sequences for {len(edited_sequences)} target sites")

        # Load cell line info if provided
        cell_line_info = None
        if args.cell_line_info:
            print("Loading cell line information...")
            with open(args.cell_line_info, 'r') as f:
                cell_line_info = json.load(f)
            print(f"Loaded cell line info for {len(cell_line_info)} sequences")

        # Create output directory
        os.makedirs(args.output, exist_ok=True)

        # Update output prefix to include directory
        output_prefix = os.path.join(args.output, args.output_prefix)

        result = analyze_cas9_mutation_outcomes(
            reference_sequences=reference_sequences,
            edited_sequences=edited_sequences,
            cell_line_info=cell_line_info,
            output_prefix=output_prefix
        )

        # Save full results to log file
        output_file = os.path.join(args.output, f"{args.output_prefix}_log.txt")
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")

    except Exception as e:
        print(f"Error during Cas9 mutation analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
