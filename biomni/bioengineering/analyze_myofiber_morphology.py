import subprocess
import sys
import os
import argparse

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
    parser.add_argument('image_path', help='Path to the microscopy image file (multichannel with nuclei and myofiber staining)')
    parser.add_argument('--nuclei-channel', type=int, default=2,
                        help='Channel index containing nuclei staining (default: 2)')
    parser.add_argument('--myofiber-channel', type=int, default=1,
                        help='Channel index containing myofiber staining (default: 1)')
    parser.add_argument('--threshold-method', choices=['otsu', 'adaptive', 'manual'], default='otsu',
                        help='Thresholding method to use (default: otsu)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Expand user path if provided
    image_path = os.path.expanduser(args.image_path)
    print(f"Analyzing myofiber morphology from: {image_path}")

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at: {image_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_myofiber_morphology(
            image_path=image_path,
            nuclei_channel=args.nuclei_channel,
            myofiber_channel=args.myofiber_channel,
            threshold_method=args.threshold_method,
            output_dir=args.output_dir
        )
        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nMyofiber morphology analysis completed successfully!")


if __name__ == "__main__":
    main()
