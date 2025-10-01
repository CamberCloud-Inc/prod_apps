# Biomni Apps - Testing & Deployment Plan

**Date:** 2025-09-30
**Total Apps:** 205 (or 206 after adding missing wrapper)
**Testing Method:** Camber Cloud Platform via `camber app run`
**Reference:** Utility Apps Testing (25 apps validated successfully)

---

## Testing Strategy

### Phase 1: Validation Testing (Sample Apps)
Test 10-15 representative apps across categories to validate infrastructure

### Phase 2: Category Testing
Test 1-2 apps per category to ensure all patterns work

### Phase 3: Full Deployment
Deploy all apps to Camber platform

---

## Phase 1: Validation Testing (10-15 apps)

### Selection Criteria
- **Variety:** Different categories, dependencies, complexity
- **Low barrier:** Apps that don't require large model downloads
- **Representative:** Cover common patterns (file I/O, parameter handling, etc.)

### Selected Apps for Initial Testing

#### 1. **Literature Tools** (Easy - No heavy dependencies)
**Test Apps:**
- `biomni-query-pubmed` - PubMed search
- `biomni-extract-pdf-content` - PDF text extraction

**Test Command:**
```bash
# Create test query file
echo '{"query": "CRISPR", "max_results": 5}' > test_pubmed_query.json
camber stash upload test_pubmed_query.json

# Run app
camber app run biomni-query-pubmed \
  --param query_file=stash://david40962/test_pubmed_query.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** JSON with PubMed search results
**Duration:** ~30-60 seconds

---

#### 2. **Molecular Biology Tools** (Medium - Standard bioinformatics)
**Test Apps:**
- `biomni-design-primer` - Primer design
- `biomni-find-restriction-sites` - Find restriction enzyme sites

**Test Command:**
```bash
# Create test sequence
echo '{"sequence": "ATGGAATTCGATCGATCGGGATCCATCG", "enzyme": "EcoRI"}' > test_sequence.json
camber stash upload test_sequence.json

# Run app
camber app run biomni-find-restriction-sites \
  --param input_file=stash://david40962/test_sequence.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** List of restriction sites found
**Duration:** ~20-30 seconds

---

#### 3. **Database Query Tools** (Easy - API calls)
**Test Apps:**
- `biomni-query-uniprot` - UniProt protein database
- `biomni-query-kegg` - KEGG pathway database

**Test Command:**
```bash
# Create test query
echo '{"protein_id": "P12345"}' > test_uniprot.json
camber stash upload test_uniprot.json

# Run app
camber app run biomni-query-uniprot \
  --param input_file=stash://david40962/test_uniprot.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Protein information from UniProt
**Duration:** ~20-40 seconds

---

#### 4. **Genetics Tools** (Medium - Computational)
**Test Apps:**
- `biomni-liftover-coordinates` - Convert genome coordinates
- `biomni-simulate-demographic-history` - Population genetics simulation

**Test Command:**
```bash
# Create test coordinates
echo '{"chr": "chr1", "pos": 100000, "source": "hg19", "target": "hg38"}' > test_liftover.json
camber stash upload test_liftover.json

# Run app
camber app run biomni-liftover-coordinates \
  --param input_file=stash://david40962/test_liftover.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Converted coordinates
**Duration:** ~30-45 seconds

---

#### 5. **Biochemistry Tools** (Medium)
**Test Apps:**
- `biomni-analyze-enzyme-kinetics-assay` - Enzyme kinetics analysis
- `biomni-analyze-protein-conservation` - Protein conservation analysis

**Test Command:**
```bash
# Create test kinetics data
echo '{"substrate_conc": [1, 2, 5, 10, 20], "reaction_rate": [0.5, 0.8, 1.2, 1.5, 1.7]}' > test_kinetics.json
camber stash upload test_kinetics.json

# Run app
camber app run biomni-analyze-enzyme-kinetics-assay \
  --param input_file=stash://david40962/test_kinetics.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Km, Vmax calculations
**Duration:** ~20-30 seconds

---

#### 6. **Synthetic Biology Tools** (Medium)
**Test Apps:**
- `biomni-optimize-codons-for-heterologous-expression` - Codon optimization
- `biomni-create-biochemical-network-sbml-model` - SBML model creation

**Test Command:**
```bash
# Create test sequence
echo '{"sequence": "ATGAAACGCATTAGCACCACCATTACCACCACCATCACCACCACCATCACC", "organism": "E. coli"}' > test_codon.json
camber stash upload test_codon.json

