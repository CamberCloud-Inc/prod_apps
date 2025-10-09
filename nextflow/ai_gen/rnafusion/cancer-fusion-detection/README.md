# Gene Fusion Detection for Cancer RNA-seq

**App Name**: `rnafusion-cancer-detection`

**Pipeline**: nf-core/rnafusion v4.0.0

**Use Case**: Detect oncogenic fusion genes in tumor RNA-seq data for precision cancer medicine

---

## Overview

This app identifies gene fusions (chimeric transcripts resulting from chromosomal rearrangements) in tumor RNA sequencing data. Gene fusions are critical biomarkers in cancer that can:

1. **Drive oncogenesis** - Create constitutively active kinases or aberrant transcription factors
2. **Guide therapy selection** - Match patients to targeted therapies (e.g., ALK inhibitors for ALK fusions)
3. **Confirm diagnosis** - Diagnostic fusions define cancer subtypes (e.g., EWS-FLI1 in Ewing sarcoma)
4. **Predict prognosis** - Certain fusions indicate favorable or poor outcomes

The pipeline uses three complementary fusion detection algorithms (STAR-Fusion, arriba, FusionCatcher) to maximize sensitivity and specificity through consensus calling.

---

## Input Requirements

### Sample Sheet Format

CSV file with the following columns:

| Column | Required | Description |
|--------|----------|-------------|
| `sample` | Yes | Unique sample identifier (no spaces) |
| `fastq_1` | Yes | Path to Read 1 FASTQ file (must be .fastq.gz or .fq.gz) |
| `fastq_2` | No | Path to Read 2 FASTQ file (leave empty for single-end, but paired-end strongly recommended) |
| `strandedness` | Yes | Library strandedness: "forward", "reverse", or "unstranded" |

**Example samplesheet.csv**:
```csv
sample,fastq_1,fastq_2,strandedness
Tumor_Patient1,Patient1_R1.fastq.gz,Patient1_R2.fastq.gz,forward
Tumor_Patient2,Patient2_R1.fastq.gz,Patient2_R2.fastq.gz,forward
K562_Control,K562_R1.fastq.gz,K562_R2.fastq.gz,forward
```

**Strandedness values**:
- `forward`: dUTP/NSR method (most common stranded library prep)
- `reverse`: Ligation method (TruSeq stranded)
- `unstranded`: Standard RNA-seq without strand information
- **If unsure**, use `unstranded` (works but slightly less accurate)

### Sequencing Requirements

- **Read type**: Paired-end strongly recommended (single-end works but reduced sensitivity)
- **Read length**: 100bp or 150bp (longer better for spanning fusion breakpoints)
- **Sequencing depth**: 50-100 million paired reads per sample minimum
  - 50M reads: Basic fusion detection
  - 100-200M reads: Comprehensive detection of low-abundance fusions
- **RNA quality**: RIN ≥ 7 for fresh frozen, ≥ 5 acceptable for FFPE
- **Library type**: Standard mRNA-seq (poly-A selection or rRNA depletion)

### Reference Genome

**Important**: This pipeline ONLY supports **GRCh38/hg38** (human genome).
- GRCh37/hg19 is NOT supported
- Non-human organisms are NOT supported

---

## Parameters

### Exposed Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `input` | File | Sample sheet CSV | Required |
| `outdir` | Directory | Output directory for results | `./rnafusion-results` |

### Hardcoded Parameters

The following parameters are optimized for cancer fusion detection and hardcoded in the app:

- **Fusion callers**: All three enabled (`--starfusion --arriba --fusioncatcher`)
- **Reference genome**: GRCh38 (via iGenomes)
- **Transcript assembly**: StringTie enabled
- **Splicing analysis**: CTAT-Splicing enabled
- **Quality filters**: Default stringent filters to minimize false positives
- **Visualization**: All output formats enabled (VCF, TSV, HTML, PDF)

---

## Expected Outputs

### Main Results Directory Structure

```
rnafusion-results/
├── multiqc/
│   └── multiqc_report.html          # Comprehensive QC report
├── star_fusion/
│   └── {sample}.star_fusion.tsv     # STAR-Fusion results per sample
├── arriba/
│   ├── {sample}.fusions.tsv         # arriba fusion calls
│   └── {sample}.pdf                 # arriba fusion visualizations
├── fusioncatcher/
│   └── {sample}.fusioncatcher.txt   # FusionCatcher results
├── fusion_report/
│   ├── fusions.vcf                  # Aggregated VCF of all fusions
│   ├── fusions_report.html          # Interactive HTML report
│   └── fusions_summary.tsv          # Summary table of all fusions
├── stringtie/
│   └── {sample}.transcripts.gtf     # Assembled transcripts
└── ctat_splicing/
    └── {sample}.splicing.tsv        # Splicing aberrations
```

