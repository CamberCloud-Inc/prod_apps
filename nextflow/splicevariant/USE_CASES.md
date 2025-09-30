# nf-core/rnasplice Use Cases

## Overview
nf-core/rnasplice is designed for alternative splicing analysis of RNA-seq data. Alternative splicing is a key regulatory mechanism that allows a single gene to produce multiple protein variants, playing crucial roles in development, disease, and cellular function.

## Priority Use Cases (Ranked by Importance)

### 1. **Disease vs. Control Differential Splicing** ⭐ HIGHEST PRIORITY
**Biological Question**: Which genes show altered splicing patterns in disease compared to healthy tissue?

**Experimental Design**:
- Compare disease samples (e.g., cancer, neurological disorders) vs. healthy controls
- Identify disease-specific splicing events
- Discover potential biomarkers and therapeutic targets

**Why It Matters**:
- Alternative splicing dysregulation is implicated in many diseases
- Can reveal disease mechanisms beyond gene expression changes
- Identifies therapeutic targets (e.g., splice-switching oligonucleotides)

**Input Requirements**:
- RNA-seq from disease and control samples (minimum 3 replicates each)
- Paired-end sequencing preferred (≥50M reads per sample)
- Reference genome with comprehensive gene annotations

**Expected Outputs**:
- Differential exon usage results
- Differential transcript usage results
- Alternative splicing events (exon skipping, intron retention, etc.)
- Quantification of isoform expression changes

**Analysis Methods Used**:
- DEXSeq for differential exon usage
- DRIMSeq + DEXSeq for differential transcript usage
- rMATS for alternative splicing events
- SUPPA2 for event-based and isoform-level analysis

---

### 2. **Treatment Response Splicing Analysis**
**Biological Question**: How does drug treatment or therapeutic intervention affect splicing patterns?

**Experimental Design**:
- Compare treated vs. untreated samples
- Time-course analysis of splicing changes
- Dose-response studies

**Applications**:
- Drug mechanism studies
- Identify splicing-related drug effects
- Optimize therapeutic dosing
- Understand resistance mechanisms

**Input Requirements**:
- RNA-seq from treated and control samples (3+ replicates per condition)
- Multiple time points or doses (optional but recommended)
- Consistent library preparation across samples

---

### 3. **Developmental Stage Splicing Dynamics**
**Biological Question**: How do splicing patterns change during development or differentiation?

**Experimental Design**:
- Multiple developmental stages or differentiation time points
- Track splicing switches during cell fate transitions
- Identify stage-specific isoforms

**Applications**:
- Developmental biology research
- Stem cell differentiation studies
- Tissue maturation processes
- Cellular reprogramming

**Input Requirements**:
- RNA-seq across developmental stages (3+ stages minimum)
- Biological replicates at each stage
- Consistent sample handling across time points

---

### 4. **Tissue-Specific Splicing Patterns**
**Biological Question**: What are the tissue-specific splicing differences across organs or cell types?

**Experimental Design**:
- Compare multiple tissues or cell types
- Identify tissue-specific isoforms
- Map splicing regulatory networks

**Applications**:
- Tissue biology studies
- Biomarker discovery
- Understanding tissue-specific disease mechanisms
- Cell type characterization

**Input Requirements**:
- RNA-seq from different tissues/cell types (3+ replicates per tissue)
- Similar sequencing depth across all samples
- Fresh or well-preserved samples for RNA quality

---

### 5. **Mutation Impact on Splicing**
**Biological Question**: How do genetic variants affect splicing regulation?

**Experimental Design**:
- Compare wildtype vs. mutant samples
- Analyze splice site variants
- Study splicing factor mutations

**Applications**:
- Rare disease diagnosis
- Understanding variant pathogenicity
- Splice site mutation analysis
- Splicing factor function studies

**Input Requirements**:
- RNA-seq from wildtype and variant samples
- Matched genetic variant information (VCF files)
- Multiple biological replicates

---

### 6. **Cancer Splicing Heterogeneity**
**Biological Question**: What splicing alterations occur in different cancer subtypes?

**Experimental Design**:
- Compare tumor samples vs. normal tissue
- Analyze multiple cancer subtypes
- Identify oncogenic splice variants