# Run app
camber app run biomni-optimize-codons-for-heterologous-expression \
  --param input_file=stash://david40962/test_codon.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Optimized codon sequence
**Duration:** ~30-45 seconds

---

#### 7. **Glycoengineering Tools** (Easy)
**Test Apps:**
- `biomni-find-n-glycosylation-motifs` - Find glycosylation sites
- `biomni-predict-o-glycosylation-hotspots` - Predict O-glycosylation

**Test Command:**
```bash
# Create test protein sequence
echo '{"sequence": "MAFNHSQTYPFHLIHQGECQCEILNVSQWRDIVSYLEGR"}' > test_glyco.json
camber stash upload test_glyco.json

# Run app
camber app run biomni-find-n-glycosylation-motifs \
  --param input_file=stash://david40962/test_glyco.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** List of N-glycosylation motifs
**Duration:** ~15-25 seconds

---

#### 8. **Support Tools** (Easy)
**Test Apps:**
- `biomni-read-function-source-code` - Read function source

**Test Command:**
```bash
# Create test request
echo '{"function_name": "biomni.tool.genomics.interspecies_gene_conversion"}' > test_source.json
camber stash upload test_source.json

# Run app
camber app run biomni-read-function-source-code \
  --param input_file=stash://david40962/test_source.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Source code of function
**Duration:** ~15-20 seconds

---

#### 9. **Systems Biology Tools** (Medium)
**Test Apps:**
- `biomni-perform-flux-balance-analysis` - FBA on metabolic networks
- `biomni-model-protein-dimerization-network` - Protein dimerization modeling

**Test Command:**
```bash
# Create test FBA input
echo '{"model_id": "e_coli_core"}' > test_fba.json
camber stash upload test_fba.json

# Run app
camber app run biomni-perform-flux-balance-analysis \
  --param input_file=stash://david40962/test_fba.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Metabolic flux predictions
**Duration:** ~45-90 seconds

---

#### 10. **Microbiology Tools** (Medium)
**Test Apps:**
- `biomni-model-bacterial-growth-dynamics` - Growth curve modeling
- `biomni-predict-rna-secondary-structure` - RNA structure prediction

**Test Command:**
```bash
# Create test growth data
echo '{"time": [0, 1, 2, 3, 4, 5], "od600": [0.05, 0.1, 0.2, 0.4, 0.6, 0.8]}' > test_growth.json
camber stash upload test_growth.json

# Run app
camber app run biomni-model-bacterial-growth-dynamics \
  --param input_file=stash://david40962/test_growth.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

**Expected:** Growth parameters (lag, doubling time, etc.)
**Duration:** ~30-45 seconds

---

## Phase 2: Category Testing (1-2 per category)

### Testing Matrix

| Category | Test App 1 | Test App 2 | Priority |
|----------|-----------|-----------|----------|
| genomics | gene_set_enrichment_analysis | analyze_genomic_region_overlap | HIGH |
| genetics | ✅ liftover_coordinates | analyze_cas9_mutation_outcomes | HIGH |
| molecular_biology | ✅ find_restriction_sites | design_primer | HIGH |
| biochemistry | ✅ analyze_enzyme_kinetics_assay | - | MEDIUM |
| biophysics | predict_protein_disorder_regions | - | MEDIUM |
| bioengineering | analyze_cell_migration_metrics | - | MEDIUM |
| bioimaging | preprocess_image | calculate_similarity_metrics | MEDIUM |
| cancer_biology | perform_gene_expression_nmf_analysis | - | MEDIUM |
| cell_biology | quantify_cell_cycle_phases_from_microscopy | - | MEDIUM |
| immunology | analyze_cfse_cell_proliferation | - | MEDIUM |
| pathology | analyze_atp_luminescence_assay | - | MEDIUM |
| literature | ✅ query_pubmed | extract_pdf_content | HIGH |
| pharmacology | calculate_physicochemical_properties | query_fda_adverse_events | HIGH |
| microbiology | ✅ model_bacterial_growth_dynamics | - | MEDIUM |
| physiology | perform_cosinor_analysis | - | MEDIUM |
| systems_biology | ✅ perform_flux_balance_analysis | - | MEDIUM |
| synthetic_biology | ✅ optimize_codons_for_heterologous_expression | - | MEDIUM |
| glycoengineering | ✅ find_n_glycosylation_motifs | - | LOW |
| database | ✅ query_uniprot | query_ensembl | HIGH |
| support_tools | ✅ read_function_source_code | - | LOW |

