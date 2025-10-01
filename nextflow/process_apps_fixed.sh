#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arrays to track results
declare -a SUCCESSFUL_APPS
declare -a FAILED_APPS

# Counter
TOTAL=0
SUCCESS=0
FAILED=0

# All apps to process (73 total: 3 already enhanced + 70 from batches 14-21)
APPS=(
    "hicar/enhancer-promoter-loops"
    "liverctanalysis/ct-analysis"
    "deepvariant/clinical-wgs"
    "longraredisease/diagnostic-wgs"
    "scflow/cell-type-annotation"
    "methylarray/clinical-ewas"
    "viralmetagenome/viral-discovery"
    "ddamsproteomics/tmt-labeling"
    "phaseimpute/genotype-imputation"
    "tfactivity/tf-regulon-analysis"
    "epitopeprediction/vaccine-design"
    "imcyto/imaging-mass-cytometry"
    "cellpainting/phenotypic-profiling"
    "molkart/spatial-multiomics"
    "pixelator/spatial-proteomics"
    "diaproteomics/dia-discovery"
    "hgtseq/horizontal-gene-transfer"
    "rnadnavar/rna-editing-analysis"
    "pathogensurveillance/clinical-surveillance"
    "variantbenchmarking/benchmark-analysis"
    "alleleexpression/ase-analysis"
    "tumourevo/tumor-phylogeny"
    "drop/rna-outliers"
    "lncpipe/lncrna-discovery"
    "reportho/orthology-analysis"
    "callingcards/tf-binding"
    "drugresponseeval/drug-screening"
    "evexplorer/molecular-evolution"
    "diseasemodulediscovery/disease-networks"
    "variantcatalogue/population-variants"
    "viralintegration/hpv-integration"
    "multiplesequencealign/protein-msa"
    "pairgenomealign/synteny-analysis"
    "denovotranscript/de-novo-transcriptome"
    "denovohybrid/hybrid-assembly"
    "ssds/single-strand-dna"
    "tbanalyzer/tb-genomics"
    "sammyseq/sammy-analysis"
    "readsimulator/ngs-simulation"
    "seqinspector/sequencing-qc"
    "rarevariantburden/rare-disease-burden"
    "coproid/ancient-dna"
    "metapep/metaproteomics"
    "mitodetect/mitochondrial-variants"
    "proteinannotator/protein-annotation"
    "proteinfamilies/protein-families"
    "genomeannotator/eukaryote-annotation"
    "genomeassembler/short-read-assembly"
    "genomeqc/genome-qc"
    "genomeskim/organelle-genomes"
    "omicsgenetraitassociation/multi-omics-gwas"
    "bamtofastq/bam-conversion"
    "fastqrepair/fastq-repair"
    "fastquorum/quality-filtering"
    "createpanelrefs/reference-panels"
    "createtaxdb/taxonomy-db"
    "references/reference-management"
    "datasync/data-sync"
    "deepmodeloptim/ml-optimization"
    "abotyper/blood-antigens"
    "stableexpression/housekeeping-genes"
    "ribomsqc/ribo-profiling-qc"
    "lsmquant/label-free-ms"
    "panoramaseq/panorama-analysis"
    "radseq/rad-seq"
    "troughgraph/tumor-heterogeneity"
    "spinningjenny/spatial-transcriptomics"
    "mhcquant/immunopeptidomics"
    "methylong/long-read-methylation"
    "marsseq/mars-seq"
    "demo/demo-pipeline"
    "neutronstar/neutron-star-analysis"
    "rangeland/remote-sensing"
)

echo "=========================================="
echo "Processing ${#APPS[@]} Nextflow Apps"
echo "=========================================="
echo ""

for APP_PATH in "${APPS[@]}"; do
    TOTAL=$((TOTAL + 1))
    echo -e "${YELLOW}[$TOTAL/${#APPS[@]}] Processing: $APP_PATH${NC}"
    
    # Check if app.json exists
    JSON_FILE="/Users/david/git/prod_apps/nextflow/$APP_PATH/app.json"
    if [ ! -f "$JSON_FILE" ]; then
        echo -e "${RED}  ERROR: app.json not found at $JSON_FILE${NC}"
        FAILED=$((FAILED + 1))
        FAILED_APPS+=("$APP_PATH (app.json not found)")
        echo ""
        continue
    fi
    
    # Extract app name from JSON
    APP_NAME=$(grep '"name"' "$JSON_FILE" | head -1 | sed 's/.*"name": "\(.*\)",/\1/')
    
    if [ -z "$APP_NAME" ]; then
        echo -e "${RED}  ERROR: Could not extract app name from $JSON_FILE${NC}"
        FAILED=$((FAILED + 1))
        FAILED_APPS+=("$APP_PATH (name extraction failed)")
        echo ""
        continue
    fi
    
    echo "  App name: $APP_NAME"
    
    # Delete existing app (ignore errors if app doesn't exist)
    echo "  Deleting existing app..."
    camber app delete "$APP_NAME" 2>&1 | grep -v "Your version" | grep -v "latest version" | grep -v "To update" | grep -v "recommended" || true
    
    # Create/replace app using --file flag
    echo "  Creating app from JSON..."
    CREATE_OUTPUT=$(camber app create --file "$JSON_FILE" 2>&1)
    CREATE_EXIT_CODE=$?
    
    if [ $CREATE_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}  SUCCESS: $APP_NAME${NC}"
        SUCCESS=$((SUCCESS + 1))
        SUCCESSFUL_APPS+=("$APP_PATH -> $APP_NAME")
    else
        echo -e "${RED}  FAILED: Could not create $APP_NAME${NC}"
        ERROR_MSG=$(echo "$CREATE_OUTPUT" | grep -i "error" | head -1)
        echo -e "${RED}  Error: $ERROR_MSG${NC}"
        FAILED=$((FAILED + 1))
        FAILED_APPS+=("$APP_PATH -> $APP_NAME")
    fi
    
    echo ""
done

# Print summary
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Total apps processed: $TOTAL"
echo -e "${GREEN}Successful: $SUCCESS${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $SUCCESS -gt 0 ]; then
    echo "Successfully processed apps:"
    for APP in "${SUCCESSFUL_APPS[@]}"; do
        echo -e "  ${GREEN}✓${NC} $APP"
    done
    echo ""
fi

if [ $FAILED -gt 0 ]; then
    echo "Failed apps:"
    for APP in "${FAILED_APPS[@]}"; do
        echo -e "  ${RED}✗${NC} $APP"
    done
    echo ""
fi

exit 0
