# Nextflow App Development and Testing Process

This document outlines the strategy for creating biologist-friendly Camber applications from nf-core workflows, with a focus on creating multiple focused apps per pipeline rather than exposing all parameters.

## ⚠️ CRITICAL: Profile Configuration

**DO NOT specify `-profile` in Nextflow commands.** The Camber backend automatically sets `-profile k8s` for all jobs.

❌ **Wrong**: `nextflow run nf-core/pipeline -profile singularity ...`
❌ **Wrong**: `nextflow run nf-core/pipeline -profile test,k8s ...`
✅ **Correct**: `nextflow run nf-core/pipeline --input ${input} -r X.Y.Z`

## Philosophy: One Pipeline → Multiple Purpose-Built Apps

Instead of creating a single complex app with dozens of parameters, create **10+ simplified apps** per nf-core pipeline, each optimized for a specific use case that biologists commonly encounter.

### Benefits of This Approach

**For Biologists:**
- Clear, descriptive app names ("Sarek: Somatic Variant Calling" vs generic "Sarek")
- Minimal decision-making (3-5 parameters vs 50+)
- Pre-configured best practices
- Faster time to results
- Less room for configuration errors

**For Platform:**
- Apps can be discovered by specific use case
- Better analytics on which workflows are actually used
- Easier to optimize resource allocation per use case
- Simpler testing and validation
- More intuitive catalog organization

## Writing Biology-Focused App Descriptions

### Target Audience: Biologists, Not Bioinformaticians

**Key Principles:**

1. **Hide Technical Details**: Don't mention Nextflow, nf-core, or specific bioinformatics tools unless necessary
2. **Focus on Biology**: Emphasize the scientific question, experimental design, and biological insights
3. **Provide Complete Input Instructions**: Tell users exactly how to create required files (especially samplesheets)
4. **Explain Expected Outputs**: Describe results in biological terms, not file formats
5. **Include Link to Advanced Info**: Add one link at the bottom for users who need pipeline details

### App Description Template

Every app should include these sections in the `content` field (HTML format):

```html
<h1>{Analysis Name in Plain Language}</h1>

<h2>What This Analysis Does</h2>
<p>1-2 paragraphs explaining the biological purpose in accessible language</p>

<h2>When To Use This</h2>
<ul>
  <li><strong>Use Case 1:</strong> Description</li>
  <li><strong>Use Case 2:</strong> Description</li>
  <li><strong>Use Case 3:</strong> Description</li>
</ul>

<h2>What You Need</h2>

<h3>1. [Data Type] (File Format)</h3>
<p>Clear description of input data requirements</p>
<ul>
  <li><strong>Source:</strong> Where the data comes from</li>
  <li><strong>Format:</strong> Expected file format</li>
  <li><strong>Quality requirements:</strong> Coverage, depth, etc.</li>
</ul>

<h3>2. Sample Information Sheet (CSV File)</h3>
<p>Create a CSV file with this exact format:</p>
<pre>column1,column2,column3
example_row1,value1,value2
example_row2,value1,value2</pre>

<p><strong>Column Details:</strong></p>
<ul>
  <li><strong>column1:</strong> Detailed explanation of what goes here</li>
  <li><strong>column2:</strong> Detailed explanation with examples</li>
  <li><strong>column3:</strong> Detailed explanation with valid values</li>
</ul>

<p><strong>Important Notes:</strong> Any special requirements or constraints</p>

<h3>3. [Other Required Inputs]</h3>
<p>Explanation of other parameters</p>

<h2>What You'll Get</h2>

<h3>[Output Category 1]</h3>
<ul>
  <li><strong>Result type:</strong> What it means biologically</li>
  <li><strong>Result type:</strong> How to interpret it</li>
</ul>

<h3>[Output Category 2]</h3>
<ul>
  <li>More output descriptions</li>
</ul>

<h2>Expected Analysis Time</h2>
<ul>
  <li><strong>Small dataset:</strong> Time estimate</li>
  <li><strong>Typical dataset:</strong> Time estimate</li>
  <li><strong>Large dataset:</strong> Time estimate</li>
</ul>

<h2>Scientific Background</h2>
<p>Brief explanation of the method/algorithm used (1-2 sentences)</p>

<p><a href='https://nf-co.re/{pipeline}' target='_blank'>Advanced users: See full pipeline documentation</a></p>
```

### Real Example: Single-Cell RNA-seq App

```json
{
  "name": "scrnaseq-10x-v3",
  "title": "Single-Cell Gene Expression Analysis: 10x Genomics",
  "description": "Measure gene expression in thousands of individual cells to discover cell types, states, and rare populations. Analyzes 10x Genomics Chromium data to reveal cellular diversity hidden in bulk tissue samples - essential for understanding development, disease heterogeneity, and tissue organization.",
  "content": "<h1>Single-Cell Gene Expression Analysis</h1><h2>What This Analysis Does</h2><p>This analysis measures which genes are active in each individual cell, revealing the diversity of cell types and states in your tissue sample. Unlike traditional RNA-seq that averages across millions of cells, single-cell analysis shows you exactly which genes are expressed in each cell, allowing you to identify rare cell populations, developmental trajectories, and disease-specific cell states.</p><h2>When To Use This</h2><ul><li><strong>Cell Type Discovery:</strong> Identify and characterize cell populations in complex tissues</li><li><strong>Developmental Biology:</strong> Track cell fate decisions and differentiation pathways</li><li><strong>Disease Research:</strong> Find disease-specific cell states in cancer, inflammation, or neurodegeneration</li><li><strong>Drug Response:</strong> Understand how different cells respond to treatments</li><li><strong>Tissue Architecture:</strong> Map cell-cell communication and tissue organization</li></ul><h2>What You Need</h2><h3>1. 10x Genomics Sequencing Data (FASTQ Files)</h3><p>You need the sequencing files generated after running your samples on a 10x Genomics Chromium instrument:</p><ul><li><strong>Sample source:</strong> Cells captured using 10x Chromium Single Cell 3' v3 kit</li><li><strong>File format:</strong> Paired FASTQ files from Illumina sequencer</li><li><strong>File naming:</strong> Typically *_S1_L001_R1_001.fastq.gz and *_S1_L001_R2_001.fastq.gz</li><li><strong>Read 1:</strong> Contains cell barcode (16bp) and UMI (12bp) - identifies which cell each molecule came from</li><li><strong>Read 2:</strong> Contains the actual RNA sequence (transcript)</li></ul><h3>2. Sample Information Sheet (CSV File)</h3><p>Create a CSV file listing your samples with this exact format:</p><pre>sample,fastq_1,fastq_2,expected_cells\ncontrol_rep1,control_S1_L001_R1_001.fastq.gz,control_S1_L001_R2_001.fastq.gz,5000\ncontrol_rep2,control_S1_L002_R1_001.fastq.gz,control_S1_L002_R2_001.fastq.gz,5000\ntreated_rep1,treated_S1_L001_R1_001.fastq.gz,treated_S1_L001_R2_001.fastq.gz,4500\ntreated_rep2,treated_S1_L002_R1_001.fastq.gz,treated_S1_L002_R2_001.fastq.gz,4500</pre><p><strong>Column Details:</strong></p><ul><li><strong>sample:</strong> A unique name for this sample (e.g., treatment condition, tissue type, replicate number)</li><li><strong>fastq_1:</strong> Path to Read 1 file (contains cell barcodes and UMIs)</li><li><strong>fastq_2:</strong> Path to Read 2 file (contains RNA sequences)</li><li><strong>expected_cells:</strong> Approximate number of cells you loaded (usually 5,000-10,000 for standard 10x). This helps the algorithm distinguish real cells from empty droplets.</li></ul><p><strong>How to find expected_cells:</strong> Check your 10x Genomics loading notes or use the target recovery from your kit (typically 5,000-10,000 cells per channel).</p><h3>3. Reference Genome</h3><p>Choose the genome matching your organism:</p><ul><li><strong>Human samples:</strong> GRCh38 (use this for almost all human studies)</li><li><strong>Mouse samples:</strong> GRCm39 or GRCm38 (mm10) for compatibility</li><li><strong>Other organisms:</strong> Select from available genomes</li></ul><h2>What You'll Get</h2><h3>Gene Expression Matrices</h3><ul><li><strong>Cell x Gene matrix:</strong> Expression level of every gene in every cell</li><li><strong>Filtered cells:</strong> High-quality cells with sufficient RNA content</li><li><strong>Normalized data:</strong> Ready for downstream analysis (clustering, differential expression)</li></ul><h3>Cell Quality Metrics</h3><ul><li><strong>Cells detected:</strong> Number of high-quality cells identified</li><li><strong>Genes per cell:</strong> Complexity of each cell's transcriptome</li><li><strong>UMIs per cell:</strong> Number of RNA molecules captured</li><li><strong>Mitochondrial content:</strong> Indicator of cell stress or damage</li></ul><h3>Analysis-Ready Outputs</h3><ul><li><strong>Seurat objects:</strong> For analysis in R (clustering, UMAP, differential expression)</li><li><strong>AnnData files:</strong> For analysis in Python with Scanpy</li><li><strong>Summary reports:</strong> QC metrics and sample statistics</li></ul><h2>Expected Analysis Time</h2><ul><li><strong>One sample (~5,000 cells):</strong> 2-3 hours</li><li><strong>Multiple samples (4-8 samples):</strong> 4-6 hours</li><li><strong>Large experiment (10+ samples):</strong> 8-12 hours</li></ul><h2>Scientific Background</h2><p>This analysis uses STARsolo for alignment and gene counting, which has been optimized for 10x Genomics data. It identifies individual cells by their unique barcode sequences and counts how many RNA molecules (UMIs) from each gene were captured in each cell. The pipeline follows current best practices for single-cell RNA-seq quality control and normalization.</p><p><a href='https://nf-co.re/scrnaseq' target='_blank'>Advanced users: See full pipeline documentation</a></p>"
}
```

