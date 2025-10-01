#!/usr/bin/env python3
import json
import re
import os
from pathlib import Path

# Map of app paths
APPS = {
    "hicar/enhancer-promoter-loops": "/Users/david/git/prod_apps/nextflow/hicar/enhancer-promoter-loops",
    "liverctanalysis/ct-analysis": "/Users/david/git/prod_apps/nextflow/liverctanalysis/ct-analysis",
    "deepvariant/clinical-wgs": "/Users/david/git/prod_apps/nextflow/deepvariant/clinical-wgs",
    "longraredisease/diagnostic-wgs": "/Users/david/git/prod_apps/nextflow/longraredisease/diagnostic-wgs",
    "scflow/cell-type-annotation": "/Users/david/git/prod_apps/nextflow/scflow/cell-type-annotation",
    "methylarray/clinical-ewas": "/Users/david/git/prod_apps/nextflow/methylarray/clinical-ewas",
    "viralmetagenome/viral-discovery": "/Users/david/git/prod_apps/nextflow/viralmetagenome/viral-discovery",
    "ddamsproteomics/tmt-labeling": "/Users/david/git/prod_apps/nextflow/ddamsproteomics/tmt-labeling",
    "phaseimpute/genotype-imputation": "/Users/david/git/prod_apps/nextflow/phaseimpute/genotype-imputation",
    "tfactivity/tf-regulon-analysis": "/Users/david/git/prod_apps/nextflow/tfactivity/tf-regulon-analysis",
    "epitopeprediction/vaccine-design": "/Users/david/git/prod_apps/nextflow/epitopeprediction/vaccine-design",
    "imcyto/imaging-mass-cytometry": "/Users/david/git/prod_apps/nextflow/imcyto/imaging-mass-cytometry",
    "cellpainting/phenotypic-profiling": "/Users/david/git/prod_apps/nextflow/cellpainting/phenotypic-profiling",
    "molkart/spatial-multiomics": "/Users/david/git/prod_apps/nextflow/molkart/spatial-multiomics",
    "pixelator/spatial-proteomics": "/Users/david/git/prod_apps/nextflow/pixelator/spatial-proteomics",
    "diaproteomics/dia-discovery": "/Users/david/git/prod_apps/nextflow/diaproteomics/dia-discovery",
    "hgtseq/horizontal-gene-transfer": "/Users/david/git/prod_apps/nextflow/hgtseq/horizontal-gene-transfer",
    "rnadnavar/rna-editing-analysis": "/Users/david/git/prod_apps/nextflow/rnadnavar/rna-editing-analysis",
    "pathogensurveillance/clinical-surveillance": "/Users/david/git/prod_apps/nextflow/pathogensurveillance/clinical-surveillance",
    "variantbenchmarking/benchmark-analysis": "/Users/david/git/prod_apps/nextflow/variantbenchmarking/benchmark-analysis",
    "alleleexpression/ase-analysis": "/Users/david/git/prod_apps/nextflow/alleleexpression/ase-analysis",
    "tumourevo/tumor-phylogeny": "/Users/david/git/prod_apps/nextflow/tumourevo/tumor-phylogeny",
    "drop/rna-outliers": "/Users/david/git/prod_apps/nextflow/drop/rna-outliers",
    "lncpipe/lncrna-discovery": "/Users/david/git/prod_apps/nextflow/lncpipe/lncrna-discovery",
    "reportho/orthology-analysis": "/Users/david/git/prod_apps/nextflow/reportho/orthology-analysis",
    "callingcards/tf-binding": "/Users/david/git/prod_apps/nextflow/callingcards/tf-binding",
    "drugresponseeval/drug-screening": "/Users/david/git/prod_apps/nextflow/drugresponseeval/drug-screening",
    "evexplorer/molecular-evolution": "/Users/david/git/prod_apps/nextflow/evexplorer/molecular-evolution",
    "diseasemodulediscovery/disease-networks": "/Users/david/git/prod_apps/nextflow/diseasemodulediscovery/disease-networks",
    "variantcatalogue/population-variants": "/Users/david/git/prod_apps/nextflow/variantcatalogue/population-variants",
    "viralintegration/hpv-integration": "/Users/david/git/prod_apps/nextflow/viralintegration/hpv-integration",
    "multiplesequencealign/protein-msa": "/Users/david/git/prod_apps/nextflow/multiplesequencealign/protein-msa",
    "pairgenomealign/synteny-analysis": "/Users/david/git/prod_apps/nextflow/pairgenomealign/synteny-analysis",
    "denovotranscript/de-novo-transcriptome": "/Users/david/git/prod_apps/nextflow/denovotranscript/de-novo-transcriptome",
    "denovohybrid/hybrid-assembly": "/Users/david/git/prod_apps/nextflow/denovohybrid/hybrid-assembly",
    "ssds/single-strand-dna": "/Users/david/git/prod_apps/nextflow/ssds/single-strand-dna",
    "tbanalyzer/tb-genomics": "/Users/david/git/prod_apps/nextflow/tbanalyzer/tb-genomics",
    "sammyseq/sammy-analysis": "/Users/david/git/prod_apps/nextflow/sammyseq/sammy-analysis",
    "readsimulator/ngs-simulation": "/Users/david/git/prod_apps/nextflow/readsimulator/ngs-simulation",
    "seqinspector/sequencing-qc": "/Users/david/git/prod_apps/nextflow/seqinspector/sequencing-qc",
    "rarevariantburden/rare-disease-burden": "/Users/david/git/prod_apps/nextflow/rarevariantburden/rare-disease-burden",
    "coproid/ancient-dna": "/Users/david/git/prod_apps/nextflow/coproid/ancient-dna",
    "metapep/metaproteomics": "/Users/david/git/prod_apps/nextflow/metapep/metaproteomics",
    "mitodetect/mitochondrial-variants": "/Users/david/git/prod_apps/nextflow/mitodetect/mitochondrial-variants",
    "proteinannotator/protein-annotation": "/Users/david/git/prod_apps/nextflow/proteinannotator/protein-annotation",
    "proteinfamilies/protein-families": "/Users/david/git/prod_apps/nextflow/proteinfamilies/protein-families",
    "genomeannotator/eukaryote-annotation": "/Users/david/git/prod_apps/nextflow/genomeannotator/eukaryote-annotation",
    "genomeassembler/short-read-assembly": "/Users/david/git/prod_apps/nextflow/genomeassembler/short-read-assembly",
    "genomeqc/genome-qc": "/Users/david/git/prod_apps/nextflow/genomeqc/genome-qc",
    "genomeskim/organelle-genomes": "/Users/david/git/prod_apps/nextflow/genomeskim/organelle-genomes",
    "omicsgenetraitassociation/multi-omics-gwas": "/Users/david/git/prod_apps/nextflow/omicsgenetraitassociation/multi-omics-gwas",
    "bamtofastq/bam-conversion": "/Users/david/git/prod_apps/nextflow/bamtofastq/bam-conversion",
    "fastqrepair/fastq-repair": "/Users/david/git/prod_apps/nextflow/fastqrepair/fastq-repair",
    "fastquorum/quality-filtering": "/Users/david/git/prod_apps/nextflow/fastquorum/quality-filtering",
    "createpanelrefs/reference-panels": "/Users/david/git/prod_apps/nextflow/createpanelrefs/reference-panels",
    "createtaxdb/taxonomy-db": "/Users/david/git/prod_apps/nextflow/createtaxdb/taxonomy-db",
    "references/reference-management": "/Users/david/git/prod_apps/nextflow/references/reference-management",
    "datasync/data-sync": "/Users/david/git/prod_apps/nextflow/datasync/data-sync",
    "deepmodeloptim/ml-optimization": "/Users/david/git/prod_apps/nextflow/deepmodeloptim/ml-optimization",
    "abotyper/blood-antigens": "/Users/david/git/prod_apps/nextflow/abotyper/blood-antigens",
    "stableexpression/housekeeping-genes": "/Users/david/git/prod_apps/nextflow/stableexpression/housekeeping-genes",
    "ribomsqc/ribo-profiling-qc": "/Users/david/git/prod_apps/nextflow/ribomsqc/ribo-profiling-qc",
    "lsmquant/label-free-ms": "/Users/david/git/prod_apps/nextflow/lsmquant/label-free-ms",
    "panoramaseq/panorama-analysis": "/Users/david/git/prod_apps/nextflow/panoramaseq/panorama-analysis",
    "radseq/rad-seq": "/Users/david/git/prod_apps/nextflow/radseq/rad-seq",
    "troughgraph/tumor-heterogeneity": "/Users/david/git/prod_apps/nextflow/troughgraph/tumor-heterogeneity",
    "spinningjenny/spatial-transcriptomics": "/Users/david/git/prod_apps/nextflow/spinningjenny/spatial-transcriptomics",
    "mhcquant/immunopeptidomics": "/Users/david/git/prod_apps/nextflow/mhcquant/immunopeptidomics",
    "methylong/long-read-methylation": "/Users/david/git/prod_apps/nextflow/methylong/long-read-methylation",
    "marsseq/mars-seq": "/Users/david/git/prod_apps/nextflow/marsseq/mars-seq",
    "demo/demo-pipeline": "/Users/david/git/prod_apps/nextflow/demo/demo-pipeline",
    "neutronstar/neutron-star-analysis": "/Users/david/git/prod_apps/nextflow/neutronstar/neutron-star-analysis",
    "rangeland/remote-sensing": "/Users/david/git/prod_apps/nextflow/rangeland/remote-sensing",
}

