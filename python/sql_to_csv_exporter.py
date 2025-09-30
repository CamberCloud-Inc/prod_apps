import subprocess
import sys
import os
import argparse
import csv

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "sqlalchemy"])

import sqlalchemy
from sqlalchemy import create_engine, text


def main():
    parser = argparse.ArgumentParser(description='Export SQL query results to CSV')
    parser.add_argument('db_path', help='Path to the database file (SQLite)')
    parser.add_argument('-q', '--query', required=True,
                        help='SQL query to execute')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for CSV file (default: ./)')
    parser.add_argument('-n', '--output-name', default='query_results',
                        help='Base name for output CSV file (default: query_results)')

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

    try:
        # Create SQLAlchemy engine
        engine = create_engine(f'sqlite:///{db_path}')

        print(f"Executing query: {args.query}")

        # Execute query
        with engine.connect() as connection:
            result = connection.execute(text(args.query))
            rows = result.fetchall()
            columns = result.keys()

            if not rows:
                print("Warning: Query returned no rows")
                row_count = 0
            else:
                row_count = len(rows)

            print(f"Query executed successfully!")
            print(f"Found {row_count} rows")
            print(f"Found {len(columns)} columns: {', '.join(columns)}")

            # Generate output filename
            output_filename = f"{args.output_name}.csv"
            output_path = os.path.join(args.output_dir, output_filename)

            print(f"\nWriting results to CSV: {output_path}")

            # Write to CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)

                # Write header
                csv_writer.writerow(columns)

                # Write data rows
                for row in rows:
                    csv_writer.writerow(row)

            print(f"CSV file saved to: {output_path}")
            print(f"Exported {row_count} records to CSV")

    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    print("\nSQL to CSV export completed successfully!")


if __name__ == "__main__":
    main()