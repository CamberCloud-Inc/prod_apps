import csv
import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Extract specific columns from CSV files')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for extracted CSV (default: ./)')
    parser.add_argument('-c', '--columns', default='',
                        help='Comma-separated column names or indices to extract (e.g., "Name,Age" or "0,2,4")')
    parser.add_argument('-k', '--keep-header', action='store_true', default=True,
                        help='Keep header row in output (default: True)')

    args = parser.parse_args()

    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Parse columns to extract
    if not args.columns:
        print("Error: No columns specified. Use -c to specify columns to extract")
        print("Example: -c 'Name,Age' or -c '0,2,4'")
        sys.exit(1)

    columns_spec = [c.strip() for c in args.columns.split(',')]
    print(f"Columns to extract: {columns_spec}")

    # Read CSV file
    print(f"\nReading CSV file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            rows = list(csv_reader)

            if not rows:
                print("Error: CSV file is empty")
                sys.exit(1)

            header = rows[0]
            data_rows = rows[1:]

            print(f"CSV validation: PASSED")
            print(f"Found {len(data_rows)} data rows")
            print(f"Found {len(header)} columns: {', '.join(header)}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Determine column indices to extract
    column_indices = []
    column_names = []

    for col_spec in columns_spec:
        # Check if it's a numeric index
        if col_spec.isdigit():
            idx = int(col_spec)
            if 0 <= idx < len(header):
                column_indices.append(idx)
                column_names.append(header[idx])
            else:
                print(f"Warning: Column index {idx} out of range (0-{len(header)-1}), skipping")
        else:
            # Try to find by name
            try:
                idx = header.index(col_spec)
                column_indices.append(idx)
                column_names.append(col_spec)
            except ValueError:
                print(f"Warning: Column '{col_spec}' not found in header, skipping")

    if not column_indices:
        print("Error: No valid columns found to extract")
        sys.exit(1)

    print(f"\nExtracting {len(column_indices)} columns: {', '.join(column_names)}")

    # Extract columns
    extracted_rows = []

    # Add header if requested
    if args.keep_header:
        extracted_header = [header[i] for i in column_indices]
        extracted_rows.append(extracted_header)

    # Extract data from each row
    for row in data_rows:
        try:
            extracted_row = [row[i] if i < len(row) else '' for i in column_indices]
            extracted_rows.append(extracted_row)
        except Exception as e:
            print(f"Warning: Error extracting from row: {e}")
            continue

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_extracted.csv"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write output CSV
    print(f"\nWriting extracted columns to: {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(extracted_rows)

        print(f"Successfully extracted {len(column_indices)} columns")
        print(f"Output contains {len(extracted_rows)} rows (including header)")
        print(f"Output saved to: {output_path}")

    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("\nCSV column extraction completed!")


if __name__ == "__main__":
    main()