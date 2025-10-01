#!/usr/bin/env python3
"""
Fix all 73 Nextflow apps:
1. Remove "nf-core/" and other prefixes from titles
2. Add samplesheet examples to descriptions where applicable
"""

import json
import os
import re
from pathlib import Path

# List of all 73 apps to fix (relative to nextflow directory)
APPS_TO_FIX = [
    "abotyper/blood-antigens",
    "alleleexpression/ase-analysis",
    "bamtofastq/bam-conversion",
    "callingcards/tf-binding",
    "cellpainting/phenotypic-profiling",
    "coproid/ancient-dna",
    "createpanelrefs/reference-panels",
    "createtaxdb/taxonomy-db",
    "datasync/data-sync",
    "ddamsproteomics/tmt-labeling",
    "deepmodeloptim/ml-optimization",
    "deepvariant/clinical-wgs",
    "demo/demo-pipeline",
    "denovohybrid/hybrid-assembly",
    "denovotranscript/de-novo-transcriptome",
    "diaproteomics/dia-discovery",
    "diseasemodulediscovery/disease-networks",
    "drop/rna-outliers",
    "drugresponseeval/drug-screening",
    "epitopeprediction/vaccine-design",
    "evexplorer/molecular-evolution",
    "fastqrepair/fastq-repair",
    "fastquorum/quality-filtering",
    "genomeannotator/eukaryote-annotation",
    "genomeassembler/short-read-assembly",
    "genomeqc/genome-qc",
    "genomeskim/organelle-genomes",
    "hgtseq/horizontal-gene-transfer",
    "hicar/enhancer-promoter-loops",
    "imcyto/imaging-mass-cytometry",
    "liverctanalysis/ct-analysis",
    "lncpipe/lncrna-discovery",
    "longraredisease/diagnostic-wgs",
    "lsmquant/label-free-ms",
    "marsseq/mars-seq",
    "metapep/metaproteomics",
    "methylarray/clinical-ewas",
    "methylong/long-read-methylation",
    "mhcquant/immunopeptidomics",
    "mitodetect/mitochondrial-variants",
    "molkart/spatial-multiomics",
    "multiplesequencealign/protein-msa",
    "neutronstar/neutron-star-analysis",
    "omicsgenetraitassociation/multi-omics-gwas",
    "pairgenomealign/synteny-analysis",
    "panoramaseq/panorama-analysis",
    "pathogensurveillance/clinical-surveillance",
    "phaseimpute/genotype-imputation",
    "pixelator/spatial-proteomics",
    "proteinannotator/protein-annotation",
    "proteinfamilies/protein-families",
    "radseq/rad-seq",
    "rangeland/remote-sensing",
    "rarevariantburden/rare-disease-burden",
    "readsimulator/ngs-simulation",
    "references/reference-management",
    "reportho/orthology-analysis",
    "ribomsqc/ribo-profiling-qc",
    "rnadnavar/rna-editing-analysis",
    "sammyseq/sammy-analysis",
    "scflow/cell-type-annotation",
    "seqinspector/sequencing-qc",
    "spinningjenny/spatial-transcriptomics",
    "ssds/single-strand-dna",
    "stableexpression/housekeeping-genes",
    "tbanalyzer/tb-genomics",
    "tfactivity/tf-regulon-analysis",
    "troughgraph/tumor-heterogeneity",
    "tumourevo/tumor-phylogeny",
    "variantbenchmarking/benchmark-analysis",
    "variantcatalogue/population-variants",
    "viralintegration/hpv-integration",
    "viralmetagenome/viral-discovery",
]


def clean_title(title):
    """Remove prefixes like 'nf-core/', colons, and other redundant text from titles."""
    # Remove "nf-core/" prefix
    title = re.sub(r'^nf-core/', '', title, flags=re.IGNORECASE)

    # Remove other common prefixes followed by colon
    # Examples: "HiCAR:", "scFlow:", "Long-read Rare Disease:"
    title = re.sub(r'^[^:]+:\s*', '', title)

    # Clean up any remaining artifacts
    title = title.strip()

    return title