**Applications**:
- Cancer subtype classification
- Therapeutic target identification
- Biomarker discovery
- Understanding tumor heterogeneity

**Input Requirements**:
- Tumor and matched normal RNA-seq data
- Multiple samples per subtype
- Clinical annotation data

---

### 7. **Stress Response Splicing Changes**
**Biological Question**: How do environmental stresses affect splicing patterns?

**Experimental Design**:
- Compare stressed vs. unstressed samples
- Various stress conditions (heat shock, oxidative stress, etc.)
- Time-course analysis of stress response

**Applications**:
- Cell stress biology
- Understanding adaptation mechanisms
- Identify stress-responsive genes
- Drug toxicity studies

---

### 8. **Aging and Splicing Dysregulation**
**Biological Question**: How does aging affect splicing fidelity and patterns?

**Experimental Design**:
- Compare young vs. aged samples
- Multiple age groups
- Cross-tissue aging analysis

**Applications**:
- Aging research
- Neurodegenerative disease studies
- Longevity studies
- Age-related disease mechanisms

---

### 9. **Sex-Specific Splicing Differences**
**Biological Question**: What are the sex-dependent splicing patterns?

**Experimental Design**:
- Male vs. female sample comparisons
- Multiple tissues for sex-specific analysis
- Hormone-responsive splicing changes

**Applications**:
- Understanding sex-biased disease risk
- Reproductive biology
- Hormone regulation studies
- Personalized medicine

---

### 10. **Circadian Rhythm Splicing Oscillations**
**Biological Question**: How do splicing patterns change across the circadian cycle?

**Experimental Design**:
- Time-course sampling across 24-hour cycle
- Multiple time points (minimum 4-6 time points)
- Controlled light/dark conditions

**Applications**:
- Circadian biology research
- Sleep disorder studies
- Metabolic regulation
- Chronotherapy optimization

---

## Common Technical Requirements

### Sequencing Recommendations
- **Read Type**: Paired-end preferred (2x50bp minimum, 2x150bp optimal)
- **Depth**: ≥30-50M reads per sample for standard analysis
- **Depth for Events**: ≥80-100M reads for rare splicing event detection
- **Replicates**: Minimum 3 biological replicates per condition
- **Library**: Strand-specific libraries recommended for better isoform resolution

### Sample Quality
- RNA Integrity Number (RIN) ≥7 preferred
- Consistent library preparation method across all samples
- Batch effects minimized or documented

### Computational Requirements
- Reference genome with comprehensive annotations (GENCODE, Ensembl)
- Appropriate node size: MEDIUM to LARGE for most analyses
- Expected runtime: 6-12 hours for standard experiment (6-12 samples)

## Analysis Approach Priority by Use Case

| Use Case | Primary Method | Alternative Method | Complexity |
|----------|----------------|-------------------|------------|
| Disease vs. Control | DEXSeq (DEU) | rMATS (Events) | Medium |
| Treatment Response | DRIMSeq + DEXSeq (DTU) | SUPPA2 | Medium-High |
| Developmental Stages | SUPPA2 (Isoform) | rMATS | High |
| Tissue-Specific | DEXSeq (DEU) | SUPPA2 | Medium |
| Mutation Impact | rMATS (Events) | DEXSeq | High |
| Cancer Heterogeneity | DRIMSeq + DEXSeq (DTU) | rMATS | High |
| Stress Response | DEXSeq (DEU) | SUPPA2 | Medium |
| Aging Studies | DEXSeq (DEU) | DRIMSeq + DEXSeq | Medium |
| Sex Differences | DEXSeq (DEU) | rMATS | Medium |
| Circadian Rhythms | SUPPA2 (Isoform) | DEXSeq | High |

## Implementation Strategy

For the Camber platform, we will implement the **highest priority use case first**:

**App #1: Disease vs. Control Differential Splicing**
- Most common use case in research
- Clear biological interpretation
- Well-established analysis methods
- Broad applicability across disease types
- Straightforward experimental design

This app will be configured with:
- DEXSeq for differential exon usage (primary)
- rMATS for event-based splicing analysis (secondary)
- Optimized for 6-12 samples (3+ per condition)
- Biology-focused parameter descriptions
- Comprehensive output explanations