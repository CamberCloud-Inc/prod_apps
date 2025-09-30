import subprocess
import sys
import os
import argparse
import csv

# Install vobject library
subprocess.check_call([sys.executable, "-m", "pip", "install", "vobject", "--break-system-packages"])

import vobject


def main():
    parser = argparse.ArgumentParser(description='Convert vCard (.vcf) contact files to CSV format')
    parser.add_argument('input_file', help='Path to the input .vcf vCard file')
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

    print(f"\nReading vCard file: {input_path}")

    # Parse the vCard file
    contacts = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            vcard_data = f.read()

        # Parse all vCards in the file
        for vcard in vobject.readComponents(vcard_data):
            if vcard.name == 'VCARD':
                contact = {}

                # Extract name
                if hasattr(vcard, 'fn'):
                    contact['full_name'] = str(vcard.fn.value)
                else:
                    contact['full_name'] = ''

                # Extract structured name (N property)
                if hasattr(vcard, 'n'):
                    n = vcard.n.value
                    contact['first_name'] = n.given if hasattr(n, 'given') else ''
                    contact['last_name'] = n.family if hasattr(n, 'family') else ''
                    contact['middle_name'] = n.additional if hasattr(n, 'additional') else ''
                    contact['prefix'] = n.prefix if hasattr(n, 'prefix') else ''
                    contact['suffix'] = n.suffix if hasattr(n, 'suffix') else ''
                else:
                    contact['first_name'] = ''
                    contact['last_name'] = ''
                    contact['middle_name'] = ''
                    contact['prefix'] = ''
                    contact['suffix'] = ''

                # Extract organization
                if hasattr(vcard, 'org'):
                    org = vcard.org.value
                    if isinstance(org, list):
                        contact['organization'] = ', '.join(str(o) for o in org)
                    else:
                        contact['organization'] = str(org)
                else:
                    contact['organization'] = ''

                # Extract title
                if hasattr(vcard, 'title'):
                    contact['title'] = str(vcard.title.value)
                else:
                    contact['title'] = ''

                # Extract email addresses
                emails = []
                if hasattr(vcard, 'email_list'):
                    for email in vcard.email_list:
                        email_type = ''
                        if hasattr(email, 'type_param'):
                            email_type = str(email.type_param) if email.type_param else ''
                        emails.append(f"{email.value} ({email_type})")
                contact['emails'] = '; '.join(emails) if emails else ''
                contact['primary_email'] = emails[0].split(' (')[0] if emails else ''

                # Extract phone numbers
                phones = []
                if hasattr(vcard, 'tel_list'):
                    for tel in vcard.tel_list:
                        phone_type = ''
                        if hasattr(tel, 'type_param'):
                            phone_type = str(tel.type_param) if tel.type_param else ''
                        phones.append(f"{tel.value} ({phone_type})")
                contact['phones'] = '; '.join(phones) if phones else ''
                contact['primary_phone'] = phones[0].split(' (')[0] if phones else ''

                # Extract addresses
                addresses = []
                if hasattr(vcard, 'adr_list'):
                    for adr in vcard.adr_list:
                        addr = adr.value
                        addr_parts = []
                        if hasattr(addr, 'street'):
                            addr_parts.append(str(addr.street))
                        if hasattr(addr, 'city'):
                            addr_parts.append(str(addr.city))
                        if hasattr(addr, 'region'):
                            addr_parts.append(str(addr.region))
                        if hasattr(addr, 'code'):
                            addr_parts.append(str(addr.code))
                        if hasattr(addr, 'country'):
                            addr_parts.append(str(addr.country))

                        addr_type = ''
                        if hasattr(adr, 'type_param'):
                            addr_type = str(adr.type_param) if adr.type_param else ''

                        full_addr = ', '.join(p for p in addr_parts if p)
                        if addr_type:
                            full_addr = f"{full_addr} ({addr_type})"
                        addresses.append(full_addr)

                contact['addresses'] = '; '.join(addresses) if addresses else ''

                # Extract URLs
                urls = []
                if hasattr(vcard, 'url_list'):
                    for url in vcard.url_list:
                        urls.append(str(url.value))
                contact['urls'] = '; '.join(urls) if urls else ''

                # Extract birthday
                if hasattr(vcard, 'bday'):
                    try:
                        contact['birthday'] = str(vcard.bday.value)
                    except:
                        contact['birthday'] = ''
                else:
                    contact['birthday'] = ''

                # Extract notes
                if hasattr(vcard, 'note'):
                    contact['note'] = str(vcard.note.value)
                else:
                    contact['note'] = ''

                # Extract UID
                if hasattr(vcard, 'uid'):
                    contact['uid'] = str(vcard.uid.value)
                else:
                    contact['uid'] = ''

                contacts.append(contact)

        print(f"vCard parsing: PASSED")
        print(f"Found {len(contacts)} contacts")

    except Exception as e:
        print(f"Error parsing vCard file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    if not contacts:
        print("Warning: No contacts found in vCard file")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.csv"
    output_path = os.path.join(args.output_dir, output_filename)

    # Define CSV columns
    fieldnames = [
        'full_name', 'first_name', 'last_name', 'middle_name', 'prefix', 'suffix',
        'organization', 'title',
        'primary_email', 'emails',
        'primary_phone', 'phones',
        'addresses', 'urls',
        'birthday', 'note', 'uid'
    ]

    # Write CSV
    print(f"\nConverting to CSV format...")
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)

        print(f"CSV file saved to: {output_path}")
        print(f"Converted {len(contacts)} contacts to CSV")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

        if contacts:
            print(f"\nSample contact:")
            print(f"  Name: {contacts[0].get('full_name', 'N/A')}")
            print(f"  Organization: {contacts[0].get('organization', 'N/A')}")
            print(f"  Email: {contacts[0].get('primary_email', 'N/A')}")
            print(f"  Phone: {contacts[0].get('primary_phone', 'N/A')}")

    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

    print("\nvCard to CSV conversion completed successfully!")


if __name__ == "__main__":
    main()