### Key Elements of Good Descriptions

**1. Use Plain Language Titles:**
- ✓ "Cancer Variant Detection: Tumor vs Normal Comparison"
- ✗ "Sarek: Somatic Variant Calling Pipeline"
- ✓ "Single-Cell Gene Expression Analysis"
- ✗ "nf-core/scrnaseq with STARsolo"

**2. Explain Biological Context:**
- Why would a biologist use this?
- What scientific questions does it answer?
- What discoveries can they make?

**3. Provide Complete Samplesheet Instructions:**
- Show exact CSV format with example data
- Explain every column in detail
- Include valid values and constraints
- Explain where to find information (e.g., lane numbers in filename)

**4. Describe Outputs in Biological Terms:**
- ✓ "High-confidence cancer-specific mutations"
- ✗ "Filtered VCF files"
- ✓ "Cell types and gene expression patterns"
- ✗ "AnnData objects with normalized counts"

**5. Set Expectations:**
- How long will it take?
- What quality of data is needed?
- What can go wrong?

**6. Minimal Technical Jargon:**
- Avoid: "BWA-MEM2 alignment with GATK4 preprocessing"
- Use: "Aligns your sequences to the reference genome and prepares them for analysis"
- Exception: When explaining a specific method (e.g., "GATK Mutect2 algorithm")

## Core Strategy

### 1. Identify Common Use Cases Per Pipeline

For each nf-core pipeline, research and identify the 5-15 most common biological questions or experimental setups.

**Example: nf-core/sarek (Variant Calling)**

Common use cases:
1. **Germline variant calling** (single samples)
2. **Somatic variant calling** (tumor/normal pairs)
3. **Trio analysis** (parents + offspring)
4. **Population genomics** (cohort analysis)
5. **Targeted sequencing** (exome/panel)
6. **Whole genome sequencing** (WGS)
7. **RNA variant calling** (from RNA-seq)
8. **Structural variant detection**
9. **Copy number variation analysis**
10. **Mitochondrial variant calling**

**Example: nf-core/rnaseq (RNA Sequencing)**

Common use cases:
1. **Differential expression** (two-group comparison)
2. **Time series analysis** (multiple time points)
3. **Small RNA sequencing** (miRNA, siRNA)
4. **Long-read RNA-seq** (Oxford Nanopore, PacBio)
5. **3' RNA-seq** (Lexogen QuantSeq)
6. **Total RNA-seq** (rRNA depletion)
7. **Poly-A enriched** (standard mRNA-seq)
8. **Strand-specific** (directional libraries)
9. **Allele-specific expression**
10. **Fusion detection**

**Example: nf-core/scrnaseq (Single-Cell RNA-seq)**

