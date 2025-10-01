# Biomni Test Data

Test data files for validating all 205 Biomni apps on Camber platform.

**Created:** 2025-09-30
**Purpose:** Functional testing of Biomni biomedical research tools

---

## Upload to Stash

```bash
# Upload all test data to stash
cd /Users/david/git/prod_apps/biomni_test_data
camber stash upload . --remote-path biomni_test_data/
```

---

## Test Data Files by Category

### Genomics & Genetics
- `gene_list.json` - List of human gene symbols
- `dna_sequence.fasta` - Sample DNA sequence
- `genome_coordinates.json` - Genomic coordinates for liftover
- `vcf_sample.vcf` - Variant call format sample
- `bed_regions.bed` - BED format genomic regions

### Molecular Biology
- `primer_target.json` - Target sequence for primer design
- `plasmid_sequence.json` - Plasmid sequence data
- `restriction_test.json` - Sequence for restriction enzyme analysis
- `pcr_params.json` - PCR parameters

### Biochemistry & Biophysics
- `enzyme_kinetics.json` - Enzyme kinetics data (substrate conc, rates)
- `protein_sequence.json` - Protein amino acid sequence
- `cd_spectrum.json` - Circular dichroism spectrum data
- `itc_data.json` - Isothermal titration calorimetry data

### Cell & Cancer Biology
- `flow_cytometry.csv` - Flow cytometry data
- `growth_curve.json` - Cell growth measurements over time
- `microscopy_coords.json` - Cell coordinates from microscopy

### Imaging & Pathology
- `test_image.tiff` - Sample microscopy image (grayscale)
- `image_pair.json` - Pair of images for registration

### Pharmacology & Drug Discovery
- `smiles_ligand.json` - SMILES string for small molecule
- `protein_pdb.json` - Protein structure identifier
- `drug_interaction.json` - Drug names for interaction check
- `admet_smiles.json` - SMILES for ADMET prediction

### Microbiology & Physiology
- `bacterial_growth.json` - Bacterial growth OD600 measurements
- `rna_sequence.json` - RNA sequence for structure prediction
- `hemodynamic_data.json` - Blood pressure/flow data

### Systems & Synthetic Biology
- `metabolic_model.json` - Metabolic model identifier
- `gene_circuit.json` - Gene circuit parameters
- `codon_optimize.json` - Sequence for codon optimization

### Database Queries
- `uniprot_id.json` - UniProt protein ID
- `ensembl_gene.json` - Ensembl gene ID
- `pubmed_query.json` - PubMed search query
- `kegg_pathway.json` - KEGG pathway ID

### Literature
- `pdf_url.json` - URL to sample PDF
- `doi.json` - DOI for paper lookup
- `arxiv_query.json` - arXiv search terms
