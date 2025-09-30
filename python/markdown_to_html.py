import subprocess
import sys
import os
import argparse

# Install markdown library
subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])

import markdown


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to HTML')
    parser.add_argument('input_file', help='Path to the Markdown (.md) file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for HTML file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")
    print(f"Absolute input_path: {os.path.abspath(input_path)}")

    if not os.path.exists(input_path):
        print(f"Error: Markdown file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read the markdown file
    print(f"Reading markdown file: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert markdown to HTML
    print("Converting markdown to HTML...")
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])

    # Create full HTML document
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted from Markdown</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
        }}
        code {{
            background: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: "Courier New", monospace;
        }}
        pre {{
            background: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 10px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            border: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 16px;
            margin-left: 0;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background: #f4f4f4;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

    # Generate output filename (replace .md with .html)
    base_name = os.path.basename(input_path)
    if base_name.endswith('.md'):
        output_name = base_name[:-3] + '.html'
    else:
        output_name = base_name + '.html'

    output_path = os.path.join(args.output_dir, output_name)

    # Write the HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_document)

    print(f"Successfully converted markdown to HTML: {output_path}")
    print("Conversion completed!")


if __name__ == "__main__":
    main()