**Total Tests:** 20-25 apps

---

## Phase 3: Deployment to Camber

### Step 1: Upload All App JSONs

```bash
# Create deployment script
cat > deploy_biomni_apps.sh << 'EOF'
#!/bin/bash

BIOMNI_DIR="/Users/david/git/prod_apps/biomni"
CATEGORIES=(
  "biochemistry" "bioengineering" "bioimaging" "biophysics"
  "cancer_biology" "cell_biology" "database" "genetics"
  "genomics" "glycoengineering" "immunology" "literature"
  "microbiology" "molecular_biology" "pathology" "pharmacology"
  "physiology" "support_tools" "synthetic_biology" "systems_biology"
)

for category in "${CATEGORIES[@]}"; do
  echo "Deploying $category apps..."
  for app_json in "$BIOMNI_DIR/$category"/*_app.json; do
    if [ -f "$app_json" ]; then
      app_name=$(basename "$app_json" _app.json)
      echo "  - Creating app: biomni-$app_name"
      camber app create "$app_json" || echo "    Failed (may already exist)"
    fi
  done
done

echo "Deployment complete!"
EOF

chmod +x deploy_biomni_apps.sh
```

### Step 2: Validate All Apps Created

```bash
# List all created apps
camber app list | grep "biomni-" | wc -l
# Expected: 205 (or 206 after adding missing wrapper)
```

### Step 3: Test Sample from Each Category

Use the testing matrix from Phase 2 to validate 1-2 apps per category.

---

## Testing Workflow

### 1. Prepare Test Data

```bash
# Create test data directory in stash
mkdir -p ~/biomni_test_data

# Create sample files for different data types
# DNA sequences
echo '{"sequence": "ATGGAATTCGATCG"}' > ~/biomni_test_data/dna_seq.json

# Protein sequences
echo '{"sequence": "MAFNHSQTYPFHLIH"}' > ~/biomni_test_data/protein_seq.json

# Numeric data
echo '{"values": [1, 2, 3, 4, 5]}' > ~/biomni_test_data/numeric_data.json

# Upload to stash
camber stash upload ~/biomni_test_data/* --remote-path biomni_test_data/
```

### 2. Automated Testing Script

```bash
cat > test_biomni_apps.sh << 'EOF'
#!/bin/bash

# Test configuration
TEST_APPS=(
  "biomni-query-pubmed"
  "biomni-find-restriction-sites"
  "biomni-query-uniprot"
  "biomni-liftover-coordinates"
  "biomni-analyze-enzyme-kinetics-assay"
  "biomni-optimize-codons-for-heterologous-expression"
  "biomni-find-n-glycosylation-motifs"
  "biomni-read-function-source-code"
  "biomni-perform-flux-balance-analysis"
  "biomni-model-bacterial-growth-dynamics"
)

RESULTS_FILE="biomni_test_results.md"
echo "# Biomni Apps Test Results" > "$RESULTS_FILE"
echo "**Date:** $(date)" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

for app in "${TEST_APPS[@]}"; do
  echo "Testing $app..."
  echo "## $app" >> "$RESULTS_FILE"

  # Run app (adjust parameters per app)
  JOB_ID=$(camber app run "$app" \
    --param inputFile=stash://david40962/biomni_test_data/test_input.json \
    --param outputDir=stash://david40962/biomni_test_output/ \
    --json | jq -r '.jobId')

  echo "Job ID: $JOB_ID" >> "$RESULTS_FILE"

  # Wait for completion (with timeout)
  TIMEOUT=300  # 5 minutes
  ELAPSED=0
  while [ $ELAPSED -lt $TIMEOUT ]; do
    STATUS=$(camber job get "$JOB_ID" --json | jq -r '.status')
    if [ "$STATUS" = "COMPLETED" ]; then
      echo "✅ Status: COMPLETED" >> "$RESULTS_FILE"
      break
    elif [ "$STATUS" = "FAILED" ]; then
      echo "❌ Status: FAILED" >> "$RESULTS_FILE"
      camber job logs "$JOB_ID" >> "$RESULTS_FILE"
      break
    fi
    sleep 10
    ELAPSED=$((ELAPSED + 10))
  done

  echo "" >> "$RESULTS_FILE"
done

echo "Testing complete! Results saved to $RESULTS_FILE"
EOF

chmod +x test_biomni_apps.sh
```

