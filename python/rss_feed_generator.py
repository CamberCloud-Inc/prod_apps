import subprocess
import sys
import os
import argparse
import json

# Install feedgen library
subprocess.check_call([sys.executable, "-m", "pip", "install", "feedgen", "--break-system-packages"])

from feedgen.feed import FeedGenerator
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Generate RSS feeds from structured JSON data')
    parser.add_argument('input_file', help='Path to the input JSON file with feed items')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for RSS feed (default: ./)')
    parser.add_argument('-n', '--name', default='feed',
                        help='Output filename (without extension) (default: feed)')
    parser.add_argument('-t', '--title', default='My RSS Feed',
                        help='Feed title (default: My RSS Feed)')
    parser.add_argument('-l', '--link', default='https://example.com',
                        help='Feed website link (default: https://example.com)')
    parser.add_argument('-d', '--description', default='RSS Feed',
                        help='Feed description (default: RSS Feed)')

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

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nReading JSON feed data: {input_path}")

    # Read and parse JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Support both array of items or object with 'items' key
        if isinstance(data, list):
            items = data
            feed_config = {}
        elif isinstance(data, dict):
            items = data.get('items', [])
            feed_config = {
                'title': data.get('title', args.title),
                'link': data.get('link', args.link),
                'description': data.get('description', args.description),
                'author': data.get('author', None),
                'language': data.get('language', 'en')
            }
        else:
            print("Error: JSON must be an array of items or object with 'items' key")
            sys.exit(1)

        if not items:
            print("Error: No feed items found in JSON")
            sys.exit(1)

        print(f"Found {len(items)} feed items")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Create RSS feed
    print(f"\nGenerating RSS feed...")

    fg = FeedGenerator()
    fg.id(feed_config.get('link', args.link))
    fg.title(feed_config.get('title', args.title))
    fg.link(href=feed_config.get('link', args.link), rel='alternate')
    fg.description(feed_config.get('description', args.description))
    fg.language(feed_config.get('language', 'en'))

    if feed_config.get('author'):
        fg.author({'name': feed_config['author']})

    # Add each item to the feed
    for idx, item in enumerate(items, 1):
        try:
            fe = fg.add_entry()

            # Required fields
            if 'title' not in item or 'link' not in item:
                print(f"Warning: Item {idx} missing required 'title' or 'link' field, skipping")
                continue

            fe.id(item['link'])
            fe.title(item['title'])
            fe.link(href=item['link'])

            # Optional fields
            if 'description' in item:
                fe.description(item['description'])

            if 'content' in item:
                fe.content(item['content'])

            if 'author' in item:
                fe.author({'name': item['author']})

            if 'pubDate' in item:
                # Try to parse date
                try:
                    if isinstance(item['pubDate'], str):
                        pub_date = datetime.fromisoformat(item['pubDate'].replace('Z', '+00:00'))
                    else:
                        pub_date = datetime.now()
                    fe.pubDate(pub_date)
                except:
                    pass

            if 'category' in item:
                if isinstance(item['category'], list):
                    for cat in item['category']:
                        fe.category({'term': cat})
                else:
                    fe.category({'term': item['category']})

        except Exception as e:
            print(f"Warning: Error processing item {idx}: {e}")
            continue

    # Generate output files
    output_rss_filename = f"{args.name}.rss"
    output_atom_filename = f"{args.name}.atom"
    output_rss_path = os.path.join(args.output_dir, output_rss_filename)
    output_atom_path = os.path.join(args.output_dir, output_atom_filename)

    try:
        # Write RSS 2.0 feed
        fg.rss_file(output_rss_path, pretty=True)
        print(f"RSS 2.0 feed saved to: {output_rss_path}")
        print(f"  File size: {os.path.getsize(output_rss_path)} bytes")

        # Write Atom feed
        fg.atom_file(output_atom_path, pretty=True)
        print(f"Atom feed saved to: {output_atom_path}")
        print(f"  File size: {os.path.getsize(output_atom_path)} bytes")

        print(f"\nFeed Information:")
        print(f"  Title: {feed_config.get('title', args.title)}")
        print(f"  Link: {feed_config.get('link', args.link)}")
        print(f"  Total items: {len(items)}")

    except Exception as e:
        print(f"Error writing feed files: {e}")
        sys.exit(1)

    print("\nRSS feed generation completed successfully!")


if __name__ == "__main__":
    main()