import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import os
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Generate XML sitemaps from URL lists')
    parser.add_argument('input_file', help='Path to the input file (one URL per line)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for sitemap (default: ./)')
    parser.add_argument('-n', '--name', default='sitemap',
                        help='Output filename (without extension) (default: sitemap)')
    parser.add_argument('-p', '--priority', type=float, default=0.5,
                        help='Default priority for URLs (0.0-1.0, default: 0.5)')
    parser.add_argument('-f', '--frequency', default='weekly',
                        choices=['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'],
                        help='Default change frequency (default: weekly)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        sys.exit(1)

    # Validate priority range
    if not 0.0 <= args.priority <= 1.0:
        print(f"Error: Priority must be between 0.0 and 1.0")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nReading URL list: {input_path}")

    # Read URLs from file
    urls = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                url = line.strip()
                if url and not url.startswith('#'):  # Skip empty lines and comments
                    # Basic URL validation
                    if not (url.startswith('http://') or url.startswith('https://')):
                        print(f"Warning: Line {line_num}: '{url}' doesn't start with http:// or https://")
                    urls.append(url)

        if not urls:
            print("Error: No valid URLs found in input file")
            sys.exit(1)

        print(f"Found {len(urls)} valid URLs")
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Create XML sitemap
    print(f"\nGenerating XML sitemap...")

    # Create root element with namespace
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    # Get current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Add each URL as a url element
    for url in urls:
        url_element = ET.SubElement(urlset, 'url')

        loc = ET.SubElement(url_element, 'loc')
        loc.text = url

        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = current_date

        changefreq = ET.SubElement(url_element, 'changefreq')
        changefreq.text = args.frequency

        priority = ET.SubElement(url_element, 'priority')
        priority.text = str(args.priority)

    # Generate pretty-printed XML
    rough_string = ET.tostring(urlset, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding='UTF-8')

    # Remove extra blank lines
    pretty_xml_str = b'\n'.join([line for line in pretty_xml.split(b'\n') if line.strip()])

    # Write to file
    output_filename = f"{args.name}.xml"
    output_path = os.path.join(args.output_dir, output_filename)

    try:
        with open(output_path, 'wb') as f:
            f.write(pretty_xml_str)
        print(f"Sitemap saved to: {output_path}")
        print(f"Total URLs in sitemap: {len(urls)}")
        print(f"Default priority: {args.priority}")
        print(f"Default change frequency: {args.frequency}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("\nSitemap generation completed successfully!")
    print(f"\nUsage tips:")
    print(f"  - Upload the sitemap to your website's root directory")
    print(f"  - Submit to search engines via Google Search Console, Bing Webmaster Tools, etc.")
    print(f"  - Add sitemap location to robots.txt: Sitemap: https://yoursite.com/{args.name}.xml")


if __name__ == "__main__":
    main()