# nf-core/rnafusion Use Cases

This document identifies biological use cases for gene fusion detection using RNA-seq.

---

## Use Case 1: Cancer Fusion Detection (HIGHEST PRIORITY)

**Priority**: P0

**Biological Question**: Which fusion genes are driving this tumor's growth and could be therapeutic targets?

**Target Audience**: Cancer researchers, oncologists, clinical genomics labs studying solid tumors and treatment options

**Biological Background**:
Gene fusions are a hallmark of many cancers, particularly:
- **Lung cancer**: ALK, ROS1, RET fusions (targetable with specific inhibitors)
- **Breast cancer**: FGFR fusions
- **Prostate cancer**: TMPRSS2-ERG fusion (most common, ~50% of cases)
- **Thyroid cancer**: RET/PTC fusions
- **Sarcomas**: EWS-FLI1, SS18-SSX fusions (diagnostic)
- **Gliomas**: BRAF fusions, FGFR fusions

These fusions often create constitutively active kinases or transcription factors that drive oncogenesis.

**Typical Experimental Design**:
- Sample type: Tumor RNA (fresh frozen or FFPE) vs matched normal (optional)
- Data type: Illumina paired-end RNA-seq (2x100bp or 2x150bp)
- Sequencing depth: 50-100M paired reads per tumor sample
- Scale: 1-50 tumor samples for discovery or clinical testing

**Key Parameters**:

**Hardcoded** (optimized for cancer detection):
- All three fusion callers: STAR-Fusion, arriba, FusionCatcher
- GRCh38 reference (only supported genome)
- Quality filters: Default stringent settings
- Visualization: All output formats (PDF, VCF, HTML, TSV)
- StringTie for transcript assembly
- CTAT-Splicing for splicing aberrations

**Exposed** (user-configurable):
- Sample sheet (tumor RNA-seq files)
- Output directory
- Read trimming options (auto-detect quality)

**Expected Outputs**:
- List of detected fusion genes with confidence scores
- Visualization of fusion breakpoints
- Evidence from multiple callers (consensus increases confidence)
- VCF file for clinical reporting
- PDF report with fusion diagrams
- Annotations with known oncogenic fusions

**Biological Impact**:
- Identify actionable fusion targets for therapy (e.g., ALK inhibitors)
- Discover novel fusions in understudied cancer types
- Validate diagnostic fusions (e.g., EWS-FLI1 in Ewing sarcoma)
- Guide clinical trial enrollment based on fusion status

**Success Criteria**:
- Detects known fusions in positive controls
- Runs to completion with test dataset
- Produces all output formats
- MultiQC report shows QC metrics

---

## Use Case 2: Translocation Validation

**Priority**: P1

**Biological Question**: Does the chromosomal translocation detected by karyotyping or FISH result in an expressed fusion transcript?

**Target Audience**: Clinical cytogenetics labs, molecular pathologists validating cytogenetic findings

**Biological Background**:
Chromosomal translocations are often detected by:
- Karyotyping (G-banded chromosomes)
- FISH (fluorescence in situ hybridization)
- DNA sequencing (whole genome sequencing)

However, these methods only show DNA-level rearrangements. RNA-seq fusion detection validates that:
1. The translocation produces a fusion transcript
2. The fusion is expressed at detectable levels
3. The exact fusion breakpoint at RNA level

**Typical Experimental Design**:
- Sample type: RNA from cells/tissue with known translocation
- Comparison: Translocation-positive vs negative samples
- Sequencing: Deep RNA-seq (100M+ reads for rare fusions)
- Scale: 2-10 samples for validation studies

**Key Parameters**:

**Hardcoded**:
- All fusion callers for maximum sensitivity
- Relaxed filtering (to capture lower-expressing fusions)
- Comprehensive reporting

**Exposed**:
- Sample sheet
- Output directory
- Optional: Expected fusion genes (for targeted analysis)

**Expected Outputs**:
- Confirmation of fusion transcript expression
- Exact breakpoint location in cDNA
- Expression level (supporting read counts)
- Comparison to normal samples

**Biological Impact**:
- Validate diagnostic translocations
- Understand functional consequences of chromosomal rearrangements
- Identify in-frame vs out-of-frame fusions (only in-frame often functional)

---

## Use Case 3: Leukemia and Lymphoma Fusion Profiling

**Priority**: P1

**Biological Question**: Which fusion genes define this leukemia subtype and predict prognosis?

