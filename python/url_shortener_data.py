import json
import csv
import os
import argparse
import hashlib
import base64


def generate_short_code(url, length=6):
    """Generate a short code from URL using hash."""
    hash_object = hashlib.md5(url.encode())
    hash_bytes = hash_object.digest()
    short_code = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')[:length]
    return short_code


def main():
    parser = argparse.ArgumentParser(description='Generate URL shortener redirect files')
    parser.add_argument('input_file', help='Path to the input file (CSV or JSON with URLs)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for redirect files (default: ./)')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'both'], default='both',
                        help='Output format (default: both)')
    parser.add_argument('-l', '--length', type=int, default=6,
                        help='Length of short codes (default: 6)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Expanded input_file: {input_file}")
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Input file not found at: {input_file}")
        return 1

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read input file
    urls = []
    file_ext = os.path.splitext(input_file)[1].lower()

    try:
        if file_ext == '.json':
            print("\nReading JSON input file...")
            with open(input_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    urls = data
                elif isinstance(data, dict):
                    # Assume dict with 'urls' key or extract all string values
                    urls = data.get('urls', list(data.values()))
        elif file_ext == '.csv':
            print("\nReading CSV input file...")
            with open(input_file, 'r') as f:
                reader = csv.reader(f)
                # Skip header if present
                header = next(reader, None)
                for row in reader:
                    if row:
                        urls.append(row[0])
        else:
            print(f"Error: Unsupported file format: {file_ext}")
            return 1

        print(f"Read {len(urls)} URLs from input file")

    except Exception as e:
        print(f"Error reading input file: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Generate short codes and mappings
    mappings = []
    short_codes_used = set()

    print("\nGenerating short codes...")
    for i, url in enumerate(urls):
        if not url or not isinstance(url, str):
            print(f"Warning: Skipping invalid URL at index {i}: {url}")
            continue

        url = url.strip()
        if not url:
            continue

        # Generate short code
        short_code = generate_short_code(url, args.length)

        # Handle collisions
        original_code = short_code
        counter = 1
        while short_code in short_codes_used:
            short_code = generate_short_code(url + str(counter), args.length)
            counter += 1
            if counter > 1000:
                print(f"Error: Could not generate unique short code for URL: {url}")
                continue

        short_codes_used.add(short_code)
        mappings.append({
            'short_code': short_code,
            'url': url
        })

        print(f"  {short_code} -> {url[:60]}{'...' if len(url) > 60 else ''}")

    print(f"\nGenerated {len(mappings)} URL mappings")

    # Write output files
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    try:
        if args.format in ['json', 'both']:
            json_output = os.path.join(args.output_dir, f"{base_name}_redirects.json")
            with open(json_output, 'w') as f:
                json.dump(mappings, f, indent=2)
            print(f"\nJSON output saved to: {json_output}")
            print(f"JSON file size: {os.path.getsize(json_output)} bytes")

        if args.format in ['csv', 'both']:
            csv_output = os.path.join(args.output_dir, f"{base_name}_redirects.csv")
            with open(csv_output, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['short_code', 'url'])
                writer.writeheader()
                writer.writerows(mappings)
            print(f"\nCSV output saved to: {csv_output}")
            print(f"CSV file size: {os.path.getsize(csv_output)} bytes")

        # Also create a summary report
        report_output = os.path.join(args.output_dir, f"{base_name}_summary.txt")
        with open(report_output, 'w') as f:
            f.write("="*60 + "\n")
            f.write("URL SHORTENER DATA GENERATION REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Total URLs processed: {len(mappings)}\n")
            f.write(f"Short code length: {args.length}\n")
            f.write(f"\n" + "="*60 + "\n")
            f.write("MAPPINGS:\n")
            f.write("="*60 + "\n")
            for mapping in mappings:
                f.write(f"{mapping['short_code']} -> {mapping['url']}\n")
            f.write("="*60 + "\n")

        print(f"\nSummary report saved to: {report_output}")

    except Exception as e:
        print(f"Error writing output files: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\nURL shortener data generation completed!")
    return 0


if __name__ == "__main__":
    exit(main())