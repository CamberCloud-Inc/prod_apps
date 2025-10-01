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
    from biomni.tool.pathology import analyze_atp_luminescence_assay
    parser = argparse.ArgumentParser(description='Analyze luminescence-based ATP concentration')
    parser.add_argument('data_file', help='Path to the luminescence data file containing sample measurements')
    parser.add_argument('standard_curve_file', help='Path to the standard curve calibration data file')
    parser.add_argument('--normalization-method', default='cell_count',
                        help='Method for normalizing ATP values - options include cell_count, protein, or none (default: cell_count)')
    parser.add_argument('--normalization-data', default=None,
                        help='JSON string or file path for normalization factors or metadata for sample-specific corrections')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Parse normalization_data if provided
    normalization_data = None
    if args.normalization_data:
        try:
            if os.path.isfile(args.normalization_data):
                with open(args.normalization_data, 'r') as f:
                    normalization_data = json.load(f)
            else:
                normalization_data = json.loads(args.normalization_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing normalization_data: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading normalization_data: {e}")
            sys.exit(1)

    print(f"\nAnalyzing ATP luminescence assay...")
    print(f"Data file: {args.data_file}")
    print(f"Standard curve file: {args.standard_curve_file}")

    try:
        result = analyze_atp_luminescence_assay(
            args.data_file,
            standard_curve_file=args.standard_curve_file,
            normalization_method=args.normalization_method,
            normalization_data=normalization_data
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
