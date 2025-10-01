# Biomni Test Data Mapping

Complete mapping of test data files to Biomni apps for validation testing.

---

## Phase 1: Priority Apps for Testing (10 apps)

### 1. Literature - query_pubmed
**Test Data:** `pubmed_query.json`
```json
{"query": "CRISPR gene editing", "max_results": 5}
```
**Command:**
```bash
camber app run biomni-query-pubmed \
  --param query_file=stash://david40962/biomni_test_data/pubmed_query.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 2. Molecular Biology - find_restriction_sites
**Test Data:** `restriction_test.json`
```json
{"sequence": "ATGGAATTCGATCGATCGGGATCCATCGATCGAAGCTTGCGGCCGCACTAGT", "enzyme": "EcoRI"}
```
**Command:**
```bash
camber app run biomni-find-restriction-sites \
  --param input_file=stash://david40962/biomni_test_data/restriction_test.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 3. Database - query_uniprot
**Test Data:** `uniprot_id.json`
```json
{"accession": "P04637"}
```
**Command:**
```bash
camber app run biomni-query-uniprot \
  --param input_file=stash://david40962/biomni_test_data/uniprot_id.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 4. Genetics - liftover_coordinates
**Test Data:** `genome_coordinates.json`
```json
{"chromosome": "chr1", "position": 100000, "source_build": "hg19", "target_build": "hg38"}
```
**Command:**
```bash
camber app run biomni-liftover-coordinates \
  --param input_file=stash://david40962/biomni_test_data/genome_coordinates.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 5. Biochemistry - analyze_enzyme_kinetics_assay
**Test Data:** `enzyme_kinetics.json`
```json
{"substrate_concentration": [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0], "reaction_rate": [0.45, 0.75, 1.2, 1.8, 2.1, 2.3, 2.4]}
```
**Command:**
```bash
camber app run biomni-analyze-enzyme-kinetics-assay \
  --param input_file=stash://david40962/biomni_test_data/enzyme_kinetics.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 6. Synthetic Biology - optimize_codons_for_heterologous_expression
**Test Data:** `codon_optimize.json`
```json
{"sequence": "ATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGT", "organism": "Escherichia coli"}
```
**Command:**
```bash
camber app run biomni-optimize-codons-for-heterologous-expression \
  --param input_file=stash://david40962/biomni_test_data/codon_optimize.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 7. Glycoengineering - find_n_glycosylation_motifs
**Test Data:** `protein_sequence.json`
```json
{"sequence": "MAFNHSQTYPFHLIHQGECQCEILNVSQWRDIVSYLEGRVMEPAKKEAAYSLVQHCLNPPIKRDVCQCSGTTAHWGRKGLNSTLVEAHEQGKSKAADLSQPGLDSHVGFDWLVESETSKPDQQFAALVKEAKRNLSQPKGAVCLIDK"}
```
**Command:**
```bash
camber app run biomni-find-n-glycosylation-motifs \
  --param input_file=stash://david40962/biomni_test_data/protein_sequence.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 8. Microbiology - model_bacterial_growth_dynamics
**Test Data:** `bacterial_growth.json`
```json
{"time_hours": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "od600": [0.05, 0.06, 0.08, 0.12, 0.20, 0.35, 0.55, 0.75, 0.85, 0.90, 0.92]}
```
**Command:**
```bash
camber app run biomni-model-bacterial-growth-dynamics \
  --param input_file=stash://david40962/biomni_test_data/bacterial_growth.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 9. Pharmacology - query_drug_interactions
**Test Data:** `drug_interaction.json`
```json
{"drugs": ["warfarin", "aspirin"]}
```
**Command:**
```bash
camber app run biomni-query-drug-interactions \
  --param input_file=stash://david40962/biomni_test_data/drug_interaction.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

### 10. Genomics - gene_set_enrichment_analysis
**Test Data:** `gene_list.json`
```json
["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS", "MYC", "PTEN", "RB1", "APC", "CDKN2A"]
```
**Command:**
```bash
camber app run biomni-gene-set-enrichment-analysis \
  --param genes_file=stash://david40962/biomni_test_data/gene_list.json \
  --param outputDir=stash://david40962/biomni_test_output/
```

---

## Complete Test Data Files

| File | Purpose | Used By Apps |
|------|---------|--------------|
| `gene_list.json` | Gene symbols | gene_set_enrichment_analysis, interspecies_gene_conversion |
| `dna_sequence.fasta` | DNA sequence | align_sequences, annotate_open_reading_frames, pcr_simple |
| `genome_coordinates.json` | Genomic positions | liftover_coordinates |
| `primer_target.json` | Primer design | design_primer, design_verification_primers |
| `restriction_test.json` | Enzyme sites | find_restriction_sites, find_restriction_enzymes, digest_sequence |
| `enzyme_kinetics.json` | Kinetics data | analyze_enzyme_kinetics_assay, analyze_protease_kinetics |
| `protein_sequence.json` | Protein sequence | find_n_glycosylation_motifs, predict_o_glycosylation_hotspots, predict_protein_disorder_regions |
| `cd_spectrum.json` | CD spectrum | analyze_circular_dichroism_spectra |
| `bacterial_growth.json` | Growth curve | model_bacterial_growth_dynamics, analyze_bacterial_growth_rate |
| `smiles_ligand.json` | Small molecule | run_diffdock_with_smiles, predict_admet_properties, calculate_physicochemical_properties |
| `uniprot_id.json` | Protein ID | query_uniprot |
| `pubmed_query.json` | Literature search | query_pubmed |
| `codon_optimize.json` | DNA for optimization | optimize_codons_for_heterologous_expression |
| `rna_sequence.json` | RNA sequence | predict_rna_secondary_structure, analyze_rna_secondary_structure_features |
| `drug_interaction.json` | Drug names | query_drug_interactions, check_drug_combination_safety |
| `ensembl_gene.json` | Gene ID | query_ensembl, get_gene_coding_sequence |
| `kegg_pathway.json` | Pathway ID | query_kegg |
| `doi.json` | Paper DOI | fetch_supplementary_info_from_doi |
| `arxiv_query.json` | arXiv search | query_arxiv |
| `pcr_params.json` | PCR setup | pcr_simple |
| `plasmid_sequence.json` | Plasmid ID | get_plasmid_sequence, annotate_plasmid |

---

## Upload Script

```bash
#!/bin/bash

cd /Users/david/git/prod_apps/biomni_test_data

echo "Uploading Biomni test data to stash..."

# Upload all JSON files
for file in *.json; do
  echo "  - Uploading $file"
  camber stash upload "$file" --remote-path "biomni_test_data/$file"
done

# Upload FASTA file
echo "  - Uploading dna_sequence.fasta"
camber stash upload dna_sequence.fasta --remote-path "biomni_test_data/dna_sequence.fasta"

echo "✅ All test data uploaded to stash://david40962/biomni_test_data/"
```

---

## Verification

```bash
# List uploaded files
camber stash ls biomni_test_data/

# Expected output: 21 files
```
