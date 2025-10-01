#!/bin/bash

apps=(
  "biomni/database/blast_sequence_app.json"
  "biomni/biochemistry/analyze_circular_dichroism_spectra_app.json"
  "biomni/biochemistry/analyze_enzyme_kinetics_assay_app.json"
  "biomni/biochemistry/analyze_itc_binding_thermodynamics_app.json"
  "biomni/physiology/analyze_hemodynamic_data_app.json"
  "biomni/cancer_biology/analyze_ddr_network_in_cancer_app.json"
  "biomni/systems_biology/model_protein_dimerization_network_app.json"
)

echo "Redeploying 7 apps with dependency fixes..."
echo "========================================================================"

for app_json in "${apps[@]}"; do
  app_name=$(basename "$app_json" | sed 's/_app\.json$//' | sed 's/_/-/g')
  app_name="biomni-${app_name}"
  
  echo "Deleting: $app_name"
  camber app delete "$app_name" 2>&1 | grep -q "deleted successfully" && echo "  ✅ Deleted" || echo "  ⏭️  Not found"
  
  echo "Deploying: $app_json"
  if camber app create --file "$app_json" 2>&1 | grep -q "App created successfully"; then
    echo "  ✅ Deployed successfully"
  else
    echo "  ❌ Failed"
  fi
  echo ""
done

echo "========================================================================"
echo "Redeployment complete"
