#!/bin/bash

FAILED_APPS=(
    "scflow/cell-type-annotation"
    "tfactivity/tf-regulon-analysis"
    "alleleexpression/ase-analysis"
    "drugresponseeval/drug-screening"
    "evexplorer/molecular-evolution"
    "createpanelrefs/reference-panels"
    "createtaxdb/taxonomy-db"
    "references/reference-management"
    "deepmodeloptim/ml-optimization"
    "stableexpression/housekeeping-genes"
    "panoramaseq/panorama-analysis"
    "troughgraph/tumor-heterogeneity"
    "spinningjenny/spatial-transcriptomics"
    "marsseq/mars-seq"
)

echo "Checking errors for failed apps:"
echo "=================================="
echo ""

for APP_PATH in "${FAILED_APPS[@]}"; do
    JSON_FILE="/Users/david/git/prod_apps/nextflow/$APP_PATH/app.json"
    APP_NAME=$(grep '"name"' "$JSON_FILE" | head -1 | sed 's/.*"name": "\(.*\)",/\1/')
    
    echo "App: $APP_PATH"
    echo "Name: $APP_NAME"
    echo "Error:"
    camber app create --file "$JSON_FILE" 2>&1 | grep -A 20 "Error:" | grep -v "Your version" | grep -v "latest version" | grep -v "To update" | grep -v "recommended" | head -20
    echo ""
    echo "---"
    echo ""
done
