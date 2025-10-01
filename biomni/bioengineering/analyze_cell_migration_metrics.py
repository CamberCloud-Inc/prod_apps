import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "matplotlib", "trackpy", "scikit-image"])




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
    from biomni.tool.bioengineering import analyze_cell_migration_metrics
    parser = argparse.ArgumentParser(description='Analyze cell migration metrics from time-lapse microscopy images')
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_sequence_path = os.path.expanduser(input_data['image_sequence_path'])
    pixel_size_um = input_data.get('pixel_size_um', 1.0)
    time_interval_min = input_data.get('time_interval_min', 1.0)
    min_track_length = input_data.get('min_track_length', 10)

    print(f"Analyzing cell migration from: {image_sequence_path}")

    if not os.path.exists(image_sequence_path):
        print(f"Error: Image sequence path not found at: {image_sequence_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_cell_migration_metrics(
            image_sequence_path=image_sequence_path,
            pixel_size_um=pixel_size_um,
            time_interval_min=time_interval_min,
            min_track_length=min_track_length,
            output_dir=args.output
        )

        # Write result to file
        output_file = os.path.join(args.output, 'cell_migration_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
