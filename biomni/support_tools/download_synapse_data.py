#!/usr/bin/env python3
"""Biomni Tool: Download Synapse Data
Wraps: biomni.tool.support_tools.download_synapse_data
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
        description='Download data from Synapse repository'
    )
    parser.add_argument('entity_ids', nargs='+', help='Synapse entity IDs to download (e.g., syn12345678)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for downloaded files (default: ./)')
    parser.add_argument('--download-location', default=None,
                        help='Target directory path for downloaded files (optional)')
    parser.add_argument('--follow-link', action='store_true',
                        help='Follow symbolic links in Synapse')
    parser.add_argument('--recursive', action='store_true',
                        help='Recursively download folders and subfolders')
    parser.add_argument('--timeout', type=int, default=300,
                        help='Download timeout in seconds (default: 300)')
    parser.add_argument('--entity-type', default='file',
                        choices=['file', 'folder', 'project'],
                        help='Type of entity (default: file)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.support_tools import download_synapse_data

    result = download_synapse_data(
        entity_ids=args.entity_ids,
        download_location=args.download_location,
        follow_link=args.follow_link,
        recursive=args.recursive,
        timeout=args.timeout,
        entity_type=args.entity_type
    )

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'download_result.txt')
    with open(output_file, 'w') as f:
        f.write(str(result))
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
