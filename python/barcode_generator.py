import subprocess
import sys
import os
import argparse

# Install python-barcode with PIL support
subprocess.check_call([sys.executable, "-m", "pip", "install", "python-barcode[images]"])

import barcode
from barcode.writer import ImageWriter


def main():
    parser = argparse.ArgumentParser(description='Generate barcodes in various formats')
    parser.add_argument('data', help='Data to encode in the barcode')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for barcode image (default: ./)')
    parser.add_argument('-n', '--name', default='barcode',
                        help='Output filename (without extension) (default: barcode)')
    parser.add_argument('-f', '--format', default='code128',
                        choices=['code128', 'code39', 'ean13', 'ean8', 'upca'],
                        help='Barcode format (default: code128)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Data to encode: {args.data}")
    print(f"Barcode format: {args.format}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate barcode
    try:
        # Get the barcode class
        barcode_class = barcode.get_barcode_class(args.format)

        # Special handling for EAN formats (they require specific lengths)
        data = args.data
        if args.format == 'ean13':
            # EAN13 requires 12 digits (checksum is calculated automatically)
            data = data.zfill(12)[:12]
            print(f"EAN13 format: padded/trimmed data to 12 digits: {data}")
        elif args.format == 'ean8':
            # EAN8 requires 7 digits (checksum is calculated automatically)
            data = data.zfill(7)[:7]
            print(f"EAN8 format: padded/trimmed data to 7 digits: {data}")
        elif args.format == 'upca':
            # UPC-A requires 11 digits (checksum is calculated automatically)
            data = data.zfill(11)[:11]
            print(f"UPC-A format: padded/trimmed data to 11 digits: {data}")

        print(f"Generating {args.format.upper()} barcode")

        # Create the barcode with ImageWriter
        bc = barcode_class(data, writer=ImageWriter())

        # Save without extension (library adds .png automatically)
        output_path_base = os.path.join(args.output_dir, args.name)
        full_path = bc.save(output_path_base)

        print(f"Successfully generated barcode")
        print(f"Output saved to: {full_path}")
        print(f"Output file size: {os.path.getsize(full_path)} bytes")
    except Exception as e:
        print(f"Error generating barcode: {e}")
        sys.exit(1)

    print("\nBarcode generation completed!")


if __name__ == "__main__":
    main()