# nf-core/hic Pipeline Use Cases

## Overview
Hi-C (High-throughput Chromosome Conformation Capture) is a powerful technique to study 3D genome organization. This document outlines common biological use cases and their implementations.

## Priority Ranking and Implementation Plan

### **Priority 1: Standard In Situ Hi-C (HIGHEST PRIORITY)** ✅
**Biological Question**: What is the 3D organization of chromatin in my cells?

**Use Case**: Standard Hi-C analysis using the in situ Hi-C protocol with restriction enzyme digestion (typically MboI or DpnII). This is the most common Hi-C protocol used in modern studies.

**When to Use**:
- Studying chromatin organization in cell types or tissues
- Identifying TADs (Topologically Associating Domains)
- Discovering A/B compartments (active/inactive chromatin)
- Understanding long-range gene regulation
- Comparing chromatin structure between conditions

**Input Requirements**:
- Paired-end Illumina sequencing (typically 50-150bp reads)
- 100-500 million read pairs (standard resolution)
- Restriction enzyme used (MboI, DpnII, HindIII most common)

**Expected Outputs**:
- Genome-wide contact maps at multiple resolutions
- TAD boundaries and compartment assignments
- Quality metrics and statistics

**Resource Needs**: MEDIUM to LARGE (depending on genome size and read depth)

---

### **Priority 2: DNase Hi-C**
**Biological Question**: What is chromatin organization without bias from restriction enzyme digestion?

**Use Case**: Hi-C analysis using DNase treatment instead of restriction enzymes. Provides unbiased fragmentation and higher resolution.

**When to Use**:
- Need unbiased chromatin fragmentation
- Working with organisms lacking optimal restriction sites
- Micro-C style experiments requiring higher resolution
- Comparative studies requiring protocol consistency

**Input Requirements**:
- Paired-end Illumina sequencing
- DNase-treated Hi-C libraries
- Higher sequencing depth recommended (500M-1B+ reads)

**Resource Needs**: LARGE to XLARGE

---

### **Priority 3: Capture Hi-C / Targeted Hi-C**
**Biological Question**: What are the 3D interactions of specific genomic regions?

**Use Case**: Hi-C analysis focused on pre-selected genomic regions (promoters, enhancers, disease loci).

**When to Use**:
- Studying specific gene regulatory regions
- Following up GWAS hits with 3D context
- Cost-effective alternative for targeted questions
- Disease variant interpretation (which genes do regulatory variants contact?)

**Input Requirements**:
- Standard Hi-C library with capture probes
- Target region BED file
- Lower sequencing depth acceptable (50-100M reads)

**Resource Needs**: MEDIUM

---

### **Priority 4: HiChIP Analysis**
**Biological Question**: What are the chromatin interactions mediated by a specific protein?

**Use Case**: Combined Hi-C and ChIP-seq to identify protein-mediated chromatin loops (e.g., cohesin-mediated loops, enhancer-promoter interactions via H3K27ac).

**When to Use**:
- Studying specific protein-mediated loops (CTCF, cohesin, Mediator)
- Identifying enhancer-promoter interactions
- Cell type-specific regulatory interactions
- More efficient than full Hi-C for loop detection

**Input Requirements**:
- HiChIP sequencing data (paired-end)
- Antibody target information
- Typically 100-300M read pairs

**Resource Needs**: MEDIUM to LARGE

---

### **Priority 5: Time Series / Comparative Hi-C**
**Biological Question**: How does chromatin organization change across conditions, development, or disease states?

**Use Case**: Multiple Hi-C samples analyzed together for comparative analysis (e.g., normal vs disease, time course during development, before/after treatment).

**When to Use**:
- Developmental studies (embryonic development, differentiation)
- Disease vs healthy tissue comparisons
- Drug treatment responses
- Cell cycle dynamics

**Input Requirements**:
- Multiple Hi-C samples (3+ per condition recommended)
- Consistent protocol across samples
- Biological replicates essential

**Resource Needs**: LARGE to XLARGE

---

### **Priority 6: High-Resolution Hi-C / Micro-C**
**Biological Question**: What is the chromatin organization at nucleosome resolution?

