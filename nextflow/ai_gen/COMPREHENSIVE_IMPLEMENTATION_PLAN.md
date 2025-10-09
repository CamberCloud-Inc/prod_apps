# Comprehensive nf-core Pipeline Implementation Plan

**Date**: September 30, 2025
**Current Status**: 44 pipelines implemented (38 unique + 6 variants)
**Target**: 139 nf-core pipelines + multiple biological use case variants
**Missing**: 101 pipelines

---

## Implementation Strategy

### Goal
Implement **ALL 139 nf-core pipelines** with **multiple biological use case variants** where applicable, creating a comprehensive bioinformatics platform covering:
- Simple, domain-specific use cases (cancer, immunology, microbiology, etc.)
- Different experimental designs (case-control, time-series, paired samples)
- Various organism types (human, mouse, bacteria, plants, etc.)
- Different data types and sequencing platforms

### Approach
1. **Batch Implementation**: Groups of 10-15 pipelines per commit
2. **Use Case Variants**: Create 2-5 variants per major pipeline based on common biological applications
3. **Clear Naming**: App names should describe the specific biological use case
4. **Documentation**: Each app includes comprehensive scientific context

---

## Missing Pipelines (101 total)

### Category 1: HIGH PRIORITY - Core Genomics/Transcriptomics (15 pipelines)

**Major Research Impact Pipelines:**

1. **rnasplice** - Alternative splicing analysis
   - **Variants needed**:
     - Disease splicing analysis (cancer, neurological disorders)
     - Drug response splicing changes
     - Developmental splicing programs

2. **riboseq** - Ribosome profiling / translational regulation
   - **Variants needed**:
     - Translation efficiency analysis
     - uORF detection
     - Stress response translation

3. **circrna** - Circular RNA identification
   - **Variants needed**:
     - circRNA biomarker discovery (cancer)
     - circRNA-miRNA sponge analysis
     - Novel circRNA annotation

4. **nascent** - Nascent RNA analysis (PRO-seq, GRO-seq)
   - **Variants needed**:
     - Transcription dynamics
     - Enhancer activity profiling
     - Pause-release analysis

5. **smartseq2** - Smart-seq2 single-cell RNA-seq
   - **Variants needed**:
     - Full-length transcript analysis
     - Isoform-level scRNA-seq
     - Low-input samples

6. **scnanoseq** - Single-cell long-read RNA-seq
   - **Variants needed**:
     - sc-IsoSeq analysis
     - Full-length transcript per cell
     - Isoform diversity in cell types

7. **slamseq** - SLAM-seq (metabolic RNA labeling)
   - **Variants needed**:
     - RNA stability/degradation
     - New vs old RNA quantification
     - Kinetic modeling

