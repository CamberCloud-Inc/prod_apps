import subprocess
import sys
import os
import argparse
import json
import csv
import sqlite3


def main():
    parser = argparse.ArgumentParser(description='Export database tables to JSON or CSV')
    parser.add_argument('db_path', help='Path to the database file (SQLite)')
    parser.add_argument('-t', '--table', required=True,
                        help='Table name to export')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json',
                        help='Output format: json or csv (default: json)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for output file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received db_path argument: {args.db_path}")

    # Expand user path if provided
    db_path = os.path.expanduser(args.db_path)
    print(f"Expanded db_path: {db_path}")

    if not os.path.exists(db_path):
        print(f"Error: Database file not found at: {db_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nConnecting to database: {db_path}")
    print(f"Exporting table: {args.table}")
    print(f"Output format: {args.format}")

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (args.table,))
        if not cursor.fetchone():
            print(f"Error: Table '{args.table}' not found in database")

            # List available tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            if tables:
                print(f"\nAvailable tables:")
                for table in tables:
                    print(f"  - {table[0]}")

            conn.close()
            sys.exit(1)

        # Query all data from the table
        cursor.execute(f"SELECT * FROM {args.table}")
        rows = cursor.fetchall()

        if not rows:
            print(f"Warning: Table '{args.table}' is empty")
            row_count = 0
            columns = []
        else:
            row_count = len(rows)
            columns = rows[0].keys()

        print(f"\nTable information:")
        print(f"  Rows: {row_count}")
        print(f"  Columns: {len(columns)}")
        if columns:
            print(f"  Column names: {', '.join(columns)}")

        # Convert rows to dictionaries
        data = []
        for row in rows:
            data.append(dict(row))

        # Generate output filename
        output_filename = f"{args.table}.{args.format}"
        output_path = os.path.join(args.output_dir, output_filename)

        print(f"\nWriting data to: {output_path}")

        # Write output based on format
        if args.format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"JSON file saved: {output_path}")

        elif args.format == 'csv':
            if data:
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=columns)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"CSV file saved: {output_path}")
            else:
                # Write empty CSV with just headers if no data
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    if columns:
                        writer = csv.DictWriter(f, fieldnames=columns)
                        writer.writeheader()
                print(f"Empty CSV file saved: {output_path}")

        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    print(f"\nDatabase table dump completed successfully!")
    print(f"Exported {row_count} records from table '{args.table}'")


if __name__ == "__main__":
    main()