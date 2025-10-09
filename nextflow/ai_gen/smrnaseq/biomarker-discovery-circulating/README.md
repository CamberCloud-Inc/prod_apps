# Circulating miRNA Biomarker Discovery

## Overview

This Camber app analyzes circulating microRNAs from liquid biopsy samples to discover disease biomarkers. Optimized for low-input biofluid samples (plasma, serum, CSF, urine) with UMI deduplication and stringent quality control.

## Use Case

**Research Question**: Which circulating miRNAs can serve as biomarkers for disease diagnosis, prognosis, or treatment monitoring?

**Target Users**:
- Clinical researchers developing diagnostic tests
- Translational researchers studying liquid biopsies
- Pharmaceutical companies validating safety biomarkers
- Precision medicine researchers

## What Makes This Different?

This configuration is specifically optimized for **biofluid samples**, not tissue:

### UMI Deduplication (`--with_umi`)
- Removes PCR duplicates using Unique Molecular Identifiers
- Essential for low-input samples that require PCR amplification
- Provides more accurate quantification for biomarker discovery

### Protocol Selection (`--protocol`)
- Explicitly specify library preparation method
- Critical for clinical samples where reproducibility is essential
- Ensures correct adapter trimming

### Enhanced Quality Control
- Stricter contamination filtering (rRNA, tRNA, DNA)
- Biofluid-specific QC metrics
- Hemolysis detection indicators

## Clinical Applications

### Cancer Diagnostics
- Early cancer detection panels
- Cancer type classification
- Minimal residual disease monitoring
- Recurrence prediction

### Drug Safety
- Organ injury biomarkers (FDA TransBioLine project)
- Liver injury: miR-122, miR-192
- Kidney injury: miR-21, miR-155
- Cardiac injury: miR-208a, miR-499

###Precision Medicine
- Treatment response prediction
- Drug resistance markers
- Patient stratification
- Adverse event prediction

### Disease Monitoring
- Non-invasive disease progression tracking
- Treatment efficacy monitoring
- Surrogate endpoints for clinical trials

## Input Requirements

### Samplesheet Format

CSV file with two columns:
- `sample`: Unique identifier (recommend: PatientID_Timepoint_Condition)
- `fastq_1`: Path or URL to single-end FASTQ file

**Example for biomarker study**:
```csv
sample,fastq_1
Patient001_Baseline_Cancer,stash://data/p001_t0.fastq.gz
Patient001_Post_Tx_Cancer,stash://data/p001_t1.fastq.gz
Patient002_Baseline_Cancer,stash://data/p002_t0.fastq.gz
Control_Healthy_001,stash://data/ctrl_001.fastq.gz
Control_Healthy_002,stash://data/ctrl_002.fastq.gz
Control_Healthy_003,stash://data/ctrl_003.fastq.gz
```

### Biofluid Sample Requirements

**Sample Types**:
- Plasma/Serum (most common)
- Cerebrospinal fluid (CSF)
- Urine
- Saliva
- Exosome fractions

**Quality Considerations**:
- Standardized collection protocol (timing, anticoagulant)
- Documented storage conditions
- Minimize freeze-thaw cycles (<3)
- Check for hemolysis (plasma/serum)

**Sequencing Depth**:
- Discovery phase: 10-20 million reads per sample
- Validation phase: 5-10 million reads per sample

## Library Preparation Protocols

Select the protocol matching your library prep:

1. **Illumina TruSeq Small RNA** (most common)
   - Standard clinical protocol
   - Good for most applications

2. **QIAseq miRNA Library Kit**
   - Includes UMIs built-in
   - Excellent for low-input samples
   - Reduced adapter dimers

3. **NEXTflex Small RNA-Seq**
   - Randomized adapters
   - Reduced ligation bias

4. **CATS Small RNA-seq**
   - Specialized for clinical samples

## Outputs

### Key Result Files