8. **cageseq** - CAGE-seq (5' transcript mapping)
   - **Variants needed**:
     - TSS annotation
     - Promoter usage analysis
     - Alternative promoters

9. **mnaseseq** - MNase-seq (nucleosome positioning)
   - **Variants needed**:
     - Nucleosome occupancy
     - Chromatin remodeling
     - TF-nucleosome competition

10. **hicar** - HiCAR (chromatin accessibility + contacts)
    - **Variants needed**:
      - Enhancer-promoter loops with accessibility
      - 3D genome + epigenome
      - Cell-type specific architecture

11. **deepvariant** - Google DeepVariant (ML-based variant calling)
    - **Variants needed**:
      - Clinical WGS variant calling
      - PacBio long-read variants
      - Challenging regions (HLA, centromeres)

12. **pacvar** - PacBio long-read variant calling
    - **Variants needed**:
      - Structural variant detection
      - Repeat expansion analysis
      - Phased variants

13. **rnadnavar** - Combined RNA+DNA variant calling
    - **Variants needed**:
      - RNA editing detection
      - Allele-specific expression validation
      - Tumor RNA+DNA matched samples

14. **longraredisease** - Long-read rare disease analysis
    - **Variants needed**:
      - Diagnostic WGS
      - Repeat expansion disorders
      - Structural variant diseases

15. **oncoanalyser** - Cancer genome analysis
    - **Variants needed**:
      - Tumor-normal somatic variant calling
      - Driver mutation detection
      - CNV + SV comprehensive analysis

---

### Category 2: MEDIUM-HIGH PRIORITY - Specialized Genomics (18 pipelines)

16. **gwas** - Genome-wide association studies
17. **phaseimpute** - Genotype phasing and imputation
18. **hgtseq** - Horizontal gene transfer detection
19. **crisprvar** - CRISPR variant analysis
20. **bactmap** - Bacterial variant mapping
21. **pathogensurveillance** - Pathogen genomic surveillance
22. **variantbenchmarking** - Variant calling benchmarking
23. **variantcatalogue** - Variant catalog creation
24. **variantprioritization** - Clinical variant prioritization
25. **rarevariantburden** - Rare variant burden testing
26. **alleleexpression** - Allele-specific expression
27. **readsimulator** - NGS read simulation
28. **seqinspector** - Sequencing QC inspector
29. **tbanalyzer** - Tuberculosis genome analysis
30. **sammyseq** - SAMMY-seq analysis
31. **ssds** - SSDS (single-stranded DNA sequencing)
32. **stableexpression** - Stable gene expression analysis
33. **radseq** - RAD-seq analysis

---

### Category 3: MEDIUM PRIORITY - Epigenomics & Chromatin (10 pipelines)

34. **methylarray** - Methylation array analysis (450K, EPIC)
    - **Variants needed**:
      - Clinical EWAS
      - Age prediction (epigenetic clock)
      - Cell-type deconvolution

35. **methylong** - Long-read methylation (PacBio, Nanopore)
    - **Variants needed**:
      - 5mC + 5hmC detection
      - Allele-specific methylation
      - Phased methylation

36. **tfactivity** - Transcription factor activity inference
    - **Variants needed**:
      - TF regulon analysis
      - ChIP-seq + RNA-seq integration
      - Master regulator discovery

37. **epitopeprediction** - T-cell epitope prediction
38. **mhcquant** - MHC peptide quantification (immunopeptidomics)
39. **imcyto** - Imaging mass cytometry
40. **cellpainting** - Cell Painting image analysis
41. **molkart** - Spatial multi-omics
42. **pixelator** - Spatial proteomics (Pixelator)
43. **spinningjenny** - Spatial transcriptomics workflow

---

### Category 4: MEDIUM PRIORITY - Metagenomics & Microbiology (15 pipelines)

44. **viralmetagenome** - Viral metagenome assembly
    - **Variants needed**:
      - Viral discovery from clinical samples
      - Environmental virome
      - Prophage detection

45. **viralintegration** - Viral integration site detection
    - **Variants needed**:
      - HPV integration in cancer
      - HBV integration
      - Retroviral integration

46. **coproid** - Ancient DNA from coprolites
47. **detaxizer** - Taxonomic contamination removal
48. **metaboigniter** - Metabolomics workflow
49. **metapep** - Metaproteomic analysis
50. **mitodetect** - Mitochondrial variant detection
51. **liverctanalysis** - Liver CT image analysis
52. **pgdb** - Prokaryotic genome database creation
53. **proteinannotator** - Protein annotation
54. **proteinfamilies** - Protein family classification
55. **genomeannotator** - Genome annotation
56. **genomeassembler** - Genome assembly
57. **genomeqc** - Genome quality control
58. **genomeskim** - Genome skimming analysis

---

### Category 5: MEDIUM PRIORITY - Single-Cell & Spatial (8 pipelines)

59. **scflow** - Single-cell RNA-seq workflow
    - **Variants needed**:
      - Cell type annotation
      - Trajectory analysis
      - Multi-sample integration

60. **scdownstream** - Single-cell downstream analysis
    - **Variants needed**:
      - DE analysis between conditions
      - Pseudotime analysis
      - RNA velocity

61. **spatialxe** - Spatial transcriptomics (Xenium)
62. **sopa** - Spatial omics pipeline
63. **mcmicro** - Multiplexed tissue imaging
64. **marsseq** - MARS-seq single-cell
65. **slamseq** - SLAM-seq (already in epigenomics list)
66. **smartseq2** - Smart-seq2 (already listed)

---

### Category 6: MEDIUM PRIORITY - Proteomics & Metabolomics (5 pipelines)

67. **ddamsproteomics** - DDA mass spec proteomics
    - **Variants needed**:
      - TMT isobaric labeling
      - SILAC quantification
      - MaxQuant workflow

68. **diaproteomics** - DIA proteomics (alternative to quantms)
69. **mhcquant** - MHC peptides (already listed above)
70. **metapep** - Metaproteomics (already listed)
71. **metaboigniter** - Metabolomics (already listed)

---

### Category 7: LOW-MEDIUM PRIORITY - Specialized Applications (20 pipelines)

72. **callingcards** - Calling Cards TF binding
73. **drugresponseeval** - Drug response evaluation
74. **omicsgenetraitassociation** - Multi-omics GWAS
75. **diseasemodulediscovery** - Disease module networks
76. **evexplorer** - Evolutionary analysis
77. **tumourevo** - Tumor evolution analysis
78. **troughgraph** - Tumor heterogeneity
79. **drop** - Detection of RNA Outliers Pipeline
80. **lncpipe** - Long non-coding RNA analysis
81. **reportho** - Ortholog detection
82. **phyloplace** - Phylogenetic placement
83. **multiplesequencealign** - Multiple sequence alignment
84. **pairgenomealign** - Pairwise genome alignment
85. **rangeland** - Rangeland remote sensing
86. **neutronstar** - Neutron star analysis (astrophysics!)
87. **lsmquant** - Label-free protein quantification
88. **ribomsqc** - Ribosomal profiling QC
89. **panoramaseq** - PANORAMSeq analysis
90. **denovotranscript** - De novo transcriptome assembly
91. **denovohybrid** - Hybrid genome assembly

---

### Category 8: LOW PRIORITY - Utility & Infrastructure (11 pipelines)

92. **bamtofastq** - BAM to FASTQ conversion
93. **fastqrepair** - FASTQ file repair
94. **fastquorum** - FASTQ quality filtering
95. **createpanelrefs** - Create reference panels
96. **createtaxdb** - Create taxonomy databases
97. **references** - Reference genome management
98. **datasync** - Data synchronization
99. **deepmodeloptim** - Deep learning model optimization
100. **demo** - Demo pipeline
101. **abotyper** - Blood group antigen typing (Nanopore)

---

### Special Cases: Already Have Basic Implementation, Need Variants

**rnasplice** (splicevariant): Currently blocked by memory limits, needs implementation
**cutandrun**: Have 1 app, need histone modification variant
**chipseq**: Have 3 apps, could add more (broad domains, etc.)

---

## Implementation Batches

### Batch 1: Core Transcriptomics (Target: 10-12 apps)
**Priority**: HIGHEST - High usage, clear biological applications

1. **rnasplice** (3 variants: disease-splicing, drug-response, developmental)
2. **riboseq** (2 variants: translation-efficiency, stress-response)
3. **circrna** (2 variants: cancer-biomarkers, circRNA-annotation)
4. **nascent** (2 variants: transcription-dynamics, enhancer-activity)
5. **slamseq** (1 variant: RNA-stability)

**Estimated Apps**: 10

---

### Batch 2: Advanced Genomics (Target: 10-12 apps)

6. **deepvariant** (3 variants: clinical-WGS, pacbio-variants, challenging-regions)
7. **pacvar** (2 variants: structural-variants, repeat-expansions)
8. **oncoanalyser** (3 variants: tumor-normal, driver-mutations, CNV-analysis)
9. **longraredisease** (2 variants: diagnostic-WGS, repeat-disorders)

**Estimated Apps**: 10

---

### Batch 3: Single-Cell & Spatial (Target: 12-15 apps)

10. **scflow** (3 variants: cell-type-annotation, trajectory, multi-sample)
11. **scdownstream** (3 variants: DE-analysis, pseudotime, RNA-velocity)
12. **smartseq2** (2 variants: full-length-transcripts, isoform-analysis)
13. **scnanoseq** (2 variants: sc-isoseq, isoform-diversity)
14. **spatialxe** (2 variants: Xenium-analysis, spatial-niches)
15. **sopa** (1 variant: spatial-omics)

**Estimated Apps**: 13

---

### Batch 4: Epigenomics & Regulation (Target: 10-12 apps)

16. **methylarray** (3 variants: clinical-EWAS, epigenetic-clock, cell-deconvolution)
17. **methylong** (2 variants: long-read-methylation, allele-specific)
18. **tfactivity** (2 variants: TF-regulon, master-regulators)
19. **mnaseseq** (2 variants: nucleosome-occupancy, chromatin-remodeling)
20. **hicar** (1 variant: enhancer-promoter-loops)

**Estimated Apps**: 10

---

### Batch 5: Metagenomics & Viromics (Target: 10-12 apps)

21. **viralmetagenome** (3 variants: viral-discovery, environmental-virome, prophage)
22. **viralintegration** (2 variants: HPV-integration, HBV-integration)
23. **bactmap** (2 variants: outbreak-analysis, AMR-tracking)
24. **pathogensurveillance** (2 variants: clinical-surveillance, foodborne)
25. **tbanalyzer** (1 variant: TB-genomics)

**Estimated Apps**: 10

---

### Batch 6: Proteomics & Immunology (Target: 10-12 apps)

26. **ddamsproteomics** (3 variants: TMT-labeling, SILAC, MaxQuant)
27. **diaproteomics** (2 variants: DIA-discovery, DIA-targeted)
28. **mhcquant** (2 variants: immunopeptidomics, neoantigen)
29. **epitopeprediction** (2 variants: vaccine-design, cancer-neoantigens)
30. **imcyto** (1 variant: imaging-mass-cytometry)

**Estimated Apps**: 10

---

### Batch 7: Clinical & Cancer Genomics (Target: 10-12 apps)

31. **gwas** (3 variants: case-control, quantitative-traits, meta-analysis)
32. **phaseimpute** (2 variants: genotype-imputation, haplotype-phasing)
33. **variantprioritization** (2 variants: clinical-germline, cancer-somatic)
34. **tumourevo** (2 variants: tumor-phylogeny, clonal-evolution)
35. **rarevariantburden** (1 variant: rare-disease-burden)

**Estimated Apps**: 10

---

### Batch 8: Specialized Genomics (Target: 12-15 apps)

36. **alleleexpression** (2 variants: ASE-analysis, imprinting)
37. **crisprvar** (2 variants: CRISPR-editing-QC, off-target-analysis)
38. **hgtseq** (1 variant: horizontal-gene-transfer)
39. **rnadnavar** (2 variants: RNA-editing, matched-RNA-DNA)
40. **variantbenchmarking** (1 variant: benchmark-analysis)
41. **variantcatalogue** (1 variant: population-variants)
42. **readsimulator** (1 variant: NGS-simulation)
43. **seqinspector** (1 variant: sequencing-QC)
44. **sammyseq** (1 variant: SAMMY-analysis)

**Estimated Apps**: 12

---

### Batch 9: Spatial & Imaging (Target: 8-10 apps)

45. **cellpainting** (2 variants: phenotypic-profiling, drug-screening)
46. **molkart** (2 variants: spatial-multiomics, tissue-architecture)
47. **pixelator** (2 variants: spatial-proteomics, protein-neighborhoods)
48. **mcmicro** (2 variants: multiplexed-imaging, cell-segmentation)
49. **liverctanalysis** (1 variant: CT-analysis)

**Estimated Apps**: 9

---

### Batch 10: Microbiology & Annotation (Target: 10-12 apps)

50. **coproid** (1 variant: ancient-DNA)
51. **detaxizer** (1 variant: contamination-removal)
52. **metapep** (1 variant: metaproteomics)
53. **pgdb** (1 variant: prokaryotic-genomes)
54. **proteinannotator** (1 variant: protein-annotation)
55. **proteinfamilies** (1 variant: protein-families)
56. **genomeannotator** (2 variants: eukaryote-annotation, prokaryote-annotation)
57. **genomeassembler** (2 variants: short-read-assembly, hybrid-assembly)
58. **genomeqc** (1 variant: genome-QC)
59. **genomeskim** (1 variant: organelle-genomes)

**Estimated Apps**: 11

---

### Batch 11: Specialized Applications (Target: 10-12 apps)

60. **callingcards** (1 variant: TF-binding-calling-cards)
61. **drugresponseeval** (2 variants: drug-screening, pharmacogenomics)
62. **omicsgenetraitassociation** (2 variants: multi-omics-GWAS, integrative-QTL)
63. **diseasemodulediscovery** (1 variant: disease-networks)
64. **evexplorer** (1 variant: molecular-evolution)
65. **troughgraph** (1 variant: tumor-heterogeneity)
66. **drop** (1 variant: RNA-outliers)
67. **lncpipe** (1 variant: lncRNA-discovery)
68. **reportho** (1 variant: orthology)

**Estimated Apps**: 11

---

### Batch 12: Phylogenetics & Alignment (Target: 6-8 apps)

69. **phyloplace** (1 variant: phylogenetic-placement)
70. **multiplesequencealign** (2 variants: protein-MSA, DNA-MSA)
71. **pairgenomealign** (1 variant: synteny-analysis)
72. **denovotranscript** (1 variant: de-novo-transcriptome)
73. **denovohybrid** (1 variant: hybrid-assembly)
74. **ssds** (1 variant: single-strand-DNA-seq)

**Estimated Apps**: 7

---

### Batch 13: Utilities & Special (Target: 10-12 apps)

75. **bamtofastq** (1 variant: BAM-conversion)
76. **fastqrepair** (1 variant: FASTQ-repair)
77. **fastquorum** (1 variant: quality-filtering)
78. **createpanelrefs** (1 variant: reference-panels)
79. **createtaxdb** (1 variant: taxonomy-DB)
80. **references** (1 variant: reference-management)
81. **datasync** (1 variant: data-sync)
82. **deepmodeloptim** (1 variant: ML-optimization)
83. **abotyper** (1 variant: blood-antigens)
84. **stableexpression** (1 variant: housekeeping-genes)
85. **ribomsqc** (1 variant: ribo-profiling-QC)
86. **rangeland** (1 variant: remote-sensing)

**Estimated Apps**: 12

---

### Batch 14: Metabolomics & Quantification (Target: 5-6 apps)

87. **metaboigniter** (2 variants: targeted-metabolomics, untargeted)
88. **lsmquant** (1 variant: label-free-MS)
89. **panoramaseq** (1 variant: panorama-analysis)
90. **radseq** (1 variant: RAD-seq)

**Estimated Apps**: 5

---

## Summary Statistics

### Current Status
- **Implemented**: 44 pipelines (38 unique + 6 variants)
- **Missing**: 101 unique pipelines
- **Total nf-core**: 139 pipelines

### Target With Variants
- **Unique pipelines**: 139
- **Estimated variants**: ~150-200 additional apps
- **Total target apps**: ~290-340 apps

### Implementation Estimate
- **14 batches** of 10-12 apps each
- **~150-170 new apps** from missing pipelines + variants
- **Total platform**: ~210-230 apps (current 61 + new 150-170)

---

## Implementation Priorities

### Tier 1 (Batches 1-3): Core Analysis Tools
- **Transcriptomics**: rnasplice, riboseq, circrna, nascent, slamseq
- **Genomics**: deepvariant, pacvar, oncoanalyser, longraredisease
- **Single-cell**: scflow, scdownstream, smartseq2, scnanoseq
- **Total**: ~33 apps

### Tier 2 (Batches 4-7): Specialized & Clinical
- **Epigenomics**: methylarray, methylong, tfactivity, mnaseseq, hicar
- **Metagenomics**: viralmetagenome, viralintegration, bactmap, pathogensurveillance
- **Proteomics**: ddamsproteomics, diaproteomics, mhcquant, epitopeprediction
- **Clinical**: gwas, phaseimpute, variantprioritization, tumourevo
- **Total**: ~40 apps

### Tier 3 (Batches 8-14): Comprehensive Coverage
- **Specialized genomics**: ~12 apps
- **Spatial & imaging**: ~9 apps
- **Microbiology**: ~11 apps
- **Applications**: ~11 apps
- **Phylogenetics**: ~7 apps
- **Utilities**: ~12 apps
- **Metabolomics**: ~5 apps
- **Total**: ~67 apps

---

## Next Steps

1. ✅ **Identify all 101 missing pipelines**
2. ⏳ **Start Batch 1** (Core Transcriptomics)
3. Implement systematically through all 14 batches
4. Test pipelines where feasible
5. Document comprehensively

**Goal**: Complete comprehensive nf-core coverage on Camber platform with biologically meaningful use case variants.

---

*Plan created: 2025-09-30*
*Target completion: Rolling implementation*
