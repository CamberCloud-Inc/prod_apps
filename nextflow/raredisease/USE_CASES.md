# nf-core/raredisease Use Cases

## Overview

This document outlines potential use cases for the nf-core/raredisease pipeline, organized by priority and clinical relevance. Each use case represents a specific biologist-friendly application that can be implemented as a separate Camber app.

---

## Priority 1: Core Diagnostic Use Cases

### 1.1 Whole Genome Sequencing for Rare Disease Diagnosis (IMPLEMENTING)

**Biological Question**: What genetic variants are causing my patient's rare disease?

**When to Use**:
- Patient presents with undiagnosed genetic condition
- Clinical features suggest Mendelian disorder
- Need comprehensive genome-wide variant detection
- Previous targeted testing was negative

**Analysis Type**: WGS
**Variant Caller**: DeepVariant (AI-based, high accuracy)
**Sample Types**: Single patient or patient + parents (trio)

**Input Requirements**:
- Whole genome sequencing data (30x+ coverage)
- Patient clinical phenotype information
- Optional: Parental samples for inheritance analysis

**Expected Outputs**:
- Ranked list of candidate disease-causing variants
- SNVs, indels, structural variants, CNVs
- Annotations with gene function, pathogenicity scores
- Coverage reports to identify gaps

**Clinical Value**: Highest diagnostic yield (~40% in production), comprehensive variant detection

**Implementation Status**: ✅ IN PROGRESS - This is the first app being implemented

---

### 1.2 Whole Exome Sequencing for Rare Disease Diagnosis

**Biological Question**: What coding variants are responsible for my patient's condition?

**When to Use**:
- Cost-effective alternative to WGS
- Focus on protein-coding regions (98% of known disease genes)
- Budget constraints or large cohort screening
- Disease likely caused by coding variant

**Analysis Type**: WES
**Variant Caller**: DeepVariant
**Sample Types**: Patient samples with optional parental data

**Input Requirements**:
- Exome sequencing data (100x+ coverage of target regions)
- Target capture kit information
- Patient phenotype

**Expected Outputs**:
- Variants in coding regions and splice sites
- Filtered by coverage in target regions
- Prioritized by gene relevance to phenotype

**Clinical Value**: Cost-effective (~1/3 price of WGS), covers most disease-causing variants

**Implementation Status**: ⏳ PLANNED (Priority 2)

---

### 1.3 Trio Analysis for Recessive and De Novo Variants

**Biological Question**: Is this a recessive disease (from both parents) or a new mutation (de novo)?

**When to Use**:
- Patient with suspected genetic disease + both parents available
- Need to determine inheritance pattern
- Distinguish de novo from inherited variants
- Reduce candidate variant list via segregation analysis

**Analysis Type**: WGS or WES (trio)
**Variant Caller**: DeepVariant + GENMOD (inheritance annotation)
**Sample Types**: Patient + mother + father

**Input Requirements**:
- Sequencing data from all three individuals
- Family relationship information in samplesheet
- Patient phenotype

**Expected Outputs**:
- De novo variants (new in patient)
- Compound heterozygous variants (different mutation from each parent)
- Recessive homozygous variants
- Inheritance pattern annotations

**Clinical Value**: Dramatically reduces candidate variants, identifies causative inheritance patterns

**Implementation Status**: ⏳ PLANNED (Priority 4)

---

## Priority 2: Specialized Analysis Types

### 2.1 Mitochondrial Disease Analysis

**Biological Question**: Does my patient have a mitochondrial genetic disorder?

**When to Use**:
- Patient symptoms suggest mitochondrial disease (muscle weakness, neurological issues, metabolic problems)
- Need specialized mito genome analysis
- Standard WGS/WES may miss low-frequency heteroplasmies
- Multi-system disease presentation

**Analysis Type**: MITO
**Variant Caller**: Optimized for mitochondrial genome
**Sample Types**: Patient tissue samples

