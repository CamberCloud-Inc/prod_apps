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
    from biomni.tool.pathology import analyze_bone_microct_morphometry
    parser = argparse.ArgumentParser(description='Analyze bone microarchitecture parameters from 3D micro-CT images')
    parser.add_argument('input_file_path', help='Path to the 3D micro-CT image file (DICOM, TIFF stack, or NIfTI format)')
    parser.add_argument('--output-dir', default='./results',
                        help='Directory for saving analysis results (default: ./results)')
    parser.add_argument('--threshold-value', type=float, default=None,
                        help='Custom threshold for bone segmentation; if not provided, automatic thresholding is applied (optional)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nAnalyzing bone micro-CT morphometry...")
    print(f"Input file path: {args.input_file_path}")

    try:
        result = analyze_bone_microct_morphometry(
            args.input_file_path,
            output_dir=args.output_dir,
            threshold_value=args.threshold_value
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
