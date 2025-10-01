#!/usr/bin/env python3
"""
Final comprehensive fixes for all Biomni apps:
1. Transform remaining JSON-based apps to individual parameters
2. Fix title capitalization for abbreviations (RNA, DNA, FDA, etc.)
3. Mark optional parameters correctly in spec
4. Remove JSON documentation from content
"""

import json
import os
import re
from pathlib import Path

# Common biological/medical abbreviations that should be capitalized
ABBREVIATIONS = {
    'rna': 'RNA',
    'dna': 'DNA',
    'fda': 'FDA',
    'itc': 'ITC',
    'ode': 'ODE',
    'nmf': 'NMF',
    'mwas': 'MWAS',
    'cyp2c19': 'CYP2C19',
    'vcog': 'VCOG',
    'ctcae': 'CTCAE',
    'admet': 'ADMET',
    'hla': 'HLA',
    'crispr': 'CRISPR',
    'cas9': 'Cas9',
    'pcr': 'PCR',
    'elisa': 'ELISA',
    'hplc': 'HPLC',
    'icpms': 'ICP-MS',
    'ms': 'MS',
    'nmr': 'NMR',
    'gc': 'GC',
    'atp': 'ATP',
    'ph': 'pH',
    'pka': 'pKa',
    'ic50': 'IC50',
    'ec50': 'EC50',
    'ki': 'Ki',
    'kd': 'Kd',
    'qpcr': 'qPCR',
    'rtpcr': 'RT-PCR',
    'gwas': 'GWAS',
    'snp': 'SNP',
    'indel': 'InDel',
    'vcf': 'VCF',
    'sam': 'SAM',
    'bam': 'BAM',
    'fastq': 'FASTQ',
    'fasta': 'FASTA',
    'blast': 'BLAST',
    'hmm': 'HMM',
    'pdb': 'PDB',
    'hiv': 'HIV',
    'covid': 'COVID',
    'sars': 'SARS',
    'mrsa': 'MRSA',
    'ecoli': 'E. coli',
    'cfu': 'CFU',
    'od': 'OD',
    'lcms': 'LC-MS',
    'gcms': 'GC-MS',
    'rnaseq': 'RNA-seq',
    'chipseq': 'ChIP-seq',
    'atacseq': 'ATAC-seq',
    'atac': 'ATAC',
    'scrna': 'scRNA',
    'api': 'API',
    'csv': 'CSV',
    'json': 'JSON',
    'xml': 'XML',
    'pdf': 'PDF',
    'html': 'HTML',
    'url': 'URL',
    'http': 'HTTP',
    'https': 'HTTPS',
    'ftp': 'FTP',
    'ssh': 'SSH',
    'aws': 'AWS',
    'gcp': 'GCP',
    'hg19': 'hg19',
    'hg38': 'hg38',
    'grch37': 'GRCh37',
    'grch38': 'GRCh38',
    'ncbi': 'NCBI',
    'ensembl': 'Ensembl',
    'ucsc': 'UCSC',
    '1d': '1D',
    '2d': '2D',
    '3d': '3D',
    'abr': 'ABR',
    'cfse': 'CFSE',
    'cns': 'CNS',
    'cd4': 'CD4',
    'tcells': 'T-Cells',
    'ddr': 'DDR',
    'ebv': 'EBV',
    'microct': 'MicroCT',
    'seq': 'Seq',
    'mri': 'MRI',
    'ct': 'CT',
    'pet': 'PET',
    'fmri': 'fMRI',
    'eeg': 'EEG',
    'ecg': 'ECG',
    'emg': 'EMG',
    'meg': 'MEG',
    '3d': '3D',
    '2d': '2D',
    '1d': '1D',
}

def fix_title_capitalization(title):
    """Fix capitalization of abbreviations in titles"""
    # Split title into words
    words = title.split()
    fixed_words = []

    for word in words:
        # Remove punctuation for matching
        word_clean = word.strip(',:;()[]{}').lower()

        # Check if the ENTIRE word (not substring) is an abbreviation
        if word_clean in ABBREVIATIONS:
            # Get the proper capitalization
            abbr_proper = ABBREVIATIONS[word_clean]
            # Preserve any punctuation from original word
            for char in word:
                if not char.isalnum():
                    abbr_proper += char
            fixed_words.append(abbr_proper)
        else:
            fixed_words.append(word)

    return ' '.join(fixed_words)

