#!/usr/bin/env python3
"""
Script to add samplesheet format examples to Nextflow app descriptions.
Processes 73 apps, extracts samplesheet formats from HTML content, and updates descriptions.
"""

import json
import re
import os
from pathlib import Path
from html import unescape

# All 73 apps to process
APPS = [
    "hicar/enhancer-promoter-loops",
    "liverctanalysis/ct-analysis",
    "deepvariant/clinical-wgs",
    "longraredisease/diagnostic-wgs",
    "scflow/cell-type-annotation",
    "methylarray/clinical-ewas",
    "viralmetagenome/viral-discovery",
    "ddamsproteomics/tmt-labeling",
    "phaseimpute/genotype-imputation",
    "tfactivity/tf-regulon-analysis",
    "epitopeprediction/vaccine-design",
    "imcyto/imaging-mass-cytometry",
    "cellpainting/phenotypic-profiling",
    "molkart/spatial-multiomics",
    "pixelator/spatial-proteomics",
    "diaproteomics/dia-discovery",
    "hgtseq/horizontal-gene-transfer",
    "rnadnavar/rna-editing-analysis",
    "pathogensurveillance/clinical-surveillance",
    "variantbenchmarking/benchmark-analysis",
    "alleleexpression/ase-analysis",
    "tumourevo/tumor-phylogeny",
    "drop/rna-outliers",
    "lncpipe/lncrna-discovery",
    "reportho/orthology-analysis",
    "callingcards/tf-binding",
    "drugresponseeval/drug-screening",
    "evexplorer/molecular-evolution",
    "diseasemodulediscovery/disease-networks",
    "variantcatalogue/population-variants",
    "viralintegration/hpv-integration",
    "multiplesequencealign/protein-msa",
    "pairgenomealign/synteny-analysis",
    "denovotranscript/de-novo-transcriptome",
    "denovohybrid/hybrid-assembly",
    "ssds/single-strand-dna",
    "tbanalyzer/tb-genomics",
    "sammyseq/sammy-analysis",
    "readsimulator/ngs-simulation",
    "seqinspector/sequencing-qc",
    "rarevariantburden/rare-disease-burden",
    "coproid/ancient-dna",
    "metapep/metaproteomics",
    "mitodetect/mitochondrial-variants",
    "proteinannotator/protein-annotation",
    "proteinfamilies/protein-families",
    "genomeannotator/eukaryote-annotation",
    "genomeassembler/short-read-assembly",
    "genomeqc/genome-qc",
    "genomeskim/organelle-genomes",
    "omicsgenetraitassociation/multi-omics-gwas",
    "bamtofastq/bam-conversion",
    "fastqrepair/fastq-repair",
    "fastquorum/quality-filtering",
    "createpanelrefs/reference-panels",
    "createtaxdb/taxonomy-db",
    "references/reference-management",
    "datasync/data-sync",
    "deepmodeloptim/ml-optimization",
    "abotyper/blood-antigens",
    "stableexpression/housekeeping-genes",
    "ribomsqc/ribo-profiling-qc",
    "lsmquant/label-free-ms",
    "panoramaseq/panorama-analysis",
    "radseq/rad-seq",
    "troughgraph/tumor-heterogeneity",
    "spinningjenny/spatial-transcriptomics",
    "mhcquant/immunopeptidomics",
    "methylong/long-read-methylation",
    "marsseq/mars-seq",
    "demo/demo-pipeline",
    "neutronstar/neutron-star-analysis",
    "rangeland/remote-sensing",
]

BASE_PATH = "/Users/david/git/prod_apps/nextflow"


def has_samplesheet_info(description):
    """Check if description already contains samplesheet format info"""
    if not description:
        return False
    patterns = [
        r'samplesheet format:',
        r'sample sheet format:',
        r'samplesheet columns:',
        r'sample sheet columns:',
        r'input format:.*sample',
    ]
    desc_lower = description.lower()
    return any(re.search(pattern, desc_lower) for pattern in patterns)


def extract_samplesheet_format(content):
    """Extract samplesheet format from HTML content"""
    if not content:
        return None

    # Unescape HTML entities
    content = unescape(content)

    # Pattern 1: Look for CSV-like content in code blocks with sample/fastq patterns
    # Match: <code>sample,fastq_1,fastq_2...
    pattern1 = r'<code>([a-zA-Z_][a-zA-Z0-9_]*(?:,[a-zA-Z0-9_]+)+)'
    matches1 = re.findall(pattern1, content, re.IGNORECASE)
    for match in matches1:
        # Check if it looks like a samplesheet header (contains common keywords)
        if any(keyword in match.lower() for keyword in ['sample', 'fastq', 'bam', 'id', 'group', 'condition']):
            # Take only the first line (header)
            first_line = match.split('\\n')[0].split('\n')[0]
            if ',' in first_line and len(first_line.split(',')) >= 2:
                return first_line.strip()

    # Pattern 2: Look for pre/code blocks with CSV content
    pattern2 = r'<pre[^>]*><code>(.*?)</code></pre>'
    matches2 = re.findall(pattern2, content, re.DOTALL | re.IGNORECASE)
    for match in matches2:
        lines = match.split('\\n')
        if not lines:
            lines = match.split('\n')

        for line in lines[:3]:  # Check first 3 lines
            line = line.strip()
            if ',' in line and any(keyword in line.lower() for keyword in ['sample', 'fastq', 'bam', 'id', 'group', 'condition', 'sentrix']):
                # This looks like a header
                parts = line.split(',')
                if len(parts) >= 2:
                    return line

    # Pattern 3: Look for bullet lists or descriptions mentioning samplesheet columns
    pattern3 = r'(?:sample.*?sheet|input.*?csv).*?(?:columns?|format|requires?).*?:?\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z0-9_]+)+)'
    matches3 = re.findall(pattern3, content, re.IGNORECASE | re.DOTALL)
    for match in matches3:
        # Clean up and verify it's a reasonable column list
        clean_match = match.strip()
        if clean_match.count(',') >= 1 and clean_match.count(',') <= 10:
            # Remove extra whitespace
            clean_match = ','.join([c.strip() for c in clean_match.split(',')])
            return clean_match

    # Pattern 4: Look for table headers in HTML
    pattern4 = r'<th[^>]*>([a-zA-Z_][a-zA-Z0-9_]*)</th>'
    headers = re.findall(pattern4, content, re.IGNORECASE)
    if len(headers) >= 2 and len(headers) <= 10:
        # Check if headers look like samplesheet columns
        if any(h.lower() in ['sample', 'fastq', 'bam', 'id', 'group', 'condition'] for h in headers):
            return ','.join(headers)

    # Pattern 5: Look for CSV content in description text
    pattern5 = r'CSV.*?(?:with|containing|includes?).*?(?:columns?)?.*?:?\s*`([a-zA-Z_][a-zA-Z0-9_,\s]+)`'
    matches5 = re.findall(pattern5, content, re.IGNORECASE)
    for match in matches5:
        clean_match = ','.join([c.strip() for c in match.split(',')])
        if clean_match.count(',') >= 1 and clean_match.count(',') <= 10:
            return clean_match

    return None


