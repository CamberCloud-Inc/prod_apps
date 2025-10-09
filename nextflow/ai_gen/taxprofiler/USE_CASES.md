# nf-core/taxprofiler: Use Cases

This document identifies and describes biological use cases for the taxprofiler pipeline.

---

## Use Case 1: Microbiome Profiling with Kraken2 (HIGHEST PRIORITY)

**Priority**: P0

**Biological Question**: What microorganisms are present in my sample and in what relative abundances?

**Target Audience**:
- Microbiome researchers studying gut, skin, oral, or environmental communities
- Biologists investigating host-microbe interactions
- Environmental scientists profiling microbial diversity

**Typical Experimental Design**:
- Sample type: Shotgun metagenomic sequencing from any environment
- Data type: Illumina paired-end or single-end reads (50-150bp)
- Scale: 1-50 samples
- Depth: 1-10 million reads per sample (for basic profiling)

**Why Kraken2**:
- Fastest taxonomic classifier (millions of reads per minute)
- Accurate for well-characterized organisms
- Standard tool in microbiome field
- Good balance of speed and accuracy
- Most commonly used profiler

**Key Parameters**:

*Hardcoded (hidden from users)*:
- Pipeline version: 1.2.3
- Profiler: Kraken2 only (run_kraken2=true)
- Preprocessing: Basic quality filtering with fastp
- Output format: Standardized taxonomic tables
- Skip other profilers: run_metaphlan=false, run_motus=false, etc.

*Exposed to users*:
- Sample sheet (FASTQ files)
- Database sheet (Kraken2 database path)
- Output directory
- Optional: Host removal (for human samples)

**Expected Outputs**:
- Kraken2 classification reports per sample
- Standardized taxonomic abundance tables (via TAXPASTA)
- Quality control reports (MultiQC)
- Visualization-ready abundance matrices

**Resource Requirements**:
- XSMALL for testing with nf-core test data
- SMALL to MEDIUM for real data (depends on database size)
- Kraken2 standard database requires ~50GB RAM

**Implementation Notes**:
- Must provide Kraken2 database via database sheet
- Can use nf-core test database for testing
- Host removal optional but common for human microbiome studies

---

## Use Case 2: Clinical Pathogen Detection

**Priority**: P0

**Biological Question**: What pathogens are present in this clinical sample (blood, CSF, tissue)?

**Target Audience**:
- Clinical microbiologists
- Infectious disease researchers
- Diagnostic laboratories
- Hospital infection control teams

**Typical Experimental Design**:
- Sample type: Clinical specimens (blood, cerebrospinal fluid, tissue biopsies)
- Data type: Illumina paired-end sequencing (rapid turnaround)
- Scale: 1-20 samples per run
- Depth: 5-20 million reads (higher for low-abundance pathogens)
- Time-critical: Results needed within hours

**Why This Matters**:
- Culture-independent pathogen identification
- Detects fastidious or unculturable organisms
- Faster than traditional culture methods
- Can identify antibiotic resistance genes

**Key Parameters**:

*Hardcoded (hidden from users)*:
- Pipeline version: 1.2.3
- Profiler: Kraken2 (speed) + Bracken (abundance refinement)
- Preprocessing: Aggressive quality filtering, host removal
- Database: Comprehensive pathogen database
- Focus on bacteria, viruses, fungi

*Exposed to users*:
- Sample sheet (FASTQ files)
- Sample type (blood, CSF, tissue) - determines host filtering
- Output directory
- Urgency level (affects resource allocation)

**Expected Outputs**:
- Pathogen identification reports
- Relative abundance of detected organisms
- Confidence scores for detections
- Clinically-relevant organism focus

**Resource Requirements**:
- MEDIUM node for speed
- Higher priority processing for urgent clinical samples

**Implementation Notes**:
- Requires comprehensive pathogen database
- Host removal critical (most reads are human)
- May need database with viral, bacterial, and fungal sequences
- Consider antibiotic resistance gene detection in future version

---

