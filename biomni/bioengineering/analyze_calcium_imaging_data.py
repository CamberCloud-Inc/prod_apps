import subprocess
import sys
import os
import argparse

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scipy", "scikit-image"])




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
    from biomni.tool.bioengineering import analyze_calcium_imaging_data
    parser = argparse.ArgumentParser(description='Analyze calcium imaging data to quantify neuronal activity')
    parser.add_argument('image_stack_path', help='Path to the time-series stack of fluorescence microscopy images (TIFF format)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Expand user path if provided
    image_stack_path = os.path.expanduser(args.image_stack_path)
    print(f"Analyzing calcium imaging data from: {image_stack_path}")

    if not os.path.exists(image_stack_path):
        print(f"Error: Image stack not found at: {image_stack_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_calcium_imaging_data(
            image_stack_path=image_stack_path,
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

    print("\nCalcium imaging analysis completed successfully!")


if __name__ == "__main__":
    main()