**Use Case**: Ultra-high resolution Hi-C analysis using Micro-C protocol (MNase digestion) to achieve nucleosome-level resolution.

**When to Use**:
- Need nucleosome-resolution contact maps
- Studying detailed chromatin fiber organization
- Examining fine-scale regulatory interactions
- Research questions requiring sub-TAD resolution

**Input Requirements**:
- Micro-C sequencing libraries (MNase treatment)
- Very high sequencing depth (1-5 billion+ read pairs)
- Small genome preferred or specific regions

**Resource Needs**: XLARGE

---

### **Priority 7: Low-Input Hi-C**
**Biological Question**: What is chromatin organization in rare cell populations or limited samples?

**Use Case**: Hi-C analysis optimized for low cell number inputs (1,000-50,000 cells).

**When to Use**:
- Rare cell populations (stem cells, primary tissues)
- Clinical samples with limited material
- Sorted cell populations
- Early embryos or small organisms

**Input Requirements**:
- Optimized low-input Hi-C protocol
- 1K-50K cells
- Standard paired-end sequencing
- May have lower complexity/coverage

**Resource Needs**: MEDIUM

---

### **Priority 8: Single-Cell Hi-C**
**Biological Question**: How does chromatin organization vary between individual cells?

**Use Case**: Hi-C analysis on single cells to understand cell-to-cell variation in 3D genome organization.

**When to Use**:
- Understanding cellular heterogeneity
- Studying stochastic vs deterministic chromatin organization
- Rare cell studies
- Developmental biology at single-cell resolution

**Input Requirements**:
- Single-cell Hi-C sequencing data
- Specialized protocol and analysis
- Many cells needed (50-1000+)
- Lower coverage per cell

**Resource Needs**: XLARGE

---

## Common Biological Questions and Recommended Use Cases

### **Q: What genes are regulated by an enhancer?**
**Recommended**: Priority 3 (Capture Hi-C) or Priority 4 (HiChIP with H3K27ac)

### **Q: How does chromatin organization change during differentiation?**
**Recommended**: Priority 5 (Time Series Hi-C) with standard protocol

### **Q: What is the 3D structure of my genome of interest?**
**Recommended**: Priority 1 (Standard In Situ Hi-C)

### **Q: Which regulatory variants affect 3D genome organization?**
**Recommended**: Priority 3 (Capture Hi-C) targeting variant regions

### **Q: How do CTCF or cohesin organize loops?**
**Recommended**: Priority 4 (HiChIP) with CTCF or SMC1 antibody

### **Q: What are nucleosome-level interactions?**
**Recommended**: Priority 6 (Micro-C / High-Resolution Hi-C)

### **Q: How does chromatin organize in rare cell populations?**
**Recommended**: Priority 7 (Low-Input Hi-C) or Priority 8 (Single-Cell Hi-C)

---

## Implementation Notes

### Standard Hi-C Parameters
- **Restriction Enzyme**: Most common are MboI (^GATC), DpnII (^GATC), HindIII (A^AGCTT)
- **Resolution**: 5kb-50kb for TAD calling, 1kb for loops
- **Read Depth**: 100-500M pairs for mammalian genome
- **Genome**: Human (GRCh38), Mouse (GRCm39), or custom

### Quality Metrics to Monitor
- **Valid Pairs %**: Should be >40% for good libraries
- **Cis/Trans Ratio**: >70% cis interactions expected for Hi-C
- **Duplicate Rate**: <30% duplicates ideal
- **Long-Range Contacts**: Good Hi-C shows contacts >20kb

### Resource Scaling
- **Human genome, 200M reads**: MEDIUM (32 CPU, 120GB RAM)
- **Human genome, 500M reads**: LARGE (64 CPU, 360GB RAM)
- **Human genome, 1B+ reads**: XLARGE (96 CPU, 540GB RAM)
- **Small genomes (bacteria, yeast)**: SMALL to MEDIUM

---

## Selected Implementation: Priority 1 - Standard In Situ Hi-C
This use case will be implemented first as it represents the most common Hi-C application and serves as a foundation for other specialized protocols.