def has_samplesheet_info(description):
    """Check if description already contains samplesheet format info"""
    patterns = [
        r'samplesheet format:',
        r'sample sheet format:',
        r'samplesheet columns:',
        r'sample sheet columns:',
    ]
    desc_lower = description.lower()
    return any(re.search(pattern, desc_lower) for pattern in patterns)

def extract_samplesheet_format(content):
    """Extract samplesheet format from HTML content"""
    # Look for common patterns in the content
    patterns = [
        # Look for explicit format examples like: sample,fastq_1,fastq_2
        r'<code>([a-zA-Z_]+,[a-zA-Z_,]+)</code>',
        # Look for CSV column headers
        r'<strong>([a-zA-Z_]+)</strong>[,\s]+<strong>([a-zA-Z_]+)</strong>',
        # Look for table headers
        r'<th>([a-zA-Z_]+)</th>',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        if matches:
            if isinstance(matches[0], tuple):
                # Join tuple elements
                return ','.join(matches[0])
            else:
                return matches[0]

    return None

def process_app(app_name, app_path):
    """Process a single app"""
    app_json_path = os.path.join(app_path, "app.json")

    if not os.path.exists(app_json_path):
        return {"status": "missing", "reason": "app.json not found"}

    try:
        with open(app_json_path, 'r') as f:
            app_data = json.load(f)

        description = app_data.get('description', '')
        content = app_data.get('content', '')

        # Check if already has samplesheet info
        if has_samplesheet_info(description):
            return {"status": "skipped", "reason": "already has samplesheet info"}

        # Try to extract samplesheet format from content
        samplesheet_format = extract_samplesheet_format(content)

        if not samplesheet_format:
            return {"status": "skipped", "reason": "no samplesheet found in content"}

        # Add to description
        new_description = f"{description} Samplesheet format: `{samplesheet_format}`"
        app_data['description'] = new_description

        # Write back
        with open(app_json_path, 'w') as f:
            json.dump(app_data, f, indent=2)

        return {
            "status": "modified",
            "format": samplesheet_format,
            "app_json_path": app_json_path
        }

    except Exception as e:
        return {"status": "error", "reason": str(e)}

def main():
    results = {}

    for app_name, app_path in APPS.items():
        print(f"Processing {app_name}...")
        result = process_app(app_name, app_path)
        results[app_name] = result

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    modified = [k for k, v in results.items() if v["status"] == "modified"]
    skipped = [k for k, v in results.items() if v["status"] == "skipped"]
    errors = [k for k, v in results.items() if v["status"] == "error"]
    missing = [k for k, v in results.items() if v["status"] == "missing"]

    print(f"\nModified: {len(modified)}")
    for app in modified:
        print(f"  - {app}: {results[app]['format']}")

    print(f"\nSkipped: {len(skipped)}")
    for app in skipped:
        print(f"  - {app}: {results[app]['reason']}")

    if errors:
        print(f"\nErrors: {len(errors)}")
        for app in errors:
            print(f"  - {app}: {results[app]['reason']}")

    if missing:
        print(f"\nMissing: {len(missing)}")
        for app in missing:
            print(f"  - {app}: {results[app]['reason']}")

    # Save results for deployment
    with open('/Users/david/git/prod_apps/nextflow/samplesheet_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
