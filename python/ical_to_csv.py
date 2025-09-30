import subprocess
import sys
import os
import argparse
import csv

# Install icalendar library
subprocess.check_call([sys.executable, "-m", "pip", "install", "icalendar", "--break-system-packages"])

from icalendar import Calendar
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Convert iCalendar (.ics) files to CSV format')
    parser.add_argument('input_file', help='Path to the input .ics calendar file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for CSV file (default: ./)')

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

    print(f"\nReading iCalendar file: {input_path}")

    # Parse the iCalendar file
    try:
        with open(input_path, 'rb') as f:
            cal = Calendar.from_ical(f.read())
        print("iCalendar parsing: PASSED")
    except Exception as e:
        print(f"Error parsing iCalendar file: {e}")
        sys.exit(1)

    # Extract events
    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event = {}

            # Extract basic fields
            event['summary'] = str(component.get('summary', ''))
            event['description'] = str(component.get('description', ''))
            event['location'] = str(component.get('location', ''))
            event['status'] = str(component.get('status', ''))
            event['organizer'] = str(component.get('organizer', ''))

            # Extract and format dates
            dtstart = component.get('dtstart')
            if dtstart:
                try:
                    dt_value = dtstart.dt
                    if isinstance(dt_value, datetime):
                        event['start_date'] = dt_value.strftime('%Y-%m-%d')
                        event['start_time'] = dt_value.strftime('%H:%M:%S')
                        event['start_datetime'] = dt_value.strftime('%Y-%m-%d %H:%M:%S')
                    else:  # date only
                        event['start_date'] = str(dt_value)
                        event['start_time'] = ''
                        event['start_datetime'] = str(dt_value)
                except:
                    event['start_date'] = str(dtstart)
                    event['start_time'] = ''
                    event['start_datetime'] = str(dtstart)
            else:
                event['start_date'] = ''
                event['start_time'] = ''
                event['start_datetime'] = ''

            dtend = component.get('dtend')
            if dtend:
                try:
                    dt_value = dtend.dt
                    if isinstance(dt_value, datetime):
                        event['end_date'] = dt_value.strftime('%Y-%m-%d')
                        event['end_time'] = dt_value.strftime('%H:%M:%S')
                        event['end_datetime'] = dt_value.strftime('%Y-%m-%d %H:%M:%S')
                    else:  # date only
                        event['end_date'] = str(dt_value)
                        event['end_time'] = ''
                        event['end_datetime'] = str(dt_value)
                except:
                    event['end_date'] = str(dtend)
                    event['end_time'] = ''
                    event['end_datetime'] = str(dtend)
            else:
                event['end_date'] = ''
                event['end_time'] = ''
                event['end_datetime'] = ''

            # Extract UID and created/modified times
            event['uid'] = str(component.get('uid', ''))

            created = component.get('created')
            if created:
                try:
                    event['created'] = created.dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    event['created'] = str(created)
            else:
                event['created'] = ''

            last_modified = component.get('last-modified')
            if last_modified:
                try:
                    event['last_modified'] = last_modified.dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    event['last_modified'] = str(last_modified)
            else:
                event['last_modified'] = ''

            # Extract categories
            categories = component.get('categories')
            if categories:
                if isinstance(categories, list):
                    event['categories'] = ', '.join(str(c) for c in categories)
                else:
                    event['categories'] = str(categories)
            else:
                event['categories'] = ''

            # Extract attendees
            attendees = []
            for attendee in component.get('attendee', []):
                attendees.append(str(attendee))
            event['attendees'] = '; '.join(attendees) if attendees else ''

            # Extract URL
            event['url'] = str(component.get('url', ''))

            events.append(event)

    if not events:
        print("Warning: No VEVENT components found in iCalendar file")
        # Try to still create a CSV with headers
        events = []

    print(f"Found {len(events)} calendar events")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.csv"
    output_path = os.path.join(args.output_dir, output_filename)

    # Define CSV columns
    fieldnames = [
        'summary', 'description', 'location', 'status',
        'start_date', 'start_time', 'start_datetime',
        'end_date', 'end_time', 'end_datetime',
        'organizer', 'attendees', 'categories',
        'url', 'uid', 'created', 'last_modified'
    ]

    # Write CSV
    print(f"\nConverting to CSV format...")
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(events)

        print(f"CSV file saved to: {output_path}")
        print(f"Converted {len(events)} events to CSV")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

        if events:
            print(f"\nSample event:")
            print(f"  Summary: {events[0].get('summary', 'N/A')}")
            print(f"  Start: {events[0].get('start_datetime', 'N/A')}")
            print(f"  Location: {events[0].get('location', 'N/A')}")

    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

    print("\niCalendar to CSV conversion completed successfully!")


if __name__ == "__main__":
    main()