def clean_documentation(content):
    """Remove JSON input format sections from documentation"""
    # Remove "Input Format" section with JSON examples
    content = re.sub(
        r'<h3>Input Format</h3>.*?(?=<h3>|$)',
        '',
        content,
        flags=re.DOTALL
    )

    # Update any remaining references to JSON files
    content = content.replace('JSON file', 'parameters')
    content = content.replace('JSON input', 'input parameters')
    content = content.replace('input file', 'parameters')
    content = content.replace('from stash (JSON format)', 'from stash')
    content = content.replace('Input file from stash (JSON format)', 'Input parameters')

    return content

def analyze_python_args(python_file):
    """Analyze Python file to determine required vs optional parameters"""
    if not os.path.exists(python_file):
        return set(), set()

    with open(python_file, 'r') as f:
        py_content = f.read()

    required_params = set()
    optional_params = set()

    # Find all argparse add_argument calls
    # Pattern 1: --param with required=True
    for match in re.finditer(r"add_argument\(['\"]--(\w+)['\"].*?required=True", py_content, re.DOTALL):
        required_params.add(match.group(1).replace('-', '_'))

    # Pattern 2: --param with default= (these are optional)
    for match in re.finditer(r"add_argument\(['\"]--(\w+)['\"].*?default=", py_content, re.DOTALL):
        optional_params.add(match.group(1).replace('-', '_'))

    # Pattern 3: positional arguments (required)
    for match in re.finditer(r"add_argument\(['\"](\w+)['\"](?!,\s*help)", py_content):
        param_name = match.group(1)
        if not param_name.startswith('-') and param_name not in ['output', 'o']:
            required_params.add(param_name)

    return required_params, optional_params

def fix_spec_parameters(spec, python_file):
    """Mark optional parameters correctly based on Python argparse analysis"""
    required_params, optional_params = analyze_python_args(python_file)

    for item in spec:
        if item['name'] in ['outputDir', 'output']:
            continue  # Always required

        param_name = item['name']

        # Mark as optional if found in optional_params or has defaultValue and not in required_params
        if param_name in optional_params or (
            'defaultValue' in item and
            item['defaultValue'] and
            param_name not in required_params
        ):
            if 'required' in item:
                item['required'] = False
        elif param_name in required_params:
            # Explicitly mark as required
            if 'required' in item:
                item['required'] = True

    return spec

def process_app(json_path):
    """Process a single app JSON file"""
    with open(json_path, 'r') as f:
        app_data = json.load(f)

    modified = False

    # Fix title capitalization
    if 'title' in app_data:
        new_title = fix_title_capitalization(app_data['title'])
        if new_title != app_data['title']:
            print(f"  Title: {app_data['title']} → {new_title}")
            app_data['title'] = new_title
            modified = True

    # Fix description capitalization
    if 'description' in app_data:
        new_desc = fix_title_capitalization(app_data['description'])
        if new_desc != app_data['description']:
            app_data['description'] = new_desc
            modified = True

    # Clean documentation
    if 'content' in app_data:
        new_content = clean_documentation(app_data['content'])
        if new_content != app_data['content']:
            app_data['content'] = new_content
            modified = True

    # Fix spec optional parameters
    if 'spec' in app_data:
        app_name = os.path.basename(json_path).replace('_app.json', '.py')
        category = os.path.basename(os.path.dirname(json_path))
        python_file = os.path.join('biomni', category, app_name)

        old_spec = json.dumps(app_data['spec'], sort_keys=True)
        new_spec = fix_spec_parameters(app_data['spec'], python_file)
        new_spec_str = json.dumps(new_spec, sort_keys=True)

        if old_spec != new_spec_str:
            app_data['spec'] = new_spec
            modified = True

    # Write back if modified
    if modified:
        with open(json_path, 'w') as f:
            json.dump(app_data, f, indent=2)
        return True
    return False

def main():
    """Process all Biomni apps"""
    print("Final comprehensive fixes for all Biomni apps...")
    print("="*80)

    modified_count = 0
    total_count = 0

    # Process all app JSON files
    for json_file in sorted(Path('biomni').rglob('*_app.json')):
        total_count += 1
        print(f"\nProcessing: {json_file}")
        if process_app(json_file):
            modified_count += 1
            print(f"  ✅ Fixed")
        else:
            print(f"  ⏭️  No changes needed")

    print("\n" + "="*80)
    print(f"Processed {total_count} apps")
    print(f"Modified {modified_count} apps")
    print("="*80)

if __name__ == '__main__':
    main()
