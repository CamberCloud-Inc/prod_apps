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
    from biomni.tool.pathology import quantify_corneal_nerve_fibers
    parser = argparse.ArgumentParser(description='Quantify immunofluorescence-labeled corneal nerve fibers')
    parser.add_argument('image_path', help='Path to the immunofluorescence image of corneal nerve fibers')
    parser.add_argument('marker_type', help='Type of neuronal marker used (e.g., beta-III-tubulin, PGP9.5, Thy1)')
    parser.add_argument('--output-dir', default='./output',
                        help='Directory where analysis results will be saved (default: ./output)')
    parser.add_argument('--threshold-method', default='otsu',
                        help='Segmentation threshold method - options include otsu, adaptive, or manual (default: otsu)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nQuantifying corneal nerve fibers...")
    print(f"Image path: {args.image_path}")
    print(f"Marker type: {args.marker_type}")

    try:
        result = quantify_corneal_nerve_fibers(
            args.image_path,
            marker_type=args.marker_type,
            output_dir=args.output_dir,
            threshold_method=args.threshold_method
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