## Use Case 3: Comprehensive Multi-Tool Taxonomic Profiling

**Priority**: P1

**Biological Question**: How do different taxonomic profilers compare on my samples? What is the consensus taxonomy?

**Target Audience**:
- Bioinformatics researchers validating methods
- Labs establishing best practices
- Researchers with novel/unusual sample types
- Publications requiring method comparison

**Typical Experimental Design**:
- Sample type: Any metagenomic data
- Data type: Illumina or Nanopore
- Scale: 1-10 samples (high computational cost per sample)
- Depth: Variable
- Goal: Method comparison and consensus taxonomy

**Why Multiple Tools**:
- Different algorithms have different biases
- Consensus across tools increases confidence
- Novel organisms may be detected by only some tools
- Important for validating unexpected findings

**Key Parameters**:

*Hardcoded (hidden from users)*:
- Pipeline version: 1.2.3
- Profilers: Kraken2 + MetaPhlAn + mOTUs (most common trio)
- Preprocessing: Standard quality filtering
- Standardized output: TAXPASTA for cross-tool comparison

*Exposed to users*:
- Sample sheet (FASTQ files)
- Database sheet (databases for all three tools)
- Output directory
- Minimum abundance threshold for reporting

**Expected Outputs**:
- Separate taxonomic profiles from each tool
- Standardized comparison tables
- Consensus taxonomy (organisms detected by multiple tools)
- Tool-specific reports
- Correlation analysis between methods

**Resource Requirements**:
- LARGE to XLARGE node (running multiple profilers)
- Higher memory for MetaPhlAn and mOTUs
- Longer runtime (multiple profilers in sequence)

**Implementation Notes**:
- Requires databases for all profilers
- Most computationally intensive use case
- Best for research validation, not routine profiling
- May need to run profilers sequentially rather than in parallel due to memory

---

## Additional Use Cases (Lower Priority)

### Use Case 4: Ancient DNA Metagenomic Profiling (P2)
- Taxonomic profiling of archaeological/paleontological samples
- Requires damage-aware profiling tools
- Special preprocessing for ancient DNA damage patterns

### Use Case 5: Environmental Metagenomics (Soil/Water) (P2)
- Broad taxonomic profiling of environmental samples
- High diversity, many novel organisms
- May benefit from multiple profilers

### Use Case 6: Food Microbiome Analysis (P2)
- Quality control and authentication of food products
- Contamination detection
- Fermentation monitoring

---

## Database Considerations

All taxprofiler use cases require pre-built databases. Common options:

### Kraken2 Databases:
- **Standard DB** (~50GB): Archaea, bacteria, viruses, human, UniVec_Core
- **PlusPF DB** (~75GB): Standard + protozoa and fungi
- **Custom DB**: User-built for specific applications

### MetaPhlAn Databases:
- **mpa_vJan21_CHOCOPhlAnSGB** (latest): ~20GB
- Pre-built marker gene databases from MetaPhlAn team

### mOTUs Databases:
- **mOTUs v3**: Pre-built reference database
- ~5GB download

### Test Databases:
- nf-core test-datasets provides miniature databases for testing
- Not suitable for real analysis but perfect for validation

---

## Implementation Recommendations

**Start with**: Use Case 1 (Microbiome Profiling with Kraken2)
- Most common use case
- Single profiler (simpler to test)
- Well-established tool
- Fast execution
- Good nf-core test data available

**Second**: Use Case 2 (Clinical Pathogen Detection)
- High biological impact
- Similar to Use Case 1 but with host removal
- Can reuse much of the configuration

**Third**: Use Case 3 (Multi-Tool Profiling)
- More complex (multiple profilers)
- Higher resource requirements
- Best after gaining experience with single profilers

---

## Success Criteria

An app is considered successful when:
- ✅ Completes with nf-core test data on XSMALL node
- ✅ Produces expected taxonomic classification outputs
- ✅ Generates quality control reports
- ✅ Output format is suitable for downstream analysis
- ✅ Runtime is reasonable for data size
- ✅ Clear documentation for database requirements