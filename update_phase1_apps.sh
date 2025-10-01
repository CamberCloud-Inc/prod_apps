#!/bin/bash

# Update the 10 Phase 1 apps with new comprehensive documentation
# These apps already exist and need to be deleted and recreated

echo "========================================================================"
echo "Updating 10 Phase 1 Biomni Apps with New Documentation"
echo "========================================================================"
echo ""

# List of Phase 1 apps that need updating
apps=(
    "analyze_enzyme_kinetics_assay:biochemistry"
    "query_uniprot:database"
    "liftover_coordinates:genetics"
    "gene_set_enrichment_analysis:genomics"
    "find_n_glycosylation_motifs:glycoengineering"
    "query_pubmed:literature"
    "model_bacterial_growth_dynamics:microbiology"
    "find_restriction_sites:molecular_biology"
    "query_drug_interactions:pharmacology"
    "optimize_codons_for_heterologous_expression:synthetic_biology"
)

updated=0
failed=0

for app_entry in "${apps[@]}"; do
    app_name=$(echo "$app_entry" | cut -d: -f1)
    category=$(echo "$app_entry" | cut -d: -f2)
    json_file="biomni/${category}/${app_name}_app.json"

    echo "Updating: biomni-$app_name (category: $category)"

    # Delete the existing app
    echo "  Deleting existing app..."
    if camber app delete "biomni-$app_name" 2>&1; then
        echo "  ✅ Deleted"

        # Brief pause
        sleep 0.5

        # Recreate with new documentation
        echo "  Creating with new documentation..."
        if camber app create --file "$json_file" 2>&1; then
            echo "  ✅ Updated successfully"
            updated=$((updated + 1))
        else
            echo "  ❌ Failed to recreate"
            failed=$((failed + 1))
        fi
    else
        echo "  ❌ Failed to delete"
        failed=$((failed + 1))
    fi

    echo ""
    sleep 0.5
done

echo ""
echo "========================================================================"
echo "Update Summary"
echo "========================================================================"
echo "Updated:        $updated"
echo "Failed:         $failed"
echo "========================================================================"