def process_app(app_path_rel):
    """Process a single app"""
    app_path = os.path.join(BASE_PATH, app_path_rel)
    app_json_path = os.path.join(app_path, "app.json")

    if not os.path.exists(app_json_path):
        return {
            "status": "missing",
            "reason": "app.json not found",
            "path": app_json_path
        }

    try:
        with open(app_json_path, 'r', encoding='utf-8') as f:
            app_data = json.load(f)

        description = app_data.get('description', '')
        content = app_data.get('content', '')
        app_name = app_data.get('name', app_path_rel)

        # Check if already has samplesheet info
        if has_samplesheet_info(description):
            return {
                "status": "skipped",
                "reason": "already has samplesheet info",
                "app_name": app_name
            }

        # Try to extract samplesheet format from content
        samplesheet_format = extract_samplesheet_format(content)

        if not samplesheet_format:
            return {
                "status": "skipped",
                "reason": "no samplesheet found in content",
                "app_name": app_name
            }

        # Add to description (with space before if description doesn't end with punctuation)
        if description and not description[-1] in '.!?':
            new_description = f"{description}. Samplesheet format: `{samplesheet_format}`"
        else:
            new_description = f"{description} Samplesheet format: `{samplesheet_format}`"

        app_data['description'] = new_description

        # Write back
        with open(app_json_path, 'w', encoding='utf-8') as f:
            json.dump(app_data, f, indent=2, ensure_ascii=False)

        return {
            "status": "modified",
            "format": samplesheet_format,
            "app_name": app_name,
            "app_json_path": app_json_path,
            "app_path_rel": app_path_rel
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "app_name": app_path_rel
        }


def main():
    """Main processing function"""
    print("=" * 80)
    print("Processing 73 Nextflow Apps - Adding Samplesheet Formats")
    print("=" * 80)
    print()

    results = {}

    for i, app in enumerate(APPS, 1):
        print(f"[{i}/73] Processing {app}...", end=" ")
        result = process_app(app)
        results[app] = result
        print(f"{result['status'].upper()}")

    # Print detailed summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    modified = {k: v for k, v in results.items() if v["status"] == "modified"}
    skipped = {k: v for k, v in results.items() if v["status"] == "skipped"}
    errors = {k: v for k, v in results.items() if v["status"] == "error"}
    missing = {k: v for k, v in results.items() if v["status"] == "missing"}

    print(f"\nMODIFIED: {len(modified)} apps")
    if modified:
        for app, info in modified.items():
            print(f"  ✓ {app}")
            print(f"    App name: {info['app_name']}")
            print(f"    Format: {info['format']}")

    print(f"\nSKIPPED: {len(skipped)} apps")
    for app, info in skipped.items():
        print(f"  - {app}: {info['reason']}")

    if errors:
        print(f"\nERRORS: {len(errors)} apps")
        for app, info in errors.items():
            print(f"  ✗ {app}: {info['reason']}")

    if missing:
        print(f"\nMISSING: {len(missing)} apps")
        for app, info in missing.items():
            print(f"  ? {app}: {info['reason']}")
            print(f"    Expected at: {info['path']}")

    # Save results for deployment
    results_file = os.path.join(BASE_PATH, 'samplesheet_update_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n\nResults saved to: {results_file}")

    # Save deployment script
    if modified:
        deploy_script = os.path.join(BASE_PATH, 'deploy_modified_apps.sh')
        with open(deploy_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Auto-generated deployment script\n")
            f.write("# Run this to deploy all modified apps\n\n")
            f.write("set -e\n\n")

            for app, info in modified.items():
                app_name = info['app_name']
                app_json = info['app_json_path']
                f.write(f"echo 'Deploying {app_name}...'\n")
                f.write(f"camber app delete {app_name} || true\n")
                f.write(f"camber app create --file {app_json}\n")
                f.write(f"echo 'Done: {app_name}'\n\n")

        os.chmod(deploy_script, 0o755)
        print(f"Deployment script saved to: {deploy_script}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