def extract_samplesheet_format(content, spec):
    """Extract samplesheet format from content and spec fields."""
    if not content:
        return None

    # Check if app requires samplesheet input
    has_samplesheet_input = False
    for field in spec:
        if field.get('name') in ['input', 'samplesheet'] and field.get('type') == 'Stash File':
            restrictions = field.get('restrictions', {})
            allowed_types = restrictions.get('allowed_file_types', [])
            if '.csv' in allowed_types or '.tsv' in allowed_types:
                has_samplesheet_input = True
                break

    if not has_samplesheet_input:
        return None

    # Look for samplesheet format in content
    # Common patterns:
    # - "sample,fastq_1,fastq_2"
    # - "Sample_Name,Sentrix_ID,Sentrix_Position"
    # - CSV format examples in <pre> or <code> tags

    # Pattern 1: Look for explicit format mentions
    format_match = re.search(r'(?:format|columns):\s*`([^`]+)`', content, re.IGNORECASE)
    if format_match:
        return format_match.group(1)

    # Pattern 2: Look for CSV examples in code blocks
    code_blocks = re.findall(r'<code>([^<]+)</code>', content, re.DOTALL)
    for code in code_blocks:
        # Check if it looks like a CSV header
        if ',' in code and '\n' in code:
            lines = code.strip().split('\n')
            if lines and ',' in lines[0] and not lines[0].startswith(' '):
                return lines[0].strip()

    # Pattern 3: Look in <pre> blocks
    pre_blocks = re.findall(r'<pre[^>]*>.*?<code>([^<]+)</code>.*?</pre>', content, re.DOTALL)
    for pre in pre_blocks:
        lines = pre.strip().split('\n')
        if lines and ',' in lines[0]:
            return lines[0].strip()

    return None


def add_samplesheet_to_description(description, samplesheet_format):
    """Add samplesheet format example to description if not already present."""
    if not samplesheet_format:
        return description

    # Check if samplesheet format is already mentioned
    if 'samplesheet format' in description.lower() or 'format:' in description.lower():
        return description

    # Add the format at the end
    format_text = f" Samplesheet format: `{samplesheet_format}`"

    return description + format_text


def process_app(app_path):
    """Process a single app.json file."""
    json_path = Path(app_path) / "app.json"

    if not json_path.exists():
        print(f"❌ Not found: {json_path}")
        return None

    try:
        # Read the app.json
        with open(json_path, 'r') as f:
            app = json.load(f)

        original_title = app.get('title', '')
        original_description = app.get('description', '')

        # Fix the title
        new_title = clean_title(original_title)

        # Extract samplesheet format
        content = app.get('content', '')
        spec = app.get('spec', [])
        samplesheet_format = extract_samplesheet_format(content, spec)

        # Update description with samplesheet format if applicable
        new_description = add_samplesheet_to_description(original_description, samplesheet_format)

        # Track changes
        changes = []
        if new_title != original_title:
            changes.append(f"Title: '{original_title}' → '{new_title}'")
            app['title'] = new_title

        if new_description != original_description and samplesheet_format:
            changes.append(f"Added samplesheet format: {samplesheet_format}")
            app['description'] = new_description

        if changes:
            # Write back the updated app.json
            with open(json_path, 'w') as f:
                json.dump(app, f, indent=2)

            print(f"✅ {app_path}")
            for change in changes:
                print(f"   {change}")
            return {"app": app_path, "changes": changes}
        else:
            print(f"ℹ️  {app_path} - No changes needed")
            return None

    except Exception as e:
        print(f"❌ Error processing {app_path}: {e}")
        return None


def main():
    """Process all apps."""
    base_dir = Path(__file__).parent

    print("=" * 80)
    print("FIXING ALL 73 NEXTFLOW APPS")
    print("=" * 80)
    print()

    results = []
    for app in APPS_TO_FIX:
        app_path = base_dir / app
        result = process_app(app_path)
        if result:
            results.append(result)
        print()

    print("=" * 80)
    print(f"SUMMARY: {len(results)} apps modified out of {len(APPS_TO_FIX)} total")
    print("=" * 80)

    return results


if __name__ == "__main__":
    main()
