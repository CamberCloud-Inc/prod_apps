import sys
import os
import argparse
import re
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Parse and format log files with filtering and analysis')
    parser.add_argument('input_file', help='Path to the input log file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for parsed log (default: ./)')
    parser.add_argument('-l', '--level', default='',
                        choices=['', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help='Filter by log level (default: all levels)')
    parser.add_argument('-p', '--pattern', default='',
                        help='Filter lines matching regex pattern (default: no filter)')
    parser.add_argument('-s', '--stats', action='store_true',
                        help='Generate statistics summary')

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

    # Common log patterns
    # Format: [LEVEL] timestamp message
    # Format: timestamp LEVEL message
    # Format: YYYY-MM-DD HH:MM:SS LEVEL message
    log_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}[\s_T]\d{2}:\d{2}:\d{2}[.,]?\d*)?'  # Optional timestamp
        r'.*?(ERROR|WARNING|WARN|INFO|DEBUG|CRITICAL|FATAL)?'  # Log level
        r'.*',  # Rest of message
        re.IGNORECASE
    )

    # Read the log file
    print(f"Reading log file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"Found {len(lines)} lines in log file")

    # Statistics tracking
    stats = {
        'ERROR': 0,
        'WARNING': 0,
        'INFO': 0,
        'DEBUG': 0,
        'OTHER': 0
    }
    timestamps = []

    # Parse and filter lines
    filtered_lines = []
    user_pattern = None

    if args.pattern:
        try:
            user_pattern = re.compile(args.pattern, re.IGNORECASE)
            print(f"Using filter pattern: {args.pattern}")
        except re.error as e:
            print(f"Error: Invalid regex pattern: {e}")
            sys.exit(1)

    if args.level:
        print(f"Filtering for log level: {args.level}")

    print("\nParsing log entries...")
    for line_num, line in enumerate(lines, 1):
        line = line.rstrip('\n\r')

        if not line.strip():
            continue

        # Try to extract log level
        match = log_pattern.match(line)
        detected_level = None

        if match and match.group(2):
            detected_level = match.group(2).upper()
            if detected_level == 'WARN':
                detected_level = 'WARNING'
            elif detected_level in ['CRITICAL', 'FATAL']:
                detected_level = 'ERROR'

        # Update statistics
        if detected_level and detected_level in stats:
            stats[detected_level] += 1
        else:
            stats['OTHER'] += 1

        # Extract timestamp if present
        if match and match.group(1):
            timestamps.append(match.group(1))

        # Apply level filter
        if args.level:
            if detected_level != args.level:
                continue

        # Apply pattern filter
        if user_pattern:
            if not user_pattern.search(line):
                continue

        # Add line to filtered results
        filtered_lines.append(line)

    print(f"Matched {len(filtered_lines)} lines after filtering")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]

    if args.level:
        output_filename = f"{name_without_ext}_parsed_{args.level.lower()}.log"
    else:
        output_filename = f"{name_without_ext}_parsed.log"

    output_path = os.path.join(args.output_dir, output_filename)

    # Write filtered log
    print(f"\nWriting parsed log to: {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if args.stats:
                # Write statistics header
                f.write("="*60 + "\n")
                f.write("LOG ANALYSIS SUMMARY\n")
                f.write("="*60 + "\n\n")
                f.write(f"Total lines processed: {len(lines)}\n")
                f.write(f"Lines matched: {len(filtered_lines)}\n\n")
                f.write("Log Level Distribution:\n")
                for level, count in sorted(stats.items()):
                    f.write(f"  {level:10s}: {count:6d}\n")

                if timestamps:
                    f.write(f"\nTimestamp range: {timestamps[0]} to {timestamps[-1]}\n")

                f.write("\n" + "="*60 + "\n\n")

            # Write filtered lines
            for line in filtered_lines:
                f.write(line + "\n")

        print(f"Successfully parsed log file")
        print(f"Output saved to: {output_path}")

        # Print statistics to console
        print("\nLog Statistics:")
        print(f"  Total lines: {len(lines)}")
        print(f"  Matched lines: {len(filtered_lines)}")
        print(f"  ERROR: {stats['ERROR']}")
        print(f"  WARNING: {stats['WARNING']}")
        print(f"  INFO: {stats['INFO']}")
        print(f"  DEBUG: {stats['DEBUG']}")
        print(f"  OTHER: {stats['OTHER']}")

    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("\nLog parsing completed!")


if __name__ == "__main__":
    main()