### Key Output Files

**Fusion Gene Results**:
- `fusions.vcf` - Standardized variant call format with all detected fusions
- `fusions_summary.tsv` - Tab-separated table with:
  - Fusion gene names (5' and 3' gene partners)
  - Breakpoint genomic coordinates
  - Supporting read counts
  - In-frame vs out-of-frame prediction
  - Confidence level (detected by which callers)
  - Known oncogenic fusion annotations

**Visualizations**:
- `multiqc_report.html` - Comprehensive QC metrics across all samples
- `fusions_report.html` - Interactive fusion gene browser
- Arriba PDF reports - Fusion diagrams showing gene structure and breakpoints

**Quality Control**:
- FastQC reports for raw reads
- Alignment statistics (STAR mapping rates)
- Fusion caller concordance metrics
- Sample-level quality scores

---

## Interpreting Results

### High Confidence Fusions (Priority)

Prioritize fusions that meet these criteria:

✅ **Detected by 2+ callers** - Consensus increases confidence
✅ **≥10 supporting reads** - Well-supported evidence
✅ **In-frame fusion** - Likely produces functional chimeric protein
✅ **Known oncogenic fusion** - In databases (COSMIC, FusionGDB)
✅ **Cancer gene involved** - Kinases, transcription factors, tumor suppressors

**Examples of high-priority fusions**:
- ALK fusions → Crizotinib/alectinib therapy
- ROS1 fusions → Crizotinib/entrectinib therapy
- RET fusions → Selpercatinib/pralsetinib therapy
- NTRK fusions → Larotrectinib/entrectinib therapy
- BCR-ABL1 → TKI therapy (imatinib, dasatinib)

### Lower Confidence Fusions (Validate)

Exercise caution with fusions that have:

⚠️ **Single caller detection** - May be artifact
⚠️ **<5 supporting reads** - Weak evidence
⚠️ **Out-of-frame** - Unlikely to be functional
⚠️ **Novel fusion** - Not in databases (could be real or false positive)
⚠️ **Read-through transcription** - Adjacent genes, often not pathogenic

**Validation methods**:
- RT-PCR with fusion-spanning primers
- Sanger sequencing of PCR product
- FISH to confirm chromosomal rearrangement
- Western blot to confirm fusion protein expression

---

## Clinically Actionable Fusions

### FDA-Approved Targeted Therapies

| Fusion Gene | Cancer Type | Targeted Therapy |
|-------------|-------------|------------------|
| ALK fusions | NSCLC, ALCL | Crizotinib, alectinib, brigatinib, lorlatinib |
| ROS1 fusions | NSCLC, GBM | Crizotinib, entrectinib |
| RET fusions | NSCLC, thyroid | Selpercatinib, pralsetinib |
| NTRK1/2/3 fusions | Pan-cancer | Larotrectinib, entrectinib |
| FGFR2/3 fusions | Cholangiocarcinoma | Pemigatinib, infigratinib |
| BCR-ABL1 | CML, ALL | Imatinib, dasatinib, nilotinib, ponatinib |

### Common Cancer-Specific Fusions

**Lung Cancer (NSCLC)**:
- ALK (3-5%), ROS1 (1-2%), RET (1-2%), NTRK (rare)

**Prostate Cancer**:
- TMPRSS2-ERG (50%), TMPRSS2-ETV1/4

**Sarcomas**:
- EWS-FLI1 (Ewing sarcoma, 85%)
- SS18-SSX (synovial sarcoma, >95%)
- PAX3/7-FOXO1 (alveolar rhabdomyosarcoma)

**Thyroid Cancer**:
- RET/PTC fusions (papillary thyroid, 20-40%)
- PAX8-PPARG (follicular carcinoma)

---

## Resource Requirements

### Node Size Recommendations

