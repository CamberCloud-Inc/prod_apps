import os
import argparse


def generate_tree(directory, prefix="", is_last=True, max_depth=None, current_depth=0, show_hidden=False):
    """Generate a visual directory tree structure."""
    lines = []

    if max_depth is not None and current_depth >= max_depth:
        return lines

    try:
        entries = sorted(os.listdir(directory))
        if not show_hidden:
            entries = [e for e in entries if not e.startswith('.')]

        # Separate directories and files
        dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]

        # Combine: directories first, then files
        all_entries = dirs + files

        for i, entry in enumerate(all_entries):
            is_last_entry = (i == len(all_entries) - 1)
            entry_path = os.path.join(directory, entry)

            # Determine the tree characters
            if is_last_entry:
                current_prefix = "└── "
                extension_prefix = "    "
            else:
                current_prefix = "├── "
                extension_prefix = "│   "

            # Add directory indicator
            if os.path.isdir(entry_path):
                entry_display = f"{entry}/"
            else:
                entry_display = entry

            lines.append(f"{prefix}{current_prefix}{entry_display}")

            # Recursively process subdirectories
            if os.path.isdir(entry_path):
                sub_lines = generate_tree(
                    entry_path,
                    prefix + extension_prefix,
                    is_last_entry,
                    max_depth,
                    current_depth + 1,
                    show_hidden
                )
                lines.extend(sub_lines)

    except PermissionError:
        lines.append(f"{prefix}[Permission Denied]")

    return lines


def main():
    parser = argparse.ArgumentParser(description='Generate visual directory structure diagrams')
    parser.add_argument('input_dir', help='Path to the directory to analyze')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for tree diagram (default: ./)')
    parser.add_argument('-d', '--max-depth', type=int, default=None,
                        help='Maximum depth to traverse (default: unlimited)')
    parser.add_argument('-a', '--show-hidden', action='store_true',
                        help='Show hidden files and directories')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_dir argument: {args.input_dir}")

    # Expand user path if provided
    input_dir = os.path.expanduser(args.input_dir)
    print(f"Expanded input_dir: {input_dir}")
    print(f"Absolute input_dir: {os.path.abspath(input_dir)}")

    if not os.path.exists(input_dir):
        print(f"Error: Directory not found at: {input_dir}")
        return 1

    if not os.path.isdir(input_dir):
        print(f"Error: Path is not a directory: {input_dir}")
        return 1

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate the tree
    try:
        print(f"\nGenerating directory tree...")
        print(f"Max depth: {args.max_depth if args.max_depth else 'unlimited'}")
        print(f"Show hidden: {args.show_hidden}")

        # Start with the root directory name
        tree_lines = [os.path.basename(os.path.abspath(input_dir)) + "/"]

        # Generate the tree structure
        tree_lines.extend(generate_tree(
            input_dir,
            "",
            True,
            args.max_depth,
            0,
            args.show_hidden
        ))

        # Print to console
        print(f"\n{'='*60}")
        print("DIRECTORY TREE")
        print(f"{'='*60}")
        for line in tree_lines:
            print(line)
        print(f"{'='*60}")

        # Count items
        total_lines = len(tree_lines) - 1  # Exclude root
        print(f"\nTotal items: {total_lines}")

        # Write to file
        base_name = os.path.basename(os.path.abspath(input_dir))
        output_filename = f"{base_name}_tree.txt"
        output_path = os.path.join(args.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            for line in tree_lines:
                f.write(line + '\n')

        print(f"\nTree diagram saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error generating directory tree: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\nDirectory tree generation completed!")
    return 0


if __name__ == "__main__":
    exit(main())