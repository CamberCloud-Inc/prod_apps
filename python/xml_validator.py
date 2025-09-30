import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "lxml"])

from lxml import etree


def main():
    parser = argparse.ArgumentParser(description='Validate XML against XSD schema')
    parser.add_argument('xml_path', help='Path to the XML file')
    parser.add_argument('-s', '--schema', required=False,
                        help='Path to XSD schema file (optional)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for validation report (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received xml_path argument: {args.xml_path}")

    # Expand user path if provided
    xml_path = os.path.expanduser(args.xml_path)
    print(f"Expanded xml_path: {xml_path}")

    if not os.path.exists(xml_path):
        print(f"Error: XML file not found at: {xml_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read and parse XML file
    print(f"\nReading XML file: {xml_path}")

    validation_results = []

    # Basic well-formedness check
    try:
        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()

        doc = etree.fromstring(xml_content.encode('utf-8'))
        validation_results.append("✓ XML is well-formed")
        print("✓ XML is well-formed")

    except etree.XMLSyntaxError as e:
        validation_results.append(f"✗ XML syntax error: {str(e)}")
        print(f"✗ XML syntax error: {str(e)}")

        # Write validation report
        base_name = os.path.splitext(os.path.basename(xml_path))[0]
        output_path = os.path.join(args.output_dir, f"{base_name}_validation_report.txt")

        with open(output_path, 'w', encoding='utf-8') as report:
            report.write("XML Validation Report\n")
            report.write("=" * 50 + "\n\n")
            report.write(f"File: {xml_path}\n\n")
            report.write("Results:\n")
            for result in validation_results:
                report.write(f"{result}\n")

        print(f"\nValidation report saved to: {output_path}")
        print("XML validation FAILED!")
        sys.exit(1)

    except Exception as e:
        validation_results.append(f"✗ Error reading XML: {str(e)}")
        print(f"✗ Error reading XML: {str(e)}")
        sys.exit(1)

    # Schema validation if schema provided
    if args.schema:
        schema_path = os.path.expanduser(args.schema)
        print(f"\nValidating against schema: {schema_path}")

        if not os.path.exists(schema_path):
            validation_results.append(f"✗ Schema file not found at: {schema_path}")
            print(f"✗ Schema file not found at: {schema_path}")
        else:
            try:
                with open(schema_path, 'r', encoding='utf-8') as schema_file:
                    schema_content = schema_file.read()

                schema_doc = etree.fromstring(schema_content.encode('utf-8'))
                schema = etree.XMLSchema(schema_doc)

                if schema.validate(doc):
                    validation_results.append("✓ XML is valid against the schema")
                    print("✓ XML is valid against the schema")
                else:
                    validation_results.append("✗ XML validation against schema failed:")
                    print("✗ XML validation against schema failed:")
                    for error in schema.error_log:
                        error_msg = f"  Line {error.line}: {error.message}"
                        validation_results.append(error_msg)
                        print(error_msg)

            except etree.XMLSchemaParseError as e:
                validation_results.append(f"✗ Schema parsing error: {str(e)}")
                print(f"✗ Schema parsing error: {str(e)}")
            except Exception as e:
                validation_results.append(f"✗ Schema validation error: {str(e)}")
                print(f"✗ Schema validation error: {str(e)}")
    else:
        validation_results.append("Note: No schema provided, only well-formedness checked")
        print("\nNote: No schema provided, only well-formedness checked")

    # Write validation report
    base_name = os.path.splitext(os.path.basename(xml_path))[0]
    output_path = os.path.join(args.output_dir, f"{base_name}_validation_report.txt")

    with open(output_path, 'w', encoding='utf-8') as report:
        report.write("XML Validation Report\n")
        report.write("=" * 50 + "\n\n")
        report.write(f"File: {xml_path}\n")
        if args.schema:
            report.write(f"Schema: {args.schema}\n")
        report.write("\nResults:\n")
        for result in validation_results:
            report.write(f"{result}\n")

    print(f"\nValidation report saved to: {output_path}")
    print("XML validation completed successfully!")


if __name__ == "__main__":
    main()