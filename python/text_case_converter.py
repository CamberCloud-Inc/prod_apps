import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert text to different case formats')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for converted text (default: ./)')
    parser.add_argument('-c', '--case', default='upper',
                        choices=['upper', 'lower', 'title', 'sentence'],
                        help='Case format to convert to (default: upper)')

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

    # Read the input file
    print(f"Reading input file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Convert based on case type
    print(f"Converting text to {args.case} case...")
    if args.case == 'upper':
        converted = content.upper()
    elif args.case == 'lower':
        converted = content.lower()
    elif args.case == 'title':
        converted = content.title()
    elif args.case == 'sentence':
        # Sentence case: capitalize first letter of each sentence
        converted = '. '.join(s.strip().capitalize() for s in content.split('.') if s.strip())
        if content.rstrip().endswith('.'):
            converted += '.'

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_{args.case}.txt"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"Successfully converted text to {args.case} case")
        print(f"Output saved to: {output_path}")
        print(f"Original length: {len(content)} characters")
        print(f"Converted length: {len(converted)} characters")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Text case conversion completed!")


if __name__ == "__main__":
    main()