```
results/
├── edger/
│   ├── counts_deduplicated.tsv       # UMI-deduplicated counts (use this!)
│   ├── counts.tsv                    # Raw counts before deduplication
│   └── normalized_counts.tsv          # Normalized expression
├── umi_tools/
│   ├── dedup_stats.txt               # UMI deduplication statistics
│   └── *.dedup.bam                   # Deduplicated alignments
├── mirtrace/
│   └── mirtrace-report.html          # Biofluid-specific QC
├── multiqc/
│   └── multiqc_report.html           # Comprehensive QC
└── bowtie/
    └── stats.txt                     # Alignment statistics
```

### Critical QC Metrics

1. **UMI Deduplication Rate**
   - Expected: 20-40% of reads are PCR duplicates
   - Too high (>60%): Over-amplification, consider more input RNA
   - Too low (<10%): May indicate UMI issues

2. **miRNA Content**
   - Biofluid samples: >30% is good (lower than tissue)
   - <20%: Poor RNA quality or extraction issues

3. **Contamination**
   - rRNA: <10% (critical for biofluids)
   - High rRNA suggests extraction contamination

4. **Hemolysis Indicators** (for plasma/serum)
   - Elevated miR-451a and/or miR-16
   - Should be checked if present

## Biomarker Discovery Workflow

### 1. Quality Control (This Pipeline)
- Run this pipeline on all samples
- Review MultiQC and miRTrace reports
- Exclude low-quality samples (document exclusions)

### 2. Differential Expression
- Use `counts_deduplicated.tsv` for analysis
- DESeq2, edgeR, or limma
- Adjust for confounders (age, sex, batch)
- Multiple testing correction (FDR < 0.05)

### 3. Biomarker Candidate Selection
- Fold-change > 2x (up or down)
- Statistical significance (adjusted p < 0.05)
- ROC curve analysis (AUC > 0.7)
- Sensitivity/Specificity trade-offs

### 4. Validation
- Independent cohort
- qPCR validation of top candidates
- Prospective validation study

### 5. Clinical Utility
- Determine clinical cut-offs
- Assess clinical impact
- Regulatory pathway (if diagnostic)

## Experimental Design Recommendations

### Sample Size
- **Discovery**: Minimum 20-30 per group (power calculation recommended)
- **Validation**: Minimum 50-100 per group
- **Account for**: 10-20% sample failure rate

### Study Design
- **Case-Control**: Matched for confounders (age, sex, etc.)
- **Longitudinal**: Paired samples (baseline, post-treatment, follow-up)
- **Nested Case-Control**: From larger cohort
- **Cross-Sectional**: Multiple disease stages

### Technical Considerations
- Randomize sample processing order (avoid batch effects)
- Include technical replicates (5-10% of samples)
- Spike-in controls for normalization (optional but recommended)
- Document collection time, storage, processing delays

## Quality Flags to Watch

### Acceptable Samples
- ✅ miRNA content >30%
- ✅ UMI deduplication 20-40%
- ✅ rRNA <10%
- ✅ Library complexity high
- ✅ Read length peak at ~22 nt

### Problematic Samples
- ⚠️ miRNA content <20% → Poor quality, consider excluding
- ⚠️ UMI deduplication >60% → Over-amplification
- ⚠️ rRNA >15% → Extraction contamination
- ⚠️ Biased miRNA profile → Check for hemolysis
- ⚠️ Low library complexity → Sample degradation

## Compute Resources

- **XSMALL**: Testing (5-10 samples)
- **SMALL**: Small studies (10-50 samples) - recommended for most
- **MEDIUM**: Large discovery cohorts (50-200 samples)

## Real-World Examples

### FDA-Qualified Biomarkers
- **miR-122**: Drug-induced liver injury (DILI)
- Qualified by FDA for preclinical drug safety studies

### Clinical Use Cases
- **Prostate Cancer**: miR-141, miR-375 in urine
- **Alzheimer's Disease**: miRNA panels in CSF
- **Heart Failure**: miR-423-5p in plasma
- **Sepsis**: miRNA-based severity scores

## References

- TransBioLine Project (IMI2): miRNA safety biomarkers
- FDA Biomarker Qualification Program
- MIQE Guidelines for qPCR validation
- Minimal Information for Publication of Quantitative Real-Time PCR Experiments

## Support

For clinical study design consultation, consider engaging biostatisticians and regulatory experts early in your planning process.
