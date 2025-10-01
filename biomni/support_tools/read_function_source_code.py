#!/usr/bin/env python3
"""Biomni Tool: Read Function Source Code
Wraps: biomni.tool.support_tools.read_function_source_code
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Read the source code of a biomni function'
    )
    parser.add_argument('function_name', help='Fully qualified function name (e.g., biomni.tool.support_tools.run_python_repl)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for source code file (default: ./)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.support_tools import read_function_source_code

    result = read_function_source_code(function_name=args.function_name)

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'source_code.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
