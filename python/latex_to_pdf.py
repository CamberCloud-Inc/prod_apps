import subprocess
import sys
import os
import argparse
import shutil


def main():
    parser = argparse.ArgumentParser(description='Compile LaTeX documents to PDF')
    parser.add_argument('tex_path', help='Path to the LaTeX (.tex) file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for PDF file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received tex_path argument: {args.tex_path}")

    # Expand user path if provided
    tex_path = os.path.expanduser(args.tex_path)
    print(f"Expanded tex_path: {tex_path}")

    if not os.path.exists(tex_path):
        print(f"Error: LaTeX file not found at: {tex_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Check if pdflatex is available
    if not shutil.which("pdflatex"):
        print("LaTeX distribution (pdflatex) not found. Attempting to install...")
        try:
            # Detect OS and install accordingly
            import platform
            system = platform.system()

            if system == "Linux":
                subprocess.run(["apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["apt-get", "install", "-y", "texlive-latex-base", "texlive-latex-extra"],
                              check=True, capture_output=True)
                print("LaTeX distribution installed successfully")
            elif system == "Darwin":  # macOS
                print("On macOS, please install MacTeX or BasicTeX:")
                print("  brew install --cask mactex")
                print("  or: brew install --cask basictex")
                print("\nSkipping LaTeX compilation - pdflatex not available")
                sys.exit(1)
            else:
                print(f"Unsupported OS: {system}")
                print("Please install a LaTeX distribution (e.g., TeX Live) manually")
                sys.exit(1)
        except Exception as e:
            print(f"Warning: Could not install LaTeX distribution: {e}")
            sys.exit(1)

    # Get the directory containing the .tex file (for any included files/images)
    tex_dir = os.path.dirname(os.path.abspath(tex_path))
    tex_filename = os.path.basename(tex_path)
    base_name = os.path.splitext(tex_filename)[0]

    # Compile LaTeX to PDF (run pdflatex twice for references)
    print(f"Compiling LaTeX document: {tex_path}")
    try:
        # First pass
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", tex_dir, tex_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print("LaTeX compilation errors:")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)

        # Second pass (for cross-references, TOC, etc.)
        print("Running second pass for references...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", tex_dir, tex_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Move PDF to output directory
        pdf_source = os.path.join(tex_dir, f"{base_name}.pdf")
        pdf_output = os.path.join(args.output_dir, f"{base_name}.pdf")

        if os.path.exists(pdf_source):
            # Only copy if source and destination are different
            pdf_source_abs = os.path.abspath(pdf_source)
            pdf_output_abs = os.path.abspath(pdf_output)

            if pdf_source_abs != pdf_output_abs:
                shutil.copy2(pdf_source, pdf_output)
                print(f"LaTeX to PDF compilation completed! Output: {pdf_output}")
            else:
                print(f"LaTeX to PDF compilation completed! Output: {pdf_source}")

            # Clean up auxiliary files
            for ext in ['.aux', '.log', '.out']:
                aux_file = os.path.join(tex_dir, f"{base_name}{ext}")
                if os.path.exists(aux_file):
                    os.remove(aux_file)
        else:
            print(f"Error: PDF was not generated at {pdf_source}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("Error: LaTeX compilation timed out (60 seconds)")
        sys.exit(1)
    except Exception as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()