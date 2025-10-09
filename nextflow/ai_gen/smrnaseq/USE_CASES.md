# nf-core/smrnaseq Use Cases

This document details the specific use cases for small RNA sequencing analysis implemented as separate Camber apps.

---

## Use Case 1: miRNA Expression Profiling

**Biological Question**: What are the expression levels of known miRNAs in my samples?

**Target Users**:
- Cancer researchers studying miRNA dysregulation
- Developmental biologists tracking miRNA changes
- Disease researchers comparing healthy vs. diseased tissues
- Basic researchers profiling miRNA expression patterns

**Scientific Applications**:
- Differential miRNA expression between conditions
- miRNA expression signatures in cancer subtypes
- Developmental stage-specific miRNA profiles
- Tissue-specific miRNA characterization

**Input Requirements**:
- Single-end small RNA-seq FASTQ files (18-30 nt typically)
- Biological replicates recommended (minimum 3 per condition)
- Standard Illumina small RNA library prep

**Key Outputs**:
- miRNA expression counts table
- Normalized expression values
- Quality control metrics (adapter content, size distribution)
- MultiQC comprehensive report
- miRTrace quality control

**Parameters Exposed**:
- Sample sheet (required)
- Reference genome (required)
- Species code for miRTrace (required)
- Output directory (required)

**Parameters Hardcoded**:
- Protocol: auto-detect
- Quantification: EdgeR + Mirtop
- Quality filtering: standard thresholds
- Adapter trimming: automatic

**Resource Requirements**: SMALL (typical studies) to MEDIUM (many samples)

---

## Use Case 2: Biomarker Discovery (Circulating miRNA)

**Biological Question**: Which circulating miRNAs can serve as biomarkers for disease diagnosis or prognosis?

**Target Users**:
- Clinical researchers developing diagnostic tests
- Translational researchers studying liquid biopsies
- Pharmaceutical companies validating drug response biomarkers
- Precision medicine researchers

**Scientific Applications**:
- Cancer biomarker discovery from blood/plasma/serum
- Cardiovascular disease biomarkers
- Neurodegenerative disease monitoring
- Drug-induced organ injury biomarkers
- Disease progression tracking

**Input Requirements**:
- Single-end small RNA-seq from biofluids (plasma, serum, CSF, urine)
- Typically lower input amounts than tissue samples
- Quality control crucial for biofluid samples
- Spike-ins recommended for normalization

**Key Outputs**:
- miRNA expression profiles optimized for low-input samples
- Contamination filtering results
- miRTrace QC showing sample quality
- Normalized expression for biomarker candidates
- Technical variation assessment

**Parameters Exposed**:
- Sample sheet (required)
- Reference genome (required)
- Species code (required)
- Library protocol (required - important for clinical samples)
- Output directory (required)

**Parameters Hardcoded**:
- UMI deduplication: enabled (important for low input)
- Contamination filtering: enabled
- Quality thresholds: stringent for biomarker discovery
- Normalization: robust methods for biofluids

**Resource Requirements**: SMALL to MEDIUM

**Special Considerations**:
- Low input samples require careful QC
- Technical replicates important for biomarker validation
- Library protocol specification critical for clinical samples

---

## Use Case 3: Novel miRNA Discovery

**Biological Question**: Are there novel, previously unannotated miRNAs in my samples?

**Target Users**:
- Non-model organism researchers
- Cancer researchers studying tumor-specific miRNAs
- Plant biologists characterizing plant miRNAs
- Researchers studying disease-specific miRNA evolution

**Scientific Applications**:
- Novel miRNA discovery in non-model organisms
- Tumor-specific miRNA identification
- Species-specific miRNA annotation
- Tissue-specific novel miRNA characterization
- Viral miRNA discovery

**Input Requirements**:
- High-quality small RNA-seq data
- Deep sequencing recommended (>10M reads per sample)
- Multiple samples for validation
- Reference genome required

**Key Outputs**:
- Novel miRNA predictions with confidence scores
- Hairpin structure predictions
- Read coverage of novel miRNA loci
- Expression quantification of both known and novel miRNAs
- Validation metrics for novel predictions

**Parameters Exposed**:
- Sample sheet (required)
- Reference genome (required)
- Species code (required - use closest related species)
- Output directory (required)

**Parameters Hardcoded**:
- Novel miRNA discovery: enabled (MIRDeep2)
- Minimum read depth for discovery
- Hairpin structure prediction thresholds
- Conservation analysis

**Resource Requirements**: MEDIUM to LARGE (computationally intensive)

**Special Considerations**:
- Requires more computational resources
- Deep sequencing essential for discovery
- Novel miRNA validation requires experimental confirmation

---

## Implementation Priority

1. **Priority 1**: miRNA Expression Profiling (most common)
2. **Priority 2**: Biomarker Discovery (high clinical impact)
3. **Priority 3**: Novel miRNA Discovery (specialized use case)

---

## Common Parameters Across All Use Cases

**Always Required**:
- `--input`: Samplesheet CSV file
- `--genome`: Reference genome (GRCh38, GRCm39, etc.)
- `--mirtrace_species`: Species code ('hsa', 'mmu', 'rno', etc.)
- `--outdir`: Output directory

**Always Hardcoded**:
- Profile: Backend handles automatically (never specify)
- Version: `-r 2.4.0`
- Quality filtering: standard thresholds
- MultiQC: always enabled

---

## Reference Information

**Species Codes for miRTrace**:
- hsa: Homo sapiens (human)
- mmu: Mus musculus (mouse)
- rno: Rattus norvegicus (rat)
- dre: Danio rerio (zebrafish)
- cel: C. elegans
- ath: Arabidopsis thaliana

**Typical Read Lengths**:
- miRNAs: 18-25 nucleotides
- Other small RNAs: up to 30-35 nucleotides
- Sequencing reads: typically 50-75 nt single-end

**Library Protocols**:
- Illumina TruSeq Small RNA (most common)
- QIAseq miRNA Library Kit
- NEXTflex Small RNA-Seq Kit
- CATS Small RNA-seq Kit
