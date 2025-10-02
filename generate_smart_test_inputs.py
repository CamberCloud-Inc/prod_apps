#!/usr/bin/env python3
"""
Generate smart test inputs for Biomni apps based on parameter descriptions
"""

import json
import re
from pathlib import Path

def get_smart_test_value(param_name, param_type, description, label):
    """Generate realistic test data based on parameter name/description"""

    # Convert to lowercase for matching
    name_lower = param_name.lower()
    desc_lower = (description or '').lower()
    label_lower = (label or '').lower()
    combined = f"{name_lower} {desc_lower} {label_lower}"

    # DNA/RNA Sequences
    if any(word in combined for word in ['sequence', 'dna', 'rna', 'primer', 'oligo']):
        if 'long' in combined or 'target' in combined or 'template' in combined:
            # Long target sequence (100bp)
            return 'ATGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG'
        elif 'short' in combined or 'primer' in combined:
            # Short primer sequence (20bp)
            return 'ATGCGATCGATCGATCGATC'
        else:
            # Default sequence (50bp)
            return 'ATGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG'

    # Protein Sequences
    if 'protein' in combined and 'sequence' in combined:
        return 'MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH'

    # File paths based on type
    if 'file' in combined or 'path' in combined:
        if 'json' in combined:
            return 'test_data.json'
        elif 'csv' in combined:
            return 'test_data.csv'
        elif 'txt' in combined or 'text' in combined:
            return 'test_data.txt'
        elif 'npy' in combined or 'numpy' in combined:
            return 'test_data.npy'
        elif 'image' in combined or 'img' in combined:
            return 'test_image.png'
        elif 'pdb' in combined:
            return 'test_structure.pdb'
        else:
            return 'test_file.txt'

    # Query/Search strings
    if any(word in combined for word in ['query', 'search', 'term', 'keyword']):
        if 'gene' in combined:
            return 'BRCA1'
        elif 'disease' in combined:
            return 'breast cancer'
        elif 'drug' in combined or 'compound' in combined:
            return 'aspirin'
        elif 'protein' in combined:
            return 'p53'
        else:
            return 'cancer immunotherapy'

    # IDs and Identifiers
    if any(word in combined for word in ['id', 'identifier', 'accession']):
        if 'gene' in combined:
            return 'ENSG00000141510'  # EGFR
        elif 'protein' in combined or 'uniprot' in combined:
            return 'P04637'  # TP53
        elif 'pdb' in combined:
            return '1TUP'
        elif 'pubmed' in combined or 'pmid' in combined:
            return '12345678'
        elif 'doi' in combined:
            return '10.1038/nature12345'
        else:
            return 'TEST_ID_12345'

    # URLs
    if 'url' in combined or 'link' in combined:
        return 'https://www.ncbi.nlm.nih.gov/pubmed/12345678'

    # Numeric values
    if any(word in combined for word in ['number', 'count', 'max', 'min', 'limit', 'size', 'threshold']):
        if 'max' in combined or 'limit' in combined:
            return '10'
        elif 'threshold' in combined:
            return '0.05'
        else:
            return '5'

    # Boolean/Yes-No
    if any(word in combined for word in ['enable', 'disable', 'flag', 'boolean']):
        return 'true'

    # Percentages
    if 'percent' in combined or '%' in combined:
        return '0.05'

    # Concentrations
    if 'concentration' in combined or 'molarity' in combined:
        return '1.0'

    # Temperature
    if 'temperature' in combined or 'temp' in combined:
        return '37'

    # pH
    if 'ph' in combined:
        return '7.4'

    # Time values
    if 'time' in combined or 'duration' in combined:
        if 'ms' in combined or 'millisecond' in combined:
            return '100'
        elif 'hour' in combined:
            return '24'
        elif 'minute' in combined:
            return '60'
        else:
            return '10'

    # Organism/Species
    if 'organism' in combined or 'species' in combined:
        return 'homo sapiens'

    # Email
    if 'email' in combined:
        return 'test@example.com'

    # SMILES (chemical notation)
    if 'smiles' in combined:
        return 'CC(=O)OC1=CC=CC=C1C(=O)O'  # Aspirin

    # Coordinates
    if 'coordinate' in combined or 'position' in combined:
        if 'chr' in combined or 'chromosome' in combined:
            return 'chr1:12345-67890'
        else:
            return '100'

    # Default fallbacks
    if param_type == 'Checkbox':
        return 'false'
    elif param_type == 'Select':
        return None  # Will be handled by options
    elif param_type == 'Stash File':
        return 'test_file.txt'
    else:
        return 'test_value'

def generate_test_inputs_for_app(app_json_path):
    """Generate smart test inputs for a specific app"""
    with open(app_json_path, 'r') as f:
        app_data = json.load(f)

    inputs = {}
    spec = app_data.get('spec', [])

    for item in spec:
        param_name = item['name']
        param_type = item['type']
        default_value = item.get('defaultValue', '')
        description = item.get('description', '')
        label = item.get('label', '')

        # Skip outputDir
        if param_name in ['outputDir', 'output']:
            continue

        # Use default values if available
        if default_value:
            inputs[param_name] = default_value
        elif param_type == 'Select':
            options = item.get('options', [])
            if options:
                inputs[param_name] = options[0].get('value', '')
        else:
            smart_value = get_smart_test_value(param_name, param_type, description, label)
            if smart_value:
                inputs[param_name] = smart_value

    return inputs

def main():
    """Generate test inputs for all biomni apps"""
    output = {}

    for json_file in sorted(Path('biomni').rglob('*_app.json')):
        app_name = json_file.stem.replace('_app', '')
        full_app_name = f"biomni-{app_name.replace('_', '-')}"

        try:
            inputs = generate_test_inputs_for_app(str(json_file))
            output[full_app_name] = {
                'json_path': str(json_file),
                'inputs': inputs
            }
            print(f"✓ {full_app_name}: {len(inputs)} parameters")
        except Exception as e:
            print(f"✗ {full_app_name}: {e}")

    # Save to file
    with open('biomni_smart_test_inputs.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Generated test inputs for {len(output)} apps")
    print("📝 Saved to: biomni_smart_test_inputs.json")

if __name__ == '__main__':
    main()
