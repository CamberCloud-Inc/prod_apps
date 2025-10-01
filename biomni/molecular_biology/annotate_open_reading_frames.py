import json
import sys
import os
import argparse



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
    from biomni.tool.molecular_biology import annotate_open_reading_frames
    parser = argparse.ArgumentParser(description='Find all Open Reading Frames (ORFs) in a DNA sequence')
    parser.add_argument('sequence', help='DNA sequence')
    parser.add_argument('min_length', type=int, help='Minimum length of ORF in nucleotides')
    parser.add_argument('--search-reverse', action='store_true',
                        help='Whether to search the reverse complement strand')
    parser.add_argument('--filter-subsets', action='store_true',
                        help='Whether to filter out nested ORFs')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nFinding ORFs in DNA sequence...")
    print(f"Sequence length: {len(args.sequence)} bp")
    print(f"Minimum ORF length: {args.min_length} bp")
    print(f"Search reverse complement: {args.search_reverse}")
    print(f"Filter nested ORFs: {args.filter_subsets}")

    try:
        result = annotate_open_reading_frames(
            args.sequence,
            args.min_length,
            search_reverse=args.search_reverse,
            filter_subsets=args.filter_subsets
        )

        # Generate output filename
        output_filename = "orf_results.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        print(f"\nResults saved to: {output_path}")
        print(f"Total ORFs found: {result['summary_stats']['total_orfs']}")
        print(f"Forward strand ORFs: {result['summary_stats']['forward_orfs']}")
        print(f"Reverse strand ORFs: {result['summary_stats']['reverse_orfs']}")
        print(f"Average ORF length: {result['summary_stats']['avg_length']} bp")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nORF annotation completed successfully!")


if __name__ == "__main__":
    main()
