import subprocess
import sys
import os
import argparse

# Install qrcode with PIL support
subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]"])

import qrcode


def main():
    parser = argparse.ArgumentParser(description='Generate QR codes from text or URLs')
    parser.add_argument('text', help='Text or URL to encode in the QR code')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for QR code image (default: ./)')
    parser.add_argument('-n', '--name', default='qr_code',
                        help='Output filename (without extension) (default: qr_code)')
    parser.add_argument('-s', '--size', type=int, default=10,
                        help='QR code box size (default: 10)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Text to encode: {args.text}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    output_filename = f"{args.name}.png"
    output_path = os.path.join(args.output_dir, output_filename)

    # Generate QR code
    try:
        print(f"Generating QR code with box size {args.size}")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=args.size,
            border=4,
        )
        qr.add_data(args.text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)

        print(f"Successfully generated QR code")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
        print(f"Image size: {img.size}")
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)

    print("\nQR code generation completed!")


if __name__ == "__main__":
    main()