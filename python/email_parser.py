import email
from email import policy
from email.parser import BytesParser
import sys
import os
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Extract addresses, subjects, and metadata from .eml files')
    parser.add_argument('input_file', help='Path to the input .eml file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for extracted data (default: ./)')
    parser.add_argument('-f', '--format', default='json', choices=['json', 'txt'],
                        help='Output format: json or txt (default: json)')

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

    print(f"\nReading email file: {input_path}")

    # Parse the email file
    try:
        with open(input_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        print("Email parsing: PASSED")
    except Exception as e:
        print(f"Error parsing email file: {e}")
        sys.exit(1)

    # Extract email data
    email_data = {
        'subject': msg.get('Subject', 'No Subject'),
        'from': msg.get('From', 'Unknown'),
        'to': msg.get('To', 'Unknown'),
        'cc': msg.get('Cc', ''),
        'bcc': msg.get('Bcc', ''),
        'date': msg.get('Date', 'Unknown'),
        'message_id': msg.get('Message-ID', ''),
        'reply_to': msg.get('Reply-To', ''),
    }

    # Extract all email addresses from various headers
    all_addresses = []

    def extract_addresses(header_value):
        if header_value:
            # Simple email extraction - split by comma and extract addresses
            parts = str(header_value).split(',')
            for part in parts:
                # Look for email in angle brackets or standalone
                if '<' in part and '>' in part:
                    start = part.index('<') + 1
                    end = part.index('>')
                    all_addresses.append(part[start:end].strip())
                elif '@' in part:
                    all_addresses.append(part.strip())

    extract_addresses(email_data['from'])
    extract_addresses(email_data['to'])
    extract_addresses(email_data['cc'])
    extract_addresses(email_data['bcc'])
    extract_addresses(email_data['reply_to'])

    email_data['all_addresses'] = list(set(all_addresses))  # Remove duplicates

    # Get email body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                try:
                    body = part.get_content()
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_content()
        except:
            pass

    email_data['body_preview'] = body[:500] if body else "No text body found"
    email_data['body_length'] = len(body) if body else 0

    # Get attachments info
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        'filename': filename,
                        'content_type': part.get_content_type(),
                        'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                    })

    email_data['attachments'] = attachments
    email_data['attachment_count'] = len(attachments)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]

    print(f"\nExtracted Email Data:")
    print(f"  Subject: {email_data['subject']}")
    print(f"  From: {email_data['from']}")
    print(f"  To: {email_data['to']}")
    print(f"  Date: {email_data['date']}")
    print(f"  Total unique addresses found: {len(email_data['all_addresses'])}")
    print(f"  Attachments: {email_data['attachment_count']}")

    # Write output
    if args.format == 'json':
        output_filename = f"{base_name}_parsed.json"
        output_path = os.path.join(args.output_dir, output_filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(email_data, f, indent=2, ensure_ascii=False)
            print(f"\nJSON output saved to: {output_path}")
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            sys.exit(1)
    else:  # txt format
        output_filename = f"{base_name}_parsed.txt"
        output_path = os.path.join(args.output_dir, output_filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"EMAIL PARSE RESULTS\n")
                f.write(f"{'=' * 50}\n\n")
                f.write(f"Subject: {email_data['subject']}\n")
                f.write(f"From: {email_data['from']}\n")
                f.write(f"To: {email_data['to']}\n")
                f.write(f"Cc: {email_data['cc']}\n")
                f.write(f"Date: {email_data['date']}\n")
                f.write(f"Message-ID: {email_data['message_id']}\n\n")
                f.write(f"All Email Addresses Found:\n")
                for addr in email_data['all_addresses']:
                    f.write(f"  - {addr}\n")
                f.write(f"\nAttachments ({email_data['attachment_count']}):\n")
                for att in email_data['attachments']:
                    f.write(f"  - {att['filename']} ({att['content_type']}, {att['size']} bytes)\n")
                f.write(f"\nBody Preview:\n")
                f.write(email_data['body_preview'])
            print(f"\nText output saved to: {output_path}")
        except Exception as e:
            print(f"Error writing text file: {e}")
            sys.exit(1)

    print("\nEmail parsing completed successfully!")


if __name__ == "__main__":
    main()