| Data Size | Node Size | Specs | Estimated Runtime |
|-----------|-----------|-------|-------------------|
| nf-core test data | XSMALL | 4 CPU, 15GB RAM | 1-2 hours |
| 1-2 samples (50M reads) | SMALL | 8 CPU, 30GB RAM | 3-6 hours |
| 3-10 samples | MEDIUM | 32 CPU, 120GB RAM | 4-8 hours |
| 10-50 samples | LARGE | 64 CPU, 360GB RAM | 8-24 hours |

**Recommendation**: Start with XSMALL for testing, then scale based on your data:
- Test data or very small pilot: XSMALL
- 1-2 clinical samples: SMALL
- Standard cohort (5-10 samples): MEDIUM
- Large discovery study (20+ samples): LARGE

### Storage Requirements

- **Per sample**: ~20-50 GB (intermediate + final files)
- **Test dataset**: ~5 GB total
- **10-sample cohort**: ~200-500 GB

---

## Testing

### Test Dataset

This app has been tested with nf-core test data:
- **Sample**: Human RNA-seq test reads (paired-end)
- **Size**: Small test dataset (~1M reads)
- **Location**: nf-core/test-datasets repository
- **Expected runtime**: 1-2 hours on XSMALL node

**Test samplesheet** (`test_samplesheet.csv`):
```csv
sample,fastq_1,fastq_2,strandedness
test,https://github.com/nf-core/test-datasets/raw/81cb45949e75cbb85cbf6c5ec9009ab45b160823/testdata/human/reads_1.fq.gz,https://github.com/nf-core/test-datasets/raw/81cb45949e75cbb85cbf6c5ec9009ab45b160823/testdata/human/reads_2.fq.gz,forward
```

### Running the Test

```bash
# Upload test samplesheet to stash
camber stash cp test_samplesheet.csv stash://username/rnafusion-test/

# Run the app
camber app run rnafusion-cancer-detection \
  --input input="stash://username/rnafusion-test/test_samplesheet.csv" \
  --input outdir="stash://username/rnafusion-test/results"

# Monitor job (replace XXXX with your job ID)
camber job get XXXX

# View logs when complete
camber job logs XXXX
```

---

## Biological Applications

### Cancer Research
- Identify driver fusions in tumor samples
- Discover novel fusions in understudied cancer types
- Characterize fusion landscapes across cancer subtypes

### Clinical Diagnostics
- Confirm diagnostic fusions (e.g., EWS-FLI1 in Ewing sarcoma)
- Identify actionable therapeutic targets
- Guide clinical trial enrollment based on fusion status

### Precision Medicine
- Match patients to fusion-targeted therapies
- Monitor minimal residual disease via fusion transcripts
- Detect resistance mechanisms after targeted therapy

### Drug Discovery
- Identify novel therapeutic targets
- Validate fusion dependencies for drug development
- Study fusion oncogene biology

---

## Limitations

1. **Human GRCh38 only**: Cannot be used for other organisms or older human genome versions
2. **Paired-end recommended**: Single-end data supported but with reduced sensitivity
3. **Minimum read depth**: 50M reads minimum; lower depth reduces sensitivity for rare fusions
4. **RNA-level only**: Detects expressed fusions, not DNA-level rearrangements
5. **False positives possible**: Always validate high-priority fusions before clinical decisions
6. **FFPE limitations**: Lower RNA quality from FFPE may reduce sensitivity

---

## References

**Pipeline Documentation**:
- nf-core/rnafusion: https://nf-co.re/rnafusion
- GitHub: https://github.com/nf-core/rnafusion
- Citation: DOI 10.5281/zenodo.3946477

**Fusion Detection Tools**:
- STAR-Fusion: https://github.com/STAR-Fusion/STAR-Fusion
- arriba: https://github.com/suhrig/arriba
- FusionCatcher: https://github.com/ndaniel/fusioncatcher

**Fusion Databases**:
- COSMIC Fusion: https://cancer.sanger.ac.uk/cosmic/fusion
- ChimerDB: http://www.kobic.re.kr/chimerdb/
- FusionGDB: https://ccsm.uth.edu/FusionGDB/

**Clinical Resources**:
- OncoKB: https://www.oncokb.org/
- CIViC: https://civicdb.org/

---

## Support

For technical issues:
- Check `TESTING_LOG.md` for troubleshooting guidance
- Review MultiQC report for quality control issues
- Consult nf-core/rnafusion documentation

For biological interpretation:
- Consult COSMIC Fusion database for known oncogenic fusions
- Review OncoKB for therapeutic implications
- Consider genetic counseling for clinical cases