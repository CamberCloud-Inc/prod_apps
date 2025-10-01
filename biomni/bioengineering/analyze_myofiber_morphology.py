import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scikit-image"])




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
    from biomni.tool.bioengineering import analyze_myofiber_morphology
    parser = argparse.ArgumentParser(description='Quantify morphological properties of myofibers in microscopy images')
    parser.add_argument('--image_path', required=True, help='Path to the multichannel fluorescence microscopy image file')
    parser.add_argument('--nuclei_channel', type=int, default=2, help='Channel index containing nuclei staining (default: 2)')
    parser.add_argument('--myofiber_channel', type=int, default=1, help='Channel index containing myofiber membrane staining (default: 1)')
    parser.add_argument('--threshold_method', default='otsu', help='Segmentation threshold algorithm (default: otsu)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    image_path = os.path.expanduser(args.image_path)
    nuclei_channel = args.nuclei_channel
    myofiber_channel = args.myofiber_channel
    threshold_method = args.threshold_method

    print(f"Analyzing myofiber morphology from: {image_path}")

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at: {image_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_myofiber_morphology(
            image_path=image_path,
            nuclei_channel=nuclei_channel,
            myofiber_channel=myofiber_channel,
            threshold_method=threshold_method,
            output_dir=args.output
        )

        # Write result to file
        output_file = os.path.join(args.output, 'myofiber_morphology_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
