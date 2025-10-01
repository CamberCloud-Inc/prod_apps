#!/usr/bin/env python3
"""Biomni Tool: Run Python REPL
Wraps: biomni.tool.support_tools.run_python_repl
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
        description='Execute Python commands in a REPL environment'
    )
    parser.add_argument('command', help='Python code to execute in the persistent REPL environment')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for result file (default: ./)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.support_tools import run_python_repl

    result = run_python_repl(command=args.command)

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'repl_result.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
