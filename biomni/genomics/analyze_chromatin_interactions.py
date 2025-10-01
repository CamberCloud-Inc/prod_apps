#!/usr/bin/env python3
"""Biomni Tool: Analyze Chromatin Interactions
Wraps: biomni.tool.genomics.analyze_chromatin_interactions
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni', 'cooler', 'numpy', 'pandas', 'scipy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Analyze chromatin interactions from Hi-C data to identify enhancer-promoter interactions and TADs'
    )
    parser.add_argument('hic_file', help='Hi-C data file (.cool or .hic format) from stash')
    parser.add_argument('regulatory_bed', help='BED file with regulatory elements from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import analyze_chromatin_interactions

    result = analyze_chromatin_interactions(
        hic_file_path=args.hic_file,
        regulatory_elements_bed=args.regulatory_bed,
        output_dir=args.output
    )

    output_file = os.path.join(args.output, 'chromatin_analysis_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