Common use cases:
1. **10x Genomics v3** (standard 3' kit)
2. **10x Genomics v2** (older 3' kit)
3. **10x Genomics 5'** (5' gene expression)
4. **Drop-seq protocol**
5. **Smart-seq2** (full-length)
6. **Smart-seq3** (improved full-length)
7. **CITE-seq** (protein + RNA)
8. **Cell hashing** (multiplexing)
9. **Spatial transcriptomics** (10x Visium)
10. **snRNA-seq** (single-nucleus)

### 2. Hardcode Parameters for Each Use Case

For each app, identify:

**Always Hardcoded** (hidden from users):
- Pipeline version (use latest stable)
- Quality control thresholds
- File format options
- Technical parameters biologists shouldn't modify
- Advanced algorithmic settings
- Container/environment settings

**Configurable** (exposed to users):
- Input data (samplesheet, FASTQ files)
- Output directory
- Reference genome/organism
- Sample metadata (e.g., tumor/normal designation)
- Optional: Key biological parameters (e.g., expected cell count)

**Example: "Tumor-Normal Variant Detection" App**

```json
{
  "name": "sarek-somatic-mutect2",
  "title": "Cancer Variant Detection: Tumor vs Normal Comparison",
  "description": "Identify cancer-specific genetic mutations by comparing tumor tissue to matched normal tissue. Detects SNVs (single nucleotide variants) and small insertions/deletions that are present in cancer cells but not in healthy cells - essential for precision oncology, understanding tumor evolution, and identifying therapeutic targets.",
  "content": "<h1>Cancer Variant Detection: Tumor vs Normal Analysis</h1><h2>What This Analysis Does</h2><p>This analysis identifies genetic mutations that are unique to cancer cells by comparing DNA sequencing data from tumor tissue against matched normal (healthy) tissue from the same patient. This reveals which mutations are driving cancer growth versus inherited variants.</p><h2>When To Use This</h2><ul><li><strong>Cancer Research:</strong> Identify driver mutations in tumor samples</li><li><strong>Precision Medicine:</strong> Find actionable mutations for targeted therapy</li><li><strong>Tumor Evolution:</strong> Track how cancer genomes change over time</li><li><strong>Clinical Diagnostics:</strong> Support treatment decisions with genomic evidence</li></ul><h2>What You Need</h2><h3>1. DNA Sequencing Data (FASTQ Files)</h3><p>You need paired-end sequencing files for both tumor and normal samples:</p><ul><li><strong>Tumor sample:</strong> DNA from cancer tissue (biopsy, surgical specimen)</li><li><strong>Normal sample:</strong> DNA from healthy tissue (blood, adjacent normal tissue)</li><li><strong>File format:</strong> FASTQ files (typically named *_R1.fastq.gz and *_R2.fastq.gz)</li><li><strong>Recommended sequencing:</strong> 100-300x coverage for tumor, 30-50x for normal</li></ul><h3>2. Sample Information Sheet (CSV File)</h3><p>Create a CSV file listing your samples with this exact format:</p><pre>patient,sample,status,lane,fastq_1,fastq_2\npatient001,normal_blood,0,L001,normal_R1.fastq.gz,normal_R2.fastq.gz\npatient001,tumor_biopsy,1,L001,tumor_R1.fastq.gz,tumor_R2.fastq.gz\npatient002,normal_blood,0,L001,normal2_R1.fastq.gz,normal2_R2.fastq.gz\npatient002,tumor_biopsy,1,L001,tumor2_R1.fastq.gz,tumor2_R2.fastq.gz</pre><p><strong>Column Details:</strong></p><ul><li><strong>patient:</strong> Unique patient ID (same ID for tumor and normal from same patient)</li><li><strong>sample:</strong> Unique sample name (describe tissue type: tumor_liver, normal_blood, etc.)</li><li><strong>status:</strong> Use <code>0</code> for normal/healthy tissue, <code>1</code> for tumor tissue</li><li><strong>lane:</strong> Sequencing lane (usually L001, L002, etc. - found in your FASTQ filenames)</li><li><strong>fastq_1:</strong> Path to Read 1 file (forward reads, *_R1.fastq.gz)</li><li><strong>fastq_2:</strong> Path to Read 2 file (reverse reads, *_R2.fastq.gz)</li></ul><p><strong>Important:</strong> Each patient must have exactly one normal (status=0) and at least one tumor (status=1) sample for comparison.</p><h3>3. Reference Genome</h3><p>Choose the genome that matches your samples:</p><ul><li><strong>Human cancer studies:</strong> GRCh38/hg38 (recommended for new studies)</li><li><strong>Legacy human data:</strong> GRCh37/hg19 (for compatibility with older datasets)</li><li><strong>Mouse cancer models:</strong> GRCm39/mm39 or GRCm38/mm10</li></ul><h2>What You'll Get</h2><h3>Somatic Variant Calls (VCF Files)</h3><ul><li><strong>Filtered mutations:</strong> High-confidence cancer-specific variants</li><li><strong>Mutation types:</strong> SNVs (point mutations) and small indels (insertions/deletions)</li><li><strong>Annotations:</strong> Gene names, protein effects, population frequencies</li><li><strong>Clinical relevance:</strong> Links to cancer databases (COSMIC, ClinVar)</li></ul><h3>Quality Control Reports</h3><ul><li><strong>Sequencing quality:</strong> Coverage depth, read quality, contamination estimates</li><li><strong>Mutation burden:</strong> Total number of somatic mutations detected</li><li><strong>Validation metrics:</strong> Confidence scores for each variant call</li></ul><h3>Analysis-Ready Outputs</h3><ul><li><strong>VCF files:</strong> Standard format compatible with downstream tools</li><li><strong>MAF files:</strong> Mutation annotation format for cancer genomics tools</li><li><strong>Summary statistics:</strong> Mutation signatures, affected pathways</li></ul><h2>Expected Analysis Time</h2><ul><li><strong>One tumor/normal pair (exome):</strong> 4-8 hours</li><li><strong>One tumor/normal pair (whole genome):</strong> 12-24 hours</li><li><strong>Multiple patients:</strong> Processes pairs in parallel</li></ul><h2>Scientific Background</h2><p>This analysis uses the GATK Mutect2 algorithm, which is specifically designed to detect low-frequency somatic mutations in cancer samples. It accounts for tumor heterogeneity, sequencing artifacts, and germline variation to provide highly accurate somatic variant calls.</p><p><a href='https://nf-co.re/sarek' target='_blank'>Advanced users: See full pipeline documentation</a></p>",
  "imageUrl": "https://sateeshperi.github.io/nextflow_varcal/nextflow/images/nf-core-variantcall_logo_light.png",
  "command": "nextflow run nf-core/sarek --input ${input} --outdir ${output} --tools mutect2 --only_paired_variant_calling true --genome ${genome} -r 3.5.1 -c /etc/mpi/nextflow.camber.config -c sarek-somatic-config.config",
  "engineType": "NEXTFLOW",
  "spec": [
    {
      "type": "Stash File",
      "label": "Sample Information Sheet",
      "name": "input",
      "description": "CSV file listing tumor and normal samples. Required columns: patient, sample, status (0=normal, 1=tumor), lane, fastq_1, fastq_2. Each patient must have one normal and one tumor sample.",
      "required": true
    },
    {
      "type": "Stash File",
      "label": "Output Directory",
      "name": "output",
      "description": "Where to save variant calls and analysis reports",
      "defaultValue": "./cancer-variants-results",
      "required": true
    },
    {
      "type": "Select",
      "label": "Reference Genome",
      "name": "genome",
      "description": "Genome version matching your sequencing data (use GRCh38 for new human studies)",
      "defaultValue": "GRCh38",
      "options": [
        {"label": "Human GRCh38/hg38 (latest, recommended)", "value": "GRCh38"},
        {"label": "Human GRCh37/hg19 (legacy/compatibility)", "value": "GRCh37"},
        {"label": "Mouse GRCm39/mm39 (latest)", "value": "GRCm39"},
        {"label": "Mouse GRCm38/mm10 (legacy)", "value": "GRCm38"}
      ]
    }
  ]
}
```

**Contrast with: "Inherited Variant Detection" App**

```json
{
  "name": "sarek-germline-haplotypecaller",
  "title": "Inherited Genetic Variant Detection",
  "description": "Identify genetic variants inherited from parents that may cause disease or affect traits. Analyzes individual DNA samples to find SNVs and small indels in your genome - useful for rare disease diagnosis, pharmacogenomics, and understanding genetic predisposition to conditions.",
  "content": "<h1>Inherited Genetic Variant Detection</h1><h2>What This Analysis Does</h2><p>This analysis identifies genetic variants that are present in your DNA from birth - inherited from your parents or arising very early in development. Unlike cancer variant detection, this looks at variants across your entire genome that may affect health, disease risk, or drug response.</p><h2>When To Use This</h2><ul><li><strong>Rare Disease Diagnosis:</strong> Find genetic causes of inherited disorders</li><li><strong>Carrier Screening:</strong> Identify variants that could be passed to offspring</li><li><strong>Pharmacogenomics:</strong> Predict drug metabolism and response based on genetics</li><li><strong>Disease Risk Assessment:</strong> Understand genetic predisposition to common diseases</li><li><strong>Population Genetics:</strong> Study genetic diversity and ancestry</li></ul><h2>What You Need</h2><h3>1. DNA Sequencing Data (FASTQ Files)</h3><p>You need paired-end sequencing files from individual samples:</p><ul><li><strong>Sample source:</strong> Blood, saliva, or any tissue (variants are the same in all cells)</li><li><strong>File format:</strong> FASTQ files (typically named *_R1.fastq.gz and *_R2.fastq.gz)</li><li><strong>Recommended sequencing:</strong> 30x coverage for whole genome, 100x for exome</li></ul><h3>2. Sample Information Sheet (CSV File)</h3><p>Create a CSV file listing your samples with this exact format:</p><pre>patient,sample,lane,fastq_1,fastq_2\npatient001,blood_sample,L001,sample1_R1.fastq.gz,sample1_R2.fastq.gz\npatient002,saliva_sample,L001,sample2_R1.fastq.gz,sample2_R2.fastq.gz\npatient003,blood_sample,L001,sample3_R1.fastq.gz,sample3_R2.fastq.gz</pre><p><strong>Column Details:</strong></p><ul><li><strong>patient:</strong> Unique patient or individual ID</li><li><strong>sample:</strong> Unique sample name (can include tissue type or collection info)</li><li><strong>lane:</strong> Sequencing lane (usually L001, L002, etc. - found in your FASTQ filenames)</li><li><strong>fastq_1:</strong> Path to Read 1 file (forward reads, *_R1.fastq.gz)</li><li><strong>fastq_2:</strong> Path to Read 2 file (reverse reads, *_R2.fastq.gz)</li></ul><p><strong>Note:</strong> Unlike tumor/normal analysis, you don't need matched samples - each individual is analyzed independently.</p><h3>3. Reference Genome</h3><p>Choose the genome that matches your species:</p><ul><li><strong>Human studies:</strong> GRCh38/hg38 (recommended for new studies)</li><li><strong>Legacy human data:</strong> GRCh37/hg19 (for compatibility with older datasets or clinical databases)</li><li><strong>Mouse studies:</strong> GRCm39/mm39 or GRCm38/mm10</li></ul><h2>What You'll Get</h2><h3>Germline Variant Calls (VCF Files)</h3><ul><li><strong>SNVs (Single Nucleotide Variants):</strong> Single letter changes in DNA</li><li><strong>Indels:</strong> Small insertions or deletions (up to ~50 bases)</li><li><strong>Quality scores:</strong> Confidence level for each variant call</li><li><strong>Genotypes:</strong> Whether variants are heterozygous (one copy) or homozygous (both copies)</li></ul><h3>Variant Annotations</h3><ul><li><strong>Gene impact:</strong> Which genes are affected and how (missense, nonsense, etc.)</li><li><strong>Clinical significance:</strong> Links to disease databases (ClinVar, OMIM)</li><li><strong>Population frequencies:</strong> How common each variant is (gnomAD database)</li><li><strong>Predictions:</strong> Whether variants are likely pathogenic or benign</li></ul><h3>Quality Reports</h3><ul><li><strong>Sequencing metrics:</strong> Coverage depth, read quality, mapping rates</li><li><strong>Variant statistics:</strong> Total variants found, transition/transversion ratios</li><li><strong>Sample QC:</strong> Contamination estimates, sex verification</li></ul><h2>Expected Analysis Time</h2><ul><li><strong>One exome sample:</strong> 2-4 hours</li><li><strong>One whole genome:</strong> 8-16 hours</li><li><strong>Multiple samples:</strong> Processed in parallel</li></ul><h2>Scientific Background</h2><p>This analysis uses GATK HaplotypeCaller, the gold-standard algorithm for germline variant detection developed by the Broad Institute. It follows GATK Best Practices for accurate identification of inherited genetic variants, with sophisticated filtering to minimize false positives.</p><p><a href='https://nf-co.re/sarek' target='_blank'>Advanced users: See full pipeline documentation</a></p>",
  "imageUrl": "https://sateeshperi.github.io/nextflow_varcal/nextflow/images/nf-core-variantcall_logo_light.png",
  "command": "nextflow run nf-core/sarek --input ${input} --outdir ${output} --tools haplotypecaller --genome ${genome} -r 3.5.1 -c /etc/mpi/nextflow.camber.config -c sarek-germline-config.config",
  "engineType": "NEXTFLOW",
  "spec": [
    {
      "type": "Stash File",
      "label": "Sample Information Sheet",
      "name": "input",
      "description": "CSV file listing individual samples. Required columns: patient, sample, lane, fastq_1, fastq_2. Each row represents one individual to analyze.",
      "required": true
    },
    {
      "type": "Stash File",
      "label": "Output Directory",
      "name": "output",
      "description": "Where to save variant calls and analysis reports",
      "defaultValue": "./germline-variants-results",
      "required": true
    },
    {
      "type": "Select",
      "label": "Reference Genome",
      "name": "genome",
      "description": "Genome version matching your sequencing data (use GRCh38 for new human studies)",
      "defaultValue": "GRCh38",
      "options": [
        {"label": "Human GRCh38/hg38 (latest, recommended)", "value": "GRCh38"},
        {"label": "Human GRCh37/hg19 (legacy/compatibility)", "value": "GRCh37"}
      ]
    }
  ]
}
```

### 3. Directory Organization

Organize apps by **pipeline**, with each use case as a **subdirectory**:

```
nextflow/
├── sarek/
│   ├── germline-haplotypecaller/
│   │   ├── app.json
│   │   ├── sarek-germline-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── somatic-mutect2/
│   │   ├── app.json
│   │   ├── sarek-somatic-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── trio-analysis/
│   │   ├── app.json
│   │   ├── sarek-trio-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── structural-variants-manta/
│   │   ├── app.json
│   │   ├── sarek-sv-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   └── cnv-analysis/
│       ├── app.json
│       ├── sarek-cnv-config.config
│       ├── test_samplesheet.csv
│       └── README.md
│
├── rnaseq/
│   ├── standard-polya/
│   │   ├── app.json
│   │   ├── rnaseq-polya-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── small-rna/
│   │   ├── app.json
│   │   ├── rnaseq-small-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── long-read-nanopore/
│   │   ├── app.json
│   │   ├── rnaseq-nanopore-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   └── fusion-detection/
│       ├── app.json
│       ├── rnaseq-fusion-config.config
│       ├── test_samplesheet.csv
│       └── README.md
│
├── scrnaseq/
│   ├── 10x-v3-standard/
│   │   ├── app.json
│   │   ├── scrnaseq-10xv3-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── 10x-v2-legacy/
│   │   ├── app.json
│   │   ├── scrnaseq-10xv2-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── dropseq/
│   │   ├── app.json
│   │   ├── scrnaseq-dropseq-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   ├── cite-seq/
│   │   ├── app.json
│   │   ├── scrnaseq-cite-config.config
│   │   ├── test_samplesheet.csv
│   │   └── README.md
│   └── spatial-visium/
│       ├── app.json
│       ├── scrnaseq-spatial-config.config
│       ├── test_samplesheet.csv
│       └── README.md
│
└── chipseq/
    ├── histone-marks/
    ├── transcription-factors/
    └── broad-peaks/
```

### 4. Naming Convention

**App Names** (internal identifier):
```
{pipeline}-{usecase}-{tool}
```
Examples:
- `sarek-germline-haplotypecaller`
- `sarek-somatic-mutect2`
- `rnaseq-polya-star`
- `scrnaseq-10xv3-star`

**App Titles** (user-facing):
```
{Pipeline}: {Use Case Description}
```
Examples:
- "Sarek: Germline Variant Calling"
- "Sarek: Somatic Variant Calling (Tumor/Normal)"
- "RNA-seq: Standard mRNA Sequencing (Poly-A)"
- "Single-Cell RNA-seq: 10x Genomics v3"

**Directory Names**:
```
{usecase}-{tool}
```
Examples:
- `germline-haplotypecaller/`
- `somatic-mutect2/`
- `10x-v3-star/`

## Development Workflow

### 1. Research the Pipeline

Before creating apps, thoroughly understand the nf-core pipeline:

```bash
# Clone the pipeline repository
cd ~/git
git clone https://github.com/nf-core/sarek.git
cd sarek

# Review documentation
cat README.md
open docs/usage.md  # Review all parameters

# Check parameter schema
cat nextflow_schema.json | jq '.definitions'

# Review example samplesheets
ls test_data/
```

**Key Questions to Answer:**
- What are the main tools/algorithms available?
- What biological questions does each tool answer?
- What are the most commonly used parameter combinations?
- What parameters are critical vs optional?
- What are sensible defaults?
- What resource requirements exist?

### 2. Create Use Case Apps

For each identified use case:

#### Step 1: Create Directory Structure
```bash
cd /Users/david/git/prod_apps/nextflow
mkdir -p sarek/germline-haplotypecaller
cd sarek/germline-haplotypecaller
```

#### Step 2: Create Custom Configuration File

Create `{pipeline}-{usecase}-config.config` with:
- Resource requirements optimized for the use case
- Container settings (Singularity, not Docker)
- Any technical parameters specific to the use case

**Example: `sarek-germline-config.config`**
```groovy
// Optimized configuration for germline variant calling

process {
  // Standard processes
  withLabel:process_low {
    cpus   = { 2     * task.attempt }
    memory = { 12.GB * task.attempt }
    time   = { 4.h   * task.attempt }
  }

  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }

  withLabel:process_high {
    cpus   = { 12    * task.attempt }
    memory = { 72.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }

  // HaplotypeCaller specific
  withName:'.*:HAPLOTYPECALLER.*' {
    cpus   = { 4     * task.attempt }
    memory = { 32.GB * task.attempt }
    time   = { 12.h  * task.attempt }
  }
}

// Container configuration
singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false  // Docker not available on Camber
}

// Germline-specific parameters (hardcoded)
params {
  // Best practices for germline calling
  only_paired_variant_calling = false  // Allow single samples

  // QC settings
  trim_fastq = true
  save_trimmed = false

  // Alignment settings
  aligner = 'bwa-mem'
  save_bam_mapped = true

  // Skip unnecessary somatic-only tools
  skip_tools = 'ascat,controlfreec,mutect2,manta_somatic'
}
```

**Example: `sarek-somatic-config.config`**
```groovy
// Optimized configuration for somatic variant calling

process {
  withLabel:process_low {
    cpus   = { 2     * task.attempt }
    memory = { 12.GB * task.attempt }
    time   = { 4.h   * task.attempt }
  }

  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }

  withLabel:process_high {
    cpus   = { 12    * task.attempt }
    memory = { 72.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }

  // Mutect2 specific - more resources for tumor/normal analysis
  withName:'.*:MUTECT2.*' {
    cpus   = { 6     * task.attempt }
    memory = { 48.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }
}

singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false
}

// Somatic-specific parameters (hardcoded)
params {
  // Require tumor/normal pairs
  only_paired_variant_calling = true

  // QC settings
  trim_fastq = true
  save_trimmed = false

  // Alignment settings
  aligner = 'bwa-mem'
  save_bam_mapped = true

  // Skip germline-only tools
  skip_tools = 'haplotypecaller,freebayes'
}
```

#### Step 3: Create app.json

Follow this template structure:

```json
{
  "name": "{pipeline}-{usecase}-{tool}",
  "title": "{Pipeline}: {User-Friendly Use Case Description}",
  "description": "1-2 sentence description emphasizing the biological question and key method",
  "content": "<HTML content with methodology, use case details, expected outputs>",
  "imageUrl": "https://url-to-pipeline-logo.png",
  "command": "nextflow run nf-core/{pipeline} --input ${input} --outdir ${output} --genome ${genome} --tools {tool} -r {version} -c /etc/mpi/nextflow.camber.config -c {pipeline}-{usecase}-config.config",
  "engineType": "NEXTFLOW",
  "jobConfig": [
    {
      "type": "Select",
      "label": "System Size",
      "name": "system_size",
      "hidden": true,
      "options": [
        {
          "label": "Small - Test datasets",
          "value": "small",
          "mapValue": {"nodeSize": "SMALL", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "Medium - 1-5 samples",
          "value": "medium",
          "mapValue": {"nodeSize": "MEDIUM", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "Large - 5-20 samples (Recommended)",
          "value": "large",
          "mapValue": {"nodeSize": "LARGE", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "XLarge - 20+ samples",
          "value": "xlarge",
          "mapValue": {"nodeSize": "XLARGE", "numNodes": 1, "withGpu": false}
        }
      ],
      "defaultValue": "large"
    }
  ],
  "spec": [
    {
      "type": "Stash File",
      "label": "Sample Sheet",
      "name": "input",
      "description": "CSV samplesheet - see documentation for format",
      "required": true
    },
    {
      "type": "Stash File",
      "label": "Output Directory",
      "name": "output",
      "defaultValue": "./results",
      "required": true
    },
    {
      "type": "Select",
      "label": "Reference Genome",
      "name": "genome",
      "description": "Reference genome for alignment and analysis",
      "defaultValue": "GRCh38",
      "options": [
        {"label": "Human GRCh38/hg38", "value": "GRCh38"},
        {"label": "Human GRCh37/hg19", "value": "GRCh37"},
        {"label": "Mouse GRCm39/mm39", "value": "GRCm39"}
      ]
    }
  ],
  "tags": [
    {"name": "genomics", "type": "subfield"},
    {"name": "variant-calling", "type": "task"},
    {"name": "biology", "type": "field"}
  ]
}
```

**Key Elements:**

**Command Construction:**
```bash
nextflow run nf-core/{pipeline} \
  --input ${input} \                          # User provides
  --outdir ${output} \                        # User provides
  --genome ${genome} \                        # User selects
  --tools {hardcoded_tool} \                  # Hardcoded for use case
  -r {pipeline_version} \                     # Hardcoded, use latest stable
  -c /etc/mpi/nextflow.camber.config \       # Platform config (ALWAYS FIRST)
  -c {usecase}-config.config                  # Custom config (SECOND)
```

**Configuration Order Matters:**
1. Platform config (`/etc/mpi/nextflow.camber.config`) - MUST be first
2. Custom use-case config - overrides and adds to platform config
3. Built-in profiles (e.g., `-profile test`) - if needed for testing

**System Size Guidelines:**
- **SMALL**: Test datasets, quick validation (<1GB data)
- **MEDIUM**: 1-5 samples, exome sequencing, targeted panels
- **LARGE**: 5-20 samples, whole genome, most production use (RECOMMENDED)
- **XLARGE**: 20+ samples, large cohorts, population studies

#### Step 4: Create Test Samplesheet

Create `test_samplesheet.csv` using the nf-core test datasets or minimal examples:

**Germline Example:**
```csv
patient,sample,lane,fastq_1,fastq_2
patient1,sample1,lane1,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R2.fastq.gz
patient2,sample2,lane1,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample2_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample2_R2.fastq.gz
```

**Somatic Example:**
```csv
patient,sample,status,lane,fastq_1,fastq_2
patient1,normal,0,lane1,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/normal_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/normal_R2.fastq.gz
patient1,tumor,1,lane1,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/tumor_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/tumor_R2.fastq.gz
```

#### Step 5: Create README.md

Document the use case, expected inputs, and outputs:

```markdown
# Sarek: Germline Variant Calling

## Use Case
Detect inherited genetic variants in individual samples using GATK HaplotypeCaller with GATK best practices.

## When to Use This App
- You have DNA sequencing data from individual samples (not tumor/normal pairs)
- You want to identify SNPs and small indels
- You're studying inherited diseases, population genetics, or rare variants
- You need clinical-grade variant calling

## Input Requirements

### Sample Sheet Format
CSV file with columns: `patient, sample, lane, fastq_1, fastq_2`

Example:
\`\`\`csv
patient,sample,lane,fastq_1,fastq_2
patient1,sample1,lane1,/path/to/sample1_R1.fastq.gz,/path/to/sample1_R2.fastq.gz
patient2,sample2,lane1,/path/to/sample2_R1.fastq.gz,/path/to/sample2_R2.fastq.gz
\`\`\`

### Data Requirements
- Paired-end Illumina sequencing data
- FASTQ format (gzipped or uncompressed)
- Human, mouse, or other supported organism
- Recommended: 30x coverage for WGS, 100x for exome

## Parameters

**Input**: Sample sheet (CSV file)
**Output Directory**: Where results will be stored
**Reference Genome**: Choose appropriate organism and build

## Outputs

### Variant Calls
- `{sample}.vcf.gz` - Germline variants in VCF format
- `{sample}.vcf.gz.tbi` - VCF index files

### Quality Control
- `multiqc_report.html` - Comprehensive QC report
- BAM files with alignments
- Quality metrics and statistics

### Annotation
- Annotated VCF files with gene names, functional predictions
- Filtering statistics

## Expected Runtime
- **Test data**: ~10 minutes
- **Exome (1 sample)**: ~2-4 hours
- **WGS (1 sample)**: ~8-16 hours
- **Multiple samples**: Scales linearly

## Resource Recommendations
- **Test datasets**: SMALL (8 CPUs, 30GB RAM)
- **1-5 exomes**: MEDIUM (32 CPUs, 120GB RAM)
- **1-5 WGS or 5-20 exomes**: LARGE (64 CPUs, 360GB RAM) ✓ Recommended
- **Large cohorts**: XLARGE (96 CPUs, 540GB RAM)

## Testing

\`\`\`bash
# Upload test samplesheet
camber stash cp test_samplesheet.csv stash://username/

# Run with test data
camber app run sarek-germline-haplotypecaller \\
  --input input="stash://username/test_samplesheet.csv" \\
  --input output="stash://username/results" \\
  --input genome="GRCh38"

# Monitor job
camber job get {job-id}
camber job logs {job-id}
\`\`\`

## References
- [nf-core/sarek documentation](https://nf-co.re/sarek)
- [GATK Best Practices](https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices-Workflows)
```

### 3. Push Apps to Camber

Once an app is ready:

```bash
cd /Users/david/git/prod_apps/nextflow/sarek/germline-haplotypecaller

# Create the app (first time)
camber app create --file app.json

# Update existing app (subsequent changes)
camber app delete sarek-germline-haplotypecaller && \\
  camber app create --file app.json
```

## Testing Workflow

### Preparation

```bash
# Navigate to app directory
cd /Users/david/git/prod_apps/nextflow/sarek/germline-haplotypecaller

# Upload test files to stash
camber stash cp test_samplesheet.csv stash://username/test-data/
camber stash cp sarek-germline-config.config stash://username/test-data/

# Verify upload
camber stash ls test-data/
```

### Test Execution

```bash
# Run with test data
camber app run sarek-germline-haplotypecaller \\
  --input input="stash://username/test-data/test_samplesheet.csv" \\
  --input output="stash://username/results-germline" \\
  --input genome="GRCh38"

# Note the Job ID from output
# Job ID: 4567
```

### Monitoring

```bash
# Check job status (repeat until COMPLETED or FAILED)
camber job get 4567

# Expected status progression:
# PENDING → RUNNING → COMPLETED (success)
# or
# PENDING → RUNNING → FAILED (error)

# View logs in real-time
camber job logs 4567

# Monitor continuously (checks every 30 seconds)
watch -n 30 "camber job get 4567"
```

### Verification

```bash
# Check outputs were created
camber stash ls results-germline/

# Expected outputs:
# - VCF files with variants
# - BAM alignment files
# - MultiQC report
# - Pipeline execution report

# Download key results for inspection
camber stash cp stash://username/results-germline/multiqc_report.html ./
open multiqc_report.html
```

### Troubleshooting Failed Jobs

```bash
# View full error logs
camber job logs 4567 > job_error.log

# Common issues:

# 1. Container/Docker errors
# Error: "docker: command not found"
# Fix: Ensure config has docker.enabled = false and singularity.enabled = true

# 2. Resource allocation errors
# Error: "OutOfMemoryError" or process killed
# Fix: Increase nodeSize in jobConfig or adjust process resources in config file

# 3. Input file not found
# Error: "No such file" or "Cannot find input"
# Fix: Verify stash paths, ensure files uploaded correctly

# 4. Parameter validation errors
# Error: "Invalid parameter" or schema validation failed
# Fix: Check parameter names match pipeline expectations

# Debug strategy:
# 1. Check pipeline version is correct (-r flag)
# 2. Verify config file syntax (proper Groovy/Nextflow format)
# 3. Test with nf-core test data first (proven to work)
# 4. Compare working scrnaseq example configuration
```

## Parameter Selection Strategy

### Research Best Practices

For each pipeline, consult:

1. **nf-core Documentation**
   - Official usage docs
   - Parameter descriptions
   - Example configurations

2. **Scientific Literature**
   - Tool-specific papers
   - Benchmark studies
   - Method comparison papers

3. **Community Resources**
   - nf-core Slack channels
   - Bioinformatics forums (Biostars, SEQanswers)
   - GitHub issues and discussions

4. **Vendor Recommendations**
   - 10x Genomics documentation (for scRNA-seq)
   - Illumina protocols
   - Kit manufacturer guidelines

### Parameter Labels and Descriptions for Biologists

When defining parameters in the `spec` section, use biology-focused language:

**Bad (Technical):**
```json
{
  "type": "Stash File",
  "label": "Input Samplesheet",
  "name": "input",
  "description": "CSV file following nf-core schema with fastq paths"
}
```

**Good (Biology-Focused):**
```json
{
  "type": "Stash File",
  "label": "Sample Information Sheet",
  "name": "input",
  "description": "CSV file listing your samples with sequencing files. Required columns: patient, sample, status (0=normal, 1=tumor), lane, fastq_1, fastq_2. Each patient needs one normal and one tumor sample."
}
```

**More Examples:**

**Reference Genome Parameter:**
```json
{
  "type": "Select",
  "label": "Reference Genome",
  "name": "genome",
  "description": "Genome version matching your sequencing data. Use GRCh38 for new human studies, GRCh37 for compatibility with older clinical databases.",
  "defaultValue": "GRCh38",
  "options": [
    {"label": "Human GRCh38/hg38 (latest, recommended)", "value": "GRCh38"},
    {"label": "Human GRCh37/hg19 (legacy/compatibility)", "value": "GRCh37"},
    {"label": "Mouse GRCm39/mm39 (latest)", "value": "GRCm39"}
  ]
}
```

**Expected Cells Parameter (Single-Cell):**
```json
{
  "type": "Input",
  "label": "Expected Number of Cells",
  "name": "expected_cells",
  "description": "Approximate number of cells you loaded into the 10x Chromium chip (typically 5,000-10,000). Check your lab notes from the day you ran the samples. This helps distinguish real cells from empty droplets.",
  "defaultValue": "5000"
}
```

**Output Directory Parameter:**
```json
{
  "type": "Stash File",
  "label": "Output Directory",
  "name": "output",
  "description": "Where to save your variant calls, quality reports, and analysis files. Results will be organized in subfolders by analysis type.",
  "defaultValue": "./variant-calling-results"
}
```

**Strandedness Parameter (RNA-seq):**
```json
{
  "type": "Select",
  "label": "Library Strandedness",
  "name": "strandedness",
  "description": "Whether your RNA-seq library preserves information about which DNA strand the RNA came from. Check your library prep kit: most modern kits are 'reverse' stranded. If unsure, choose 'auto' to detect automatically.",
  "defaultValue": "auto",
  "options": [
    {"label": "Auto-detect (recommended if unsure)", "value": "auto"},
    {"label": "Reverse stranded (most Illumina kits)", "value": "reverse"},
    {"label": "Forward stranded (some older kits)", "value": "forward"},
    {"label": "Unstranded (older libraries)", "value": "unstranded"}
  ]
}
```

### Categories of Parameters

**Always Expose to Users:**
- Input data paths
- Output directory
- Reference genome/organism
- Sample metadata crucial for analysis

**Usually Expose:**
- Key biological parameters (e.g., expected cells in scRNA-seq)
- Quality filtering thresholds if commonly adjusted
- Tool selection if multiple equally valid options exist

**Rarely Expose:**
- Technical parameters (thread counts, memory limits)
- File formats (use best practice defaults)
- Advanced algorithmic settings
- QC parameters (use validated defaults)

**Never Expose:**
- Pipeline version (hardcode latest stable)
- Container settings
- Platform-specific configurations
- Deprecated parameters

### Common Parameter Patterns

**Reference Genome Selection:**
```json
{
  "type": "Select",
  "label": "Reference Genome",
  "name": "genome",
  "defaultValue": "GRCh38",
  "options": [
    {"label": "Human GRCh38 (latest)", "value": "GRCh38"},
    {"label": "Human GRCh37 (legacy)", "value": "GRCh37"},
    {"label": "Mouse GRCm39 (latest)", "value": "GRCm39"},
    {"label": "Mouse GRCm38 (mm10)", "value": "GRCm38"}
  ]
}
```

**Tool Selection (when appropriate):**
```json
{
  "type": "Select",
  "label": "Alignment Method",
  "name": "aligner",
  "description": "Choose aligner based on your needs: STAR (fast, standard), HISAT2 (memory-efficient), Salmon (pseudoalignment)",
  "defaultValue": "star",
  "options": [
    {"label": "STAR - Standard RNA-seq aligner", "value": "star"},
    {"label": "HISAT2 - Memory efficient", "value": "hisat2"},
    {"label": "Salmon - Pseudoalignment (fastest)", "value": "salmon"}
  ]
}
```

**Expected Cell Count (scRNA-seq):**
```json
{
  "type": "Input",
  "label": "Expected Number of Cells",
  "name": "expected_cells",
  "description": "Approximate number of cells captured (helps optimize cell calling)",
  "defaultValue": "5000",
  "required": false
}
```

## App Configuration Best Practices

### Command Structure

**CRITICAL**: DO NOT specify `-profile` in commands. The Camber backend automatically sets `-profile k8s` for all Nextflow jobs.

**Template:**
```bash
nextflow run nf-core/{pipeline} \\
  --input ${input} \\
  --outdir ${output} \\
  --genome ${genome} \\
  --{key_param} {value} \\          # Use case specific
  --{another_param} {value} \\      # Use case specific
  -r {version}                      # Hardcoded
```

**Note**: All parameters (both user-provided like `${input}` and hardcoded like `--tools mutect2`) go directly in the command. Do NOT create separate config files unless absolutely necessary for complex resource tuning.

**Real Example (Sarek Somatic):**
```bash
nextflow run nf-core/sarek \\
  --input ${input} \\
  --outdir ${output} \\
  --genome ${genome} \\
  --tools mutect2 \\
  --only_paired_variant_calling true \\
  -r 3.5.1
```

### Config File Structure

**Essential Components:**

```groovy
// 1. Process Resource Allocation
process {
  // Label-based (standard)
  withLabel:process_low {
    cpus   = { 2     * task.attempt }
    memory = { 12.GB * task.attempt }
    time   = { 4.h   * task.attempt }
  }

  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }

  withLabel:process_high {
    cpus   = { 12    * task.attempt }
    memory = { 72.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }

  // Name-based (specific processes)
  withName:'.*:SPECIFIC_PROCESS.*' {
    cpus   = { 8     * task.attempt }
    memory = { 48.GB * task.attempt }
    time   = { 12.h  * task.attempt }
  }
}

// 2. Container Configuration (CRITICAL)
singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false  // Must be false on Camber
}

// 3. Use-Case Specific Parameters
params {
  // Hardcoded settings optimized for this use case
  parameter1 = value1
  parameter2 = value2

  // Skip irrelevant tools
  skip_tools = 'tool1,tool2'
}

// 4. Retry Strategy (optional)
maxRetries = 3
errorStrategy = { task.attempt < 3 ? 'retry' : 'finish' }
```

### System Size Guidelines by Pipeline

**Variant Calling (Sarek, Germline/Somatic):**
- SMALL (8 CPU, 30GB): Test data only
- MEDIUM (32 CPU, 120GB): 1-3 exomes
- LARGE (64 CPU, 360GB): 1-3 WGS or 5-10 exomes ✓ Default
- XLARGE (96 CPU, 540GB): Large cohorts (20+ samples)

**RNA-seq (nf-core/rnaseq):**
- SMALL (8 CPU, 30GB): Test data
- MEDIUM (32 CPU, 120GB): 1-10 samples ✓ Default
- LARGE (64 CPU, 360GB): 10-50 samples
- XLARGE (96 CPU, 540GB): 50+ samples

**Single-Cell RNA-seq (nf-core/scrnaseq):**
- MEDIUM (32 CPU, 180GB): Test data or small experiments (<5k cells)
- LARGE (64 CPU, 360GB): Standard experiments (5-20k cells) ✓ Default
- XLARGE (96 CPU, 540GB): Large experiments (20k+ cells)

**ChIP-seq (nf-core/chipseq):**
- SMALL (8 CPU, 30GB): Test data
- MEDIUM (32 CPU, 120GB): 1-10 samples ✓ Default
- LARGE (64 CPU, 360GB): 10-30 samples

**ATAC-seq (nf-core/atacseq):**
- SMALL (8 CPU, 30GB): Test data
- MEDIUM (32 CPU, 120GB): 1-10 samples ✓ Default
- LARGE (64 CPU, 360GB): 10-30 samples

## Common Nextflow Pitfalls

### 1. Docker vs Singularity
**Problem:** Most nf-core examples use Docker, but Camber requires Singularity

**Solution:** Always include in config:
```groovy
docker { enabled = false }
singularity { enabled = true; autoMounts = true }
```

### 2. Config File Ordering
**Problem:** Configs applied in wrong order can cause issues

**Correct Order:**
```bash
-c /etc/mpi/nextflow.camber.config  # Platform first
-c custom-config.config              # Custom second
```

### 3. Profile Conflicts
**Problem:** Using `-profile docker` or `-profile test,docker` fails

**Solution:** Use platform-compatible profiles:
```bash
# Good
-profile test
-profile test,k8s

# Bad
-profile test,docker
-profile docker
```

### 4. Resource Overallocation
**Problem:** Requesting more resources than node size provides

**Solution:** Match process resources to jobConfig nodeSize:
```groovy
// For LARGE (64 CPU, 360GB)
withLabel:process_high {
  cpus   = { 12    * task.attempt }  // ✓ Under 64
  memory = { 72.GB * task.attempt }  // ✓ Under 360GB
}

// Bad for LARGE
withLabel:process_high {
  cpus   = { 80    * task.attempt }  // ✗ Over 64
  memory = { 400.GB * task.attempt } // ✗ Over 360GB
}
```

### 5. File Path Issues
**Problem:** Nextflow can't find input files in stash

**Solution:** Ensure samplesheet uses stash:// paths or relative paths:
```csv
# Good - stash paths
sample1,stash://username/data/sample1_R1.fq.gz,stash://username/data/sample1_R2.fq.gz

# Good - relative paths (if files in working directory)
sample1,./sample1_R1.fq.gz,./sample1_R2.fq.gz

# Bad - absolute local paths that don't exist
sample1,/home/user/data/sample1_R1.fq.gz,/home/user/data/sample1_R2.fq.gz
```

## Complete Example: Creating 3 Sarek Apps

### App 1: Germline HaplotypeCaller

```bash
# Create directory
mkdir -p /Users/david/git/prod_apps/nextflow/sarek/germline-haplotypecaller
cd /Users/david/git/prod_apps/nextflow/sarek/germline-haplotypecaller

# Create config file
cat > sarek-germline-config.config << 'EOF'
process {
  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }
  withName:'.*:HAPLOTYPECALLER.*' {
    cpus   = { 4     * task.attempt }
    memory = { 32.GB * task.attempt }
    time   = { 12.h  * task.attempt }
  }
}
singularity { enabled = true; autoMounts = true }
docker { enabled = false }
params {
  only_paired_variant_calling = false
  skip_tools = 'mutect2,ascat,controlfreec'
}
EOF

# Create test samplesheet
cat > test_samplesheet.csv << 'EOF'
patient,sample,lane,fastq_1,fastq_2
test1,sample1,L001,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R2.fastq.gz
EOF

# Create app.json (shown earlier)
# ... create app.json file ...

# Create README.md (shown earlier)
# ... create README.md file ...

# Upload to Camber
camber app create --file app.json
```

### App 2: Somatic Mutect2

```bash
# Create directory
mkdir -p /Users/david/git/prod_apps/nextflow/sarek/somatic-mutect2
cd /Users/david/git/prod_apps/nextflow/sarek/somatic-mutect2

# Create config file
cat > sarek-somatic-config.config << 'EOF'
process {
  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }
  withName:'.*:MUTECT2.*' {
    cpus   = { 6     * task.attempt }
    memory = { 48.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }
}
singularity { enabled = true; autoMounts = true }
docker { enabled = false }
params {
  only_paired_variant_calling = true
  skip_tools = 'haplotypecaller,freebayes'
}
EOF

# Create test samplesheet (tumor/normal pairs)
cat > test_samplesheet.csv << 'EOF'
patient,sample,status,lane,fastq_1,fastq_2
patient1,normal,0,L001,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/normal_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/normal_R2.fastq.gz
patient1,tumor,1,L001,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/tumor_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/somatic/tumor_R2.fastq.gz
EOF

# Create app.json and README.md
# ... create files ...

# Upload to Camber
camber app create --file app.json
```

### App 3: Structural Variants (Manta)

```bash
# Create directory
mkdir -p /Users/david/git/prod_apps/nextflow/sarek/structural-variants-manta
cd /Users/david/git/prod_apps/nextflow/sarek/structural-variants-manta

# Create config file
cat > sarek-sv-config.config << 'EOF'
process {
  withLabel:process_high {
    cpus   = { 12    * task.attempt }
    memory = { 72.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }
  withName:'.*:MANTA.*' {
    cpus   = { 8     * task.attempt }
    memory = { 64.GB * task.attempt }
    time   = { 20.h  * task.attempt }
  }
}
singularity { enabled = true; autoMounts = true }
docker { enabled = false }
params {
  skip_tools = 'haplotypecaller,mutect2,freebayes'
}
EOF

# Create test samplesheet
cat > test_samplesheet.csv << 'EOF'
patient,sample,lane,fastq_1,fastq_2
test1,sample1,L001,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/sarek/testdata/tiny/germline/sample1_R2.fastq.gz
EOF

# Create app.json and README.md
# ... create files ...

# Upload to Camber
camber app create --file app.json
```

## Recommended Apps Per Pipeline

### High Priority Pipelines

**nf-core/sarek** (Variant Calling):
1. ✓ Germline: HaplotypeCaller (single samples)
2. ✓ Somatic: Mutect2 (tumor/normal)
3. Germline: DeepVariant (ML-based)
4. Somatic: Strelka (tumor/normal)
5. Structural Variants: Manta
6. Copy Number: CNVkit
7. Trio Analysis (family-based)
8. Targeted Sequencing (exome/panel)

**nf-core/rnaseq** (RNA Sequencing):
1. ✓ Standard mRNA-seq (poly-A)
2. Small RNA-seq (miRNA)
3. Long-read RNA-seq (Nanopore)
4. Strand-specific RNA-seq
5. 3' RNA-seq (QuantSeq)
6. Total RNA-seq
7. Fusion Detection
8. Allele-specific Expression

**nf-core/scrnaseq** (Single-Cell):
1. ✓ 10x v3 (most common)
2. 10x v2 (legacy)
3. 10x v4 (newest)
4. Drop-seq
5. Smart-seq2
6. Smart-seq3
7. CITE-seq (protein+RNA)
8. Spatial transcriptomics (Visium)

**nf-core/chipseq** (ChIP Sequencing):
1. Transcription Factors (narrow peaks)
2. Histone Marks (broad peaks)
3. ChIP-seq with Input Control
4. ChIP-seq without Input
5. Peak Calling: MACS2
6. Peak Calling: Homer

**nf-core/atacseq** (Chromatin Accessibility):
1. Standard ATAC-seq
2. ATAC-seq with Nucleosome Positioning
3. Single-Cell ATAC-seq

### Medium Priority Pipelines

**nf-core/methylseq** (DNA Methylation):
1. Bisulfite Sequencing (BS-seq)
2. Whole Genome BS-seq
3. Reduced Representation BS-seq (RRBS)

**nf-core/ampliseq** (16S/18S/ITS):
1. 16S rRNA (Bacteria)
2. 18S rRNA (Eukaryotes)
3. ITS (Fungi)

**nf-core/mag** (Metagenomics):
1. ✓ Metagenomic Assembly (standard)
2. Metagenome-Assembled Genomes (MAGs)
3. Taxonomic Classification

## Maintenance and Updates

### Version Management

**Strategy:**
- Use latest stable release for new apps
- Test major version updates before deploying
- Document version in app.json and README

```json
{
  "command": "nextflow run nf-core/sarek ... -r 3.5.1"
}
```

### Updating Apps

When nf-core releases updates:

```bash
# 1. Review changelog
open https://github.com/nf-core/sarek/releases

# 2. Update test locally
cd /Users/david/git/prod_apps/nextflow/sarek/germline-haplotypecaller

# 3. Update app.json version
# Change: -r 3.5.1 to -r 3.6.0

# 4. Test with test data
camber stash cp test_samplesheet.csv stash://username/test/
camber app run sarek-germline-haplotypecaller \\
  --input input="stash://username/test/test_samplesheet.csv" \\
  --input output="stash://username/test-results" \\
  --input genome="GRCh38"

# 5. Verify success
camber job get {job-id}
camber job logs {job-id}

# 6. If successful, update production app
camber app delete sarek-germline-haplotypecaller
camber app create --file app.json

# 7. Update README with version notes
```

### Monitoring Usage

Track which apps are most used to prioritize improvements:

```bash
# Check recent jobs for an app
camber job list | grep sarek-germline

# Review feedback from users
# (platform-specific mechanism)
```

## Success Criteria

### App is Ready When:
- [ ] Runs successfully on test data
- [ ] Produces expected outputs
- [ ] Completes within reasonable time
- [ ] Config file optimizes resources
- [ ] Documentation is clear and complete
- [ ] Samplesheet format is documented with examples
- [ ] Parameters are minimal but sufficient
- [ ] Use case is clearly explained
- [ ] Error messages are interpretable

### Platform is Successful When:
- [ ] 10+ apps per major pipeline
- [ ] Apps cover 80% of common use cases
- [ ] Users can find relevant app by biological question
- [ ] Average parameters per app: 3-5 (not 20+)
- [ ] Test-to-production workflow is smooth
- [ ] Resource allocation is appropriate
- [ ] User feedback is positive

## Additional Resources

- [nf-core pipelines](https://nf-co.re/pipelines)
- [Nextflow patterns](https://nextflow-io.github.io/patterns/)
- [nf-core configs](https://github.com/nf-core/configs)
- [Camber documentation](https://docs.camber.cloud)