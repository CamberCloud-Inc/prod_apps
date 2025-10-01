import json
import sys
import os
import argparse



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
    from biomni.tool.cell_biology import analyze_flow_cytometry_immunophenotyping
    parser = argparse.ArgumentParser(description='Analyze flow cytometry immunophenotyping data')
    parser.add_argument('fcs_file_path', help='Path to the FCS file containing flow cytometry data')
    parser.add_argument('gating_strategy', help='JSON string or file path defining sequential gates to identify cell populations')
    parser.add_argument('--compensation-matrix', default=None,
                        help='JSON string or file path for compensation matrix to correct for fluorescence spillover')
    parser.add_argument('--output-dir', default='./results',
                        help='Directory path where results will be saved (default: ./results)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Parse gating_strategy - can be JSON string or file path
    try:
        if os.path.isfile(args.gating_strategy):
            with open(args.gating_strategy, 'r') as f:
                gating_strategy = json.load(f)
        else:
            gating_strategy = json.loads(args.gating_strategy)
    except json.JSONDecodeError as e:
        print(f"Error parsing gating_strategy: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading gating_strategy: {e}")
        sys.exit(1)

    # Parse compensation_matrix if provided
    compensation_matrix = None
    if args.compensation_matrix:
        try:
            if os.path.isfile(args.compensation_matrix):
                with open(args.compensation_matrix, 'r') as f:
                    compensation_matrix = json.load(f)
            else:
                compensation_matrix = json.loads(args.compensation_matrix)
        except json.JSONDecodeError as e:
            print(f"Error parsing compensation_matrix: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading compensation_matrix: {e}")
            sys.exit(1)

    print(f"\nAnalyzing flow cytometry immunophenotyping...")
    print(f"FCS file: {args.fcs_file_path}")
    print(f"Gating strategy: {gating_strategy}")

    try:
        result = analyze_flow_cytometry_immunophenotyping(
            args.fcs_file_path,
            gating_strategy=gating_strategy,
            compensation_matrix=compensation_matrix,
            output_dir=args.output_dir
        )

        # Generate output filename
        output_filename = "result.json"
        output_path = os.path.join(args.output, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"research_log": result}, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
