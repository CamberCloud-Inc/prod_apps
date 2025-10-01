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
    parser.add_argument('--image_sequence_path', required=True, help='Path to directory containing time-lapse microscopy images or path to a multi-frame TIFF file')
    parser.add_argument('--pixel_size_um', type=float, default=1.0, help='Physical size of each pixel in micrometers (default: 1.0)')
    parser.add_argument('--time_interval_min', type=float, default=1.0, help='Time interval between consecutive frames in minutes (default: 1.0)')
    parser.add_argument('--min_track_length', type=int, default=10, help='Minimum number of frames a cell must be tracked (default: 10)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    image_sequence_path = os.path.expanduser(args.image_sequence_path)
    pixel_size_um = args.pixel_size_um
    time_interval_min = args.time_interval_min
    min_track_length = args.min_track_length

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