**Input Requirements**:
- WGS data (mito genome extracted)
- High coverage of mitochondrial DNA
- Patient phenotype with mito-specific symptoms

**Expected Outputs**:
- Mitochondrial variants with heteroplasmy levels
- Both homoplasmic and heteroplasmic variants
- Known pathogenic mito mutations
- Coverage of entire mitochondrial genome

**Clinical Value**: Specialized detection of mito variants including low-frequency heteroplasmies

**Implementation Status**: ⏳ PLANNED (Priority 3)

---

### 2.2 Structural Variant Detection for Complex Rearrangements

**Biological Question**: Are large genomic rearrangements causing disease?

**When to Use**:
- SNV/indel analysis was negative
- Disease may be caused by deletions, duplications, inversions
- Suspected genomic disorder (contiguous gene syndromes)
- Need CNV and SV detection

**Analysis Type**: WGS (SV-focused)
**Variant Caller**: Manta + Tiddit
**Sample Types**: Patient samples

**Input Requirements**:
- Whole genome sequencing (30x+ coverage)
- Short-read Illumina data
- Patient phenotype

**Expected Outputs**:
- Structural variants: deletions, duplications, inversions, translocations
- Copy number variants
- Breakpoint sequences
- Overlap with known disease-associated SVs

**Clinical Value**: Detects disease-causing variants missed by SNV/indel calling

**Implementation Status**: ⏳ PLANNED (Priority 5)

---

### 2.3 Repeat Expansion Detection

**Biological Question**: Does my patient have a repeat expansion disorder?