---

## Expected Issues & Solutions

### Issue 1: Dependency Installation Failures
**Symptoms:** Apps fail during `pip install` phase
**Solution:**
- Add retry logic to pip install
- Pre-build Docker images with common dependencies
- Use pip timeout and fallback mirrors

### Issue 2: Large Model Downloads
**Symptoms:** Apps timeout downloading ESM, UCE, or other large models
**Solution:**
- Increase job timeout for model-heavy apps
- Cache models in persistent storage
- Document expected download sizes/times

### Issue 3: External Tool Dependencies
**Symptoms:** Apps requiring MACS2, HOMER fail
**Solution:**
- Install via conda in wrapper script
- Pre-build containers with tools
- Document which apps need external tools

### Issue 4: Memory/Compute Requirements
**Symptoms:** Apps crash with OOM or take too long
**Solution:**
- Adjust jobConfig in app JSONs (increase CPU/RAM)
- Use appropriate node sizes (small_cpu → large_cpu)
- Document resource requirements

---

## Success Metrics

### Phase 1 Success Criteria:
- ✅ 8/10 test apps complete successfully (80% success rate)
- ✅ Git clone infrastructure works (proved by utility apps)
- ✅ Stash file I/O works correctly
- ✅ Dependency installation succeeds

### Phase 2 Success Criteria:
- ✅ At least 1 app per category succeeds
- ✅ Identify any category-specific issues
- ✅ Document resource requirements

### Phase 3 Success Criteria:
- ✅ All 205 apps deployed to Camber
- ✅ >90% of apps work when properly configured
- ✅ Documentation complete for all apps

---

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Phase 1** | 2-3 hours | Test 10 apps, validate infrastructure |
| **Phase 2** | 3-4 hours | Test 1-2 per category (20-25 apps) |
| **Phase 3** | 1-2 hours | Deploy all apps, validate deployment |
| **Total** | 6-9 hours | Complete testing and deployment |

---

## Deployment Checklist

### Pre-Deployment
- [ ] Add missing `analyze_immunohistochemistry_image` wrapper
- [ ] Verify all 206 app JSON files are valid
- [ ] Create test data files for validation testing
- [ ] Set up stash directory structure

### Phase 1 Testing
- [ ] Test 10 representative apps
- [ ] Document any failures
- [ ] Verify git clone works
- [ ] Verify stash I/O works
- [ ] Check dependency installation

### Phase 2 Testing
- [ ] Test 1-2 apps per category
- [ ] Document resource requirements
- [ ] Identify apps needing special configuration
- [ ] Update app JSONs with proper resource allocation

### Phase 3 Deployment
- [ ] Run deployment script
- [ ] Verify all apps created in Camber
- [ ] Validate with sample runs
- [ ] Create user documentation

### Post-Deployment
- [ ] Monitor first week of usage
- [ ] Collect user feedback
- [ ] Address any issues
- [ ] Update documentation

---

## Next Steps

1. **Immediate:** Add missing `analyze_immunohistochemistry_image` wrapper
2. **Today:** Start Phase 1 testing with 10 apps
3. **This Week:** Complete Phase 2 category testing
4. **Next Week:** Deploy all apps and create documentation

---

**Plan Created:** 2025-09-30
**Status:** Ready to Execute
**Total Apps to Deploy:** 205 (or 206 after adding missing wrapper)
