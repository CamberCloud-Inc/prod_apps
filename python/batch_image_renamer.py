import os
import sys
import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Rename multiple images with patterns')
    parser.add_argument('input_dir', help='Path to directory containing images')
    parser.add_argument('-p', '--pattern', default='image_{n}',
                        help='Naming pattern (use {n} for number, {original} for original name) (default: image_{n})')
    parser.add_argument('-s', '--start', type=int, default=1,
                        help='Starting number for sequential numbering (default: 1)')
    parser.add_argument('-e', '--extension', default=None,
                        help='Filter by extension (e.g., jpg, png). If not specified, renames all image files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without actually renaming files')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_dir argument: {args.input_dir}")

    # Expand user path if provided
    input_dir = os.path.expanduser(args.input_dir)
    print(f"Absolute input_dir: {os.path.abspath(input_dir)}")

    if not os.path.exists(input_dir):
        print(f"Error: Directory not found at: {input_dir}")
        sys.exit(1)

    if not os.path.isdir(input_dir):
        print(f"Error: Path is not a directory: {input_dir}")
        sys.exit(1)

    # Common image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic'}

    # Get all image files
    all_files = sorted(os.listdir(input_dir))
    image_files = []

    for filename in all_files:
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        # Filter by extension if specified
        if args.extension:
            if ext == f'.{args.extension.lower()}' or ext.lstrip('.') == args.extension.lower():
                image_files.append(filename)
        elif ext in image_extensions:
            image_files.append(filename)

    if not image_files:
        print(f"No image files found in directory: {input_dir}")
        if args.extension:
            print(f"Filter was applied: .{args.extension}")
        sys.exit(1)

    print(f"\nFound {len(image_files)} image file(s) to rename")

    # Process renaming
    counter = args.start
    renamed_count = 0

    for original_filename in image_files:
        original_base, original_ext = os.path.splitext(original_filename)

        # Build new filename based on pattern
        new_base = args.pattern.replace('{n}', str(counter).zfill(3))
        new_base = new_base.replace('{original}', original_base)
        new_filename = f"{new_base}{original_ext}"

        original_path = os.path.join(input_dir, original_filename)
        new_path = os.path.join(input_dir, new_filename)

        # Skip if names are the same
        if original_filename == new_filename:
            print(f"Skipping: {original_filename} (no change needed)")
            counter += 1
            continue

        # Check if target file already exists
        if os.path.exists(new_path) and original_path != new_path:
            print(f"Warning: {new_filename} already exists. Skipping {original_filename}")
            counter += 1
            continue

        if args.dry_run:
            print(f"Would rename: {original_filename} -> {new_filename}")
        else:
            try:
                os.rename(original_path, new_path)
                print(f"Renamed: {original_filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {original_filename}: {e}")

        counter += 1

    if args.dry_run:
        print("\n=== DRY RUN MODE ===")
        print("No files were actually renamed. Remove --dry-run to apply changes.")
    else:
        print(f"\nBatch renaming completed! {renamed_count} file(s) renamed.")


if __name__ == "__main__":
    main()