**When to Use**:
- Suspected repeat expansion disorder (Huntington's, Fragile X, etc.)
- Family history of repeat expansion disease
- Progressive neurological symptoms
- Anticipation observed in family

**Analysis Type**: WGS with ExpansionHunter
**Sample Types**: Patient samples

**Input Requirements**:
- Whole genome sequencing data
- Known repeat loci to interrogate
- Patient phenotype

**Expected Outputs**:
- Repeat sizes for disease-associated loci
- Comparison to normal/pathogenic thresholds
- Detected expansions in known disease genes

**Clinical Value**: Detects specific class of mutations difficult to find with standard sequencing

**Implementation Status**: ⏳ PLANNED (Priority 6)

---

## Priority 3: Extended Family and Population Analysis

### 3.1 Extended Pedigree Analysis

**Biological Question**: How does this variant segregate through multiple generations?

**When to Use**:
- Multiple affected family members
- Complex inheritance pattern
- Need to trace variant through extended family
- Validate causative variant

**Analysis Type**: WGS or WES (multiple samples)
**Sample Types**: Multiple family members across generations

**Input Requirements**:
- Sequencing from multiple family members
- Complete pedigree structure
- Affected status for all individuals

**Expected Outputs**:
- Variants segregating with disease in family
- Linkage information
- Inheritance pattern confirmation

**Clinical Value**: Confirms causative variants, rules out incidental findings

**Implementation Status**: ⏳ PLANNED (Priority 7)

---

### 3.2 Cohort Analysis for Gene Discovery

**Biological Question**: What genes are associated with this rare phenotype across multiple patients?

**When to Use**:
- Multiple unrelated patients with similar phenotype
- Gene discovery research
- Need to identify recurrently mutated genes
- Rare disease with unknown genetic cause

**Analysis Type**: WGS or WES (cohort)
**Sample Types**: Multiple unrelated patients

**Input Requirements**:
- Sequencing from multiple patients with shared phenotype
- Detailed phenotype data
- Control cohort or population databases

**Expected Outputs**:
- Genes with recurrent variants across patients
- Statistical evidence for gene-disease association
- Candidate novel disease genes

**Clinical Value**: Enables gene discovery, expands diagnostic capabilities

**Implementation Status**: ⏳ PLANNED (Priority 8)

---

## Priority 4: Quality Control and Technical Validation

### 4.1 Coverage Analysis and Gap Detection

**Biological Question**: Did my sequencing cover all medically relevant genes adequately?

**When to Use**:
- Verify sequencing quality before clinical interpretation
- Identify poorly covered regions
- Determine if resequencing is needed
- WES coverage assessment

**Analysis Type**: WGS or WES (QC-focused)
**Sample Types**: Any sequenced sample

**Input Requirements**:
- Sequencing data (any coverage)
- List of medically relevant genes/regions

**Expected Outputs**:
- Per-gene coverage statistics
- Regions below coverage thresholds
- QC pass/fail metrics
- Gaps requiring fill-in sequencing

**Clinical Value**: Ensures diagnostic quality, identifies technical limitations

**Implementation Status**: ⏳ PLANNED (Priority 9)

---

## Implementation Recommendations

### Immediate Implementation (Priority 1)
1. **WGS Rare Disease Analysis** - Standard use case, highest demand ✅ IMPLEMENTING

### Short-term Implementation (Priority 2-3)
2. **WES Rare Disease Analysis** - Cost-effective alternative
3. **Mitochondrial Analysis** - Specialized but important niche
4. **Trio Analysis** - High clinical value for family cases

### Medium-term Implementation (Priority 4-6)
5. **Structural Variant Detection** - Complements SNV/indel analysis
6. **Repeat Expansion Detection** - Specific disease classes
7. **Extended Pedigree Analysis** - Complex family structures

### Long-term Implementation (Priority 7-9)
8. **Cohort Analysis** - Research-focused
9. **Coverage QC** - Technical validation tool

---

## App Design Principles for Each Use Case

For each use case, the Camber app should:

1. **Hide Technical Complexity**: No mention of Nextflow, containers, or computational details
2. **Focus on Biology**: Emphasize the clinical question and diagnostic value
3. **Simplify Inputs**: 3-5 parameters maximum (samplesheet, output, genome, analysis type)
4. **Pre-configure Tools**: Hardcode optimal variant callers and settings
5. **Provide Clear Instructions**: Step-by-step samplesheet creation guide
6. **Explain Outputs**: Describe results in clinical terms (not file formats)
7. **Set Expectations**: Provide realistic analysis time and resource needs

---

## Samplesheet Examples for Each Use Case

### Single Patient (WGS/WES)
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,patient_R1.fq.gz,patient_R2.fq.gz,2,2,,,case001
```

### Trio Analysis
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,patient_R1.fq.gz,patient_R2.fq.gz,2,2,father01,mother01,case001
father01,L001,father_R1.fq.gz,father_R2.fq.gz,1,1,,,case001
mother01,L001,mother_R1.fq.gz,mother_R2.fq.gz,2,1,,,case001
```

### Multiple Unrelated Patients (Cohort)
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,p1_R1.fq.gz,p1_R2.fq.gz,1,2,,,case001
patient02,L001,p2_R1.fq.gz,p2_R2.fq.gz,2,2,,,case002
patient03,L001,p3_R1.fq.gz,p3_R2.fq.gz,1,2,,,case003
```

---

## Resource Requirements by Use Case

| Use Case | Node Size | CPUs | Memory | Time (est.) |
|----------|-----------|------|---------|-------------|
| WGS Single | LARGE | 64 | 360GB | 12-24h |
| WGS Trio | XLARGE | 96 | 540GB | 24-36h |
| WES Single | LARGE | 64 | 360GB | 4-8h |
| WES Trio | LARGE | 64 | 360GB | 8-16h |
| Mito Analysis | LARGE | 64 | 360GB | 6-12h |
| SV Detection | LARGE | 64 | 360GB | 12-24h |

---

## Testing Strategy

Each use case should be tested with:
1. **nf-core test dataset**: Minimal data for pipeline validation
2. **Public data**: GIAB or 1000 Genomes samples for WGS/WES
3. **Synthetic trio**: If available from nf-core
4. **Edge cases**: Single samples, trios, coverage variations

Maximum 5 test attempts per use case, documented in TESTING_LOG.md.

---

**Last Updated**: 2025-09-30
**Maintainer**: david40962