**Target Audience**: Hematologic oncology researchers, leukemia/lymphoma diagnostic labs

**Biological Background**:
Hematologic malignancies frequently harbor diagnostic and prognostic fusions:

**Acute Myeloid Leukemia (AML)**:
- PML-RARA (acute promyelocytic leukemia, APL) - responds to ATRA therapy
- RUNX1-RUNX1T1 (AML-M2) - favorable prognosis
- CBFB-MYH11 (AML-M4Eo) - favorable prognosis
- MLL (KMT2A) fusions - poor prognosis, many partners

**Acute Lymphoblastic Leukemia (ALL)**:
- BCR-ABL1 (Philadelphia chromosome) - targetable with TKIs
- ETV6-RUNX1 - favorable prognosis in pediatric ALL
- TCF3-PBX1 - common in pre-B ALL
- MLL rearrangements - poor prognosis in infant ALL

**Chronic Myeloid Leukemia (CML)**:
- BCR-ABL1 - defining fusion, treated with imatinib/TKIs

**Lymphomas**:
- NPM1-ALK in anaplastic large cell lymphoma
- IGH fusions in various B-cell lymphomas

**Typical Experimental Design**:
- Sample type: Bone marrow or peripheral blood RNA from leukemia patients
- Controls: Normal hematopoietic samples or remission samples
- Sequencing: 50-100M paired-end reads
- Scale: 5-100 samples for cohort studies

**Key Parameters**:

**Hardcoded**:
- All fusion callers
- Hematologic malignancy focus (leukemia-relevant fusions prioritized)
- Known fusion database annotation

**Exposed**:
- Sample sheet (patient samples)
- Output directory

**Expected Outputs**:
- Detected fusions with clinical annotations
- Comparison to known prognostic fusions
- Stratification of samples by fusion type
- VCF for clinical reporting

**Biological Impact**:
- Rapid molecular diagnosis (faster than traditional cytogenetics)
- Prognostic stratification (risk-adapted therapy)
- Minimal residual disease monitoring (detect fusion at low levels)
- Identify rare or novel fusions missed by targeted panels

---

## Implementation Priority Rationale

**Use Case 1 (Cancer Fusion Detection) is highest priority because**:

1. **Broadest applicability**: Works for solid tumors, sarcomas, and many cancer types
2. **Clinical relevance**: Identifies actionable therapeutic targets (ALK, ROS1, RET inhibitors)
3. **Established use case**: Most common application of fusion detection
4. **Test data available**: nf-core test-datasets has cancer RNA-seq data
5. **High impact**: Directly informs treatment decisions in precision oncology

**Use Cases 2 and 3 are secondary because**:
- Use Case 2: More specialized (validation studies rather than discovery)
- Use Case 3: Important but narrower audience (hematologic malignancies only)
- Both can leverage the same app infrastructure built for Use Case 1

---

## General Experimental Considerations

**Sample Quality**:
- Fresh frozen RNA preferred (higher quality)
- FFPE RNA acceptable but may reduce sensitivity
- RIN score ≥ 7 recommended for optimal results

**Sequencing Specifications**:
- Paired-end strongly recommended
- Read length: 100bp or 150bp (longer better for spanning breakpoints)
- Depth: 50-100M reads minimum, 100-200M for comprehensive detection

**Controls**:
- Positive controls: Cell lines with known fusions (e.g., K562 for BCR-ABL1)
- Negative controls: Normal tissue RNA
- Technical replicates: For validation studies

**Interpretation**:
- Require multiple supporting reads (default filters)
- Prioritize fusions detected by multiple callers
- Check if fusion is in-frame (likely functional)
- Annotate with known oncogenic fusion databases

---

## References and Resources

**nf-core/rnafusion Documentation**:
- Pipeline: https://nf-co.re/rnafusion
- GitHub: https://github.com/nf-core/rnafusion
- Publication: DOI 10.5281/zenodo.3946477

**Fusion Databases**:
- COSMIC Fusion: Cancer fusion gene database
- ChimerDB: Comprehensive fusion gene database
- FusionGDB: Fusion gene annotation database
- Mitelman Database: Chromosomal aberrations in cancer

**Clinical Resources**:
- OncoKB: Oncogenic fusion annotations and therapy
- CIViC: Clinical interpretation of variants (including fusions)
- NCCN Guidelines: Cancer treatment guidelines mentioning fusion biomarkers