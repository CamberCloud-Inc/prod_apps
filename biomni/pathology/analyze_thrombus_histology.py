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
    from biomni.tool.pathology import analyze_thrombus_histology
    parser = argparse.ArgumentParser(description='Analyze histological images of thrombus samples')
    parser.add_argument('image_path', help='Path to the histological image file (H&E, Masson\'s trichrome, or immunohistochemistry)')
    parser.add_argument('--output-dir', default='./output',
                        help='Directory where analysis results will be saved (default: ./output)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nAnalyzing thrombus histology...")
    print(f"Image path: {args.image_path}")

    try:
        result = analyze_thrombus_histology(
            args.image_path,
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
