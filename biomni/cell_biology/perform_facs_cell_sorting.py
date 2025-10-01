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
    from biomni.tool.cell_biology import perform_facs_cell_sorting
    parser = argparse.ArgumentParser(description='Perform FACS cell sorting')
    parser.add_argument('cell_suspension_data', help='Path to the FCS file containing flow cytometry data')
    parser.add_argument('fluorescence_parameter', help='Name of the fluorescence channel to use for sorting decisions')
    parser.add_argument('--threshold-min', type=float, default=None,
                        help='Minimum fluorescence intensity threshold for the sort gate')
    parser.add_argument('--threshold-max', type=float, default=None,
                        help='Maximum fluorescence intensity threshold for the sort gate')
    parser.add_argument('--output-file', default='sorted_cells.csv',
                        help='Filename for the sorted cell data CSV export (default: sorted_cells.csv)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nPerforming FACS cell sorting...")
    print(f"Cell suspension data: {args.cell_suspension_data}")
    print(f"Fluorescence parameter: {args.fluorescence_parameter}")

    try:
        result = perform_facs_cell_sorting(
            args.cell_suspension_data,
            args.fluorescence_parameter,
            threshold_min=args.threshold_min,
            threshold_max=args.threshold_max,
            output_file=args.output_file
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
