# Rare Disease Diagnosis: Whole Genome Analysis

## Use Case

Comprehensive genomic analysis for patients with rare genetic diseases using whole genome sequencing (WGS). Detects SNVs, indels, structural variants, and CNVs to identify disease-causing mutations.

## When to Use This App

- You have whole genome sequencing data from a rare disease patient
- Previous genetic tests were negative or inconclusive
- Need comprehensive variant detection across entire genome
- Patient presents with undiagnosed genetic condition
- Clinical diagnostics or research gene discovery

## Input Requirements

### Sample Sheet Format

CSV file with columns: `sample, lane, fastq_1, fastq_2, sex, phenotype, paternal_id, maternal_id, case_id`

**Single Patient Example:**
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,patient_R1.fastq.gz,patient_R2.fastq.gz,2,2,,,case001
```

**Trio Example (Patient + Parents):**
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,patient_R1.fastq.gz,patient_R2.fastq.gz,2,2,father01,mother01,family001
father01,L001,father_R1.fastq.gz,father_R2.fastq.gz,1,1,,,family001
mother01,L001,mother_R1.fastq.gz,mother_R2.fastq.gz,2,1,,,family001
```

### Column Definitions

- **sample**: Unique sample identifier
- **lane**: Sequencing lane (L001, L002, etc.)
- **fastq_1**: Path to Read 1 file (R1 or _1)
- **fastq_2**: Path to Read 2 file (R2 or _2)
- **sex**: 0=unknown, 1=male, 2=female
- **phenotype**: 0=unknown, 1=unaffected, 2=affected
- **paternal_id**: Father's sample ID (empty if not applicable)
- **maternal_id**: Mother's sample ID (empty if not applicable)
- **case_id**: Case/family identifier

### Data Requirements

- Paired-end Illumina WGS data (FASTQ format)
- Minimum 30x coverage recommended, 50x optimal
- 150bp paired-end reads (standard)
- ~100-150 GB per sample at 30x coverage

## Parameters

### Required Inputs

1. **Sample Information Sheet**: CSV file with sample details
2. **Output Directory**: Where to save results
3. **Reference Genome**: GRCh38 (recommended) or GRCh37 (legacy)

### Hardcoded Settings

- **Analysis Type**: WGS (whole genome sequencing)
- **Variant Caller**: DeepVariant (AI-based, high accuracy)
- **Pipeline Version**: 2.6.0
- **Tools**: Alignment (BWA-mem2), SV calling (Manta), Annotation (VEP), Scoring (CADD)

## Outputs

### Variant Calls

- **SNVs and Indels**: Single nucleotide variants and small insertions/deletions
- **Structural Variants**: Large genomic rearrangements (deletions, duplications, inversions)
- **Copy Number Variants**: Regions with abnormal copy numbers
- **VCF Files**: Standard variant call format for downstream analysis

### Annotations

- **Gene Impact**: Which genes affected and how (loss of function, missense, etc.)
- **Pathogenicity Scores**: CADD scores predicting variant harm
- **Clinical Relevance**: Links to disease databases (OMIM, ClinVar)
- **Ranked Candidates**: Variants prioritized by disease likelihood

### Quality Control

- **MultiQC Report**: Comprehensive HTML report with all metrics
- **Coverage Analysis**: Per-region sequencing depth
- **Alignment Statistics**: Mapping rates, duplicate levels
- **Sample QC**: Identity verification, quality checks

### Analysis Files

- **BAM Files**: Aligned reads for genome browser visualization
- **Annotated VCFs**: Variants with functional annotations
- **Summary Reports**: Analysis statistics and QC metrics

## Expected Runtime

- **Single patient (30x)**: 12-18 hours
- **Single patient (50x)**: 18-24 hours
- **Trio (3 samples)**: 24-36 hours
- **Multiple samples**: Scales linearly

*Runtime depends on data size, coverage, and node size selected*

## Resource Recommendations

- **XSMALL**: Test data only (not for real analysis)
- **SMALL**: Single sample, low coverage or testing
- **MEDIUM**: 1-2 samples at 30x coverage
- **LARGE**: 1-3 samples at 30-50x coverage ✓ Recommended for production
- **XLARGE**: Trios or 4+ samples

## Testing

### Using nf-core Test Data

```bash
# Upload test samplesheet
camber stash cp test_samplesheet.csv stash://david40962/test-raredisease/

# Run test
camber app run raredisease-wgs-standard \
  --input input="stash://david40962/test-raredisease/test_samplesheet.csv" \
  --input outdir="stash://david40962/test-raredisease/results" \
  --input genome="GRCh38"

# Monitor job
camber job get {job-id}
camber job logs {job-id}
```

## Clinical Considerations

### Diagnostic Yield

- Approximately 40% diagnostic rate in clinical practice
- Higher success with well-characterized phenotypes
- Best results with trio analysis (patient + parents)
- Improved detection with high coverage (50x vs 30x)

### Interpretation

- Results require clinical genetics expertise
- Not all variants are disease-causing
- Clinical correlation essential
- Consider phenotype match with gene function

### Incidental Findings

- May detect medically actionable variants unrelated to primary indication
- Follow institutional policies for secondary findings
- Discuss with patients before testing

## Scientific Background

This app uses the nf-core/raredisease pipeline (v2.6.0), a best-practice workflow developed from clinical diagnostic experience with thousands of rare disease patients. Key features:

- **DeepVariant**: AI-based variant caller with superior accuracy
- **Manta**: Structural variant detection
- **VEP**: Comprehensive variant annotation
- **CADD**: Pathogenicity prediction scoring
- **Clinical Validation**: Proven ~40% diagnostic yield in Stockholm region healthcare

The pipeline follows GATK best practices and implements quality standards appropriate for clinical diagnostics.

## References

- **nf-core/raredisease**: https://nf-co.re/raredisease/2.6.0/
- **GitHub**: https://github.com/nf-core/raredisease
- **Pipeline Paper**: Pettersson et al. (referenced in nf-core docs)
- **nf-core Framework**: Ewels et al., Nature Biotechnology 2020

## Troubleshooting

### Common Issues

1. **Insufficient Coverage**: Ensure 30x+ coverage for reliable variant calling
2. **File Not Found**: Verify FASTQ paths in samplesheet are correct
3. **Memory Errors**: Increase node size for large samples or high coverage
4. **Lane Information**: Check FASTQ filenames for correct lane identifiers

### Getting Help

- Review MultiQC report for quality issues
- Check pipeline logs for specific error messages
- Verify samplesheet format matches specification exactly
- Ensure FASTQ files are properly gzipped

---

**Version**: 1.0.0
**Pipeline**: nf-core/raredisease 2.6.0
**Created**: 2025-09-30
**Maintainer**: david40962