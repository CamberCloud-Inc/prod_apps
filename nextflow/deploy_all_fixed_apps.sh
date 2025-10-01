#!/bin/bash

# Deploy all 62 fixed Nextflow apps
# This script will delete and recreate each app

set -e  # Exit on error

BASE_DIR="/Users/david/git/prod_apps/nextflow"
cd "$BASE_DIR"

# Array of all apps that were modified
APPS=(
    "abotyper/blood-antigens"
    "alleleexpression/ase-analysis"
    "cellpainting/phenotypic-profiling"
    "createpanelrefs/reference-panels"
    "datasync/data-sync"
    "ddamsproteomics/tmt-labeling"
    "deepmodeloptim/ml-optimization"
    "deepvariant/clinical-wgs"
    "demo/demo-pipeline"
    "denovotranscript/de-novo-transcriptome"
    "diaproteomics/dia-discovery"
    "diseasemodulediscovery/disease-networks"
    "drop/rna-outliers"
    "drugresponseeval/drug-screening"
    "epitopeprediction/vaccine-design"
    "fastqrepair/fastq-repair"
    "fastquorum/quality-filtering"
    "genomeannotator/eukaryote-annotation"
    "genomeassembler/short-read-assembly"
    "genomeqc/genome-qc"
    "genomeskim/organelle-genomes"
    "hgtseq/horizontal-gene-transfer"
    "hicar/enhancer-promoter-loops"
    "imcyto/imaging-mass-cytometry"
    "liverctanalysis/ct-analysis"
    "longraredisease/diagnostic-wgs"
    "lsmquant/label-free-ms"
    "marsseq/mars-seq"
    "metapep/metaproteomics"
    "methylarray/clinical-ewas"
    "mhcquant/immunopeptidomics"
    "mitodetect/mitochondrial-variants"
    "molkart/spatial-multiomics"
    "multiplesequencealign/protein-msa"
    "neutronstar/neutron-star-analysis"
    "omicsgenetraitassociation/multi-omics-gwas"
    "pairgenomealign/synteny-analysis"
    "panoramaseq/panorama-analysis"
    "pathogensurveillance/clinical-surveillance"
    "phaseimpute/genotype-imputation"
    "pixelator/spatial-proteomics"
    "proteinannotator/protein-annotation"
    "proteinfamilies/protein-families"
    "radseq/rad-seq"
    "rangeland/remote-sensing"
    "readsimulator/ngs-simulation"
    "references/reference-management"
    "reportho/orthology-analysis"
    "ribomsqc/ribo-profiling-qc"
    "rnadnavar/rna-editing-analysis"
    "sammyseq/sammy-analysis"
    "scflow/cell-type-annotation"
    "seqinspector/sequencing-qc"
    "spinningjenny/spatial-transcriptomics"
    "ssds/single-strand-dna"
    "stableexpression/housekeeping-genes"
    "tbanalyzer/tb-genomics"
    "tfactivity/tf-regulon-analysis"
    "troughgraph/tumor-heterogeneity"
    "variantbenchmarking/benchmark-analysis"
    "variantcatalogue/population-variants"
    "viralintegration/hpv-integration"
)

echo "========================================"
echo "DEPLOYING 62 FIXED NEXTFLOW APPS"
echo "========================================"
echo ""

DEPLOYED=0
FAILED=0
FAILED_APPS=()

for APP in "${APPS[@]}"; do
    APP_PATH="$BASE_DIR/$APP"
    APP_JSON="$APP_PATH/app.json"

    # Extract app name from app.json
    APP_NAME=$(jq -r '.name' "$APP_JSON")

    echo "----------------------------------------"
    echo "[$((DEPLOYED + FAILED + 1))/62] Deploying: $APP"
    echo "App name: $APP_NAME"
    echo "----------------------------------------"

    # Delete existing app (ignore errors if app doesn't exist)
    echo "Deleting existing app..."
    camber app delete "$APP_NAME" 2>/dev/null || echo "  (App may not exist yet)"

    # Create app
    echo "Creating app..."
    if camber app create --file "$APP_JSON"; then
        echo "✅ Successfully deployed: $APP_NAME"
        ((DEPLOYED++))
    else
        echo "❌ Failed to deploy: $APP_NAME"
        ((FAILED++))
        FAILED_APPS+=("$APP")
    fi

    echo ""
done

echo "========================================"
echo "DEPLOYMENT SUMMARY"
echo "========================================"
echo "Total apps: 62"
echo "Successfully deployed: $DEPLOYED"
echo "Failed: $FAILED"

if [ $FAILED -gt 0 ]; then
    echo ""
    echo "Failed apps:"
    for FAILED_APP in "${FAILED_APPS[@]}"; do
        echo "  - $FAILED_APP"
    done
    exit 1
else
    echo ""
    echo "🎉 All apps deployed successfully!"
    exit 0
fi
