# {Pipeline Name}: {Use Case Descriptive Title}

**App Name**: `{app-name}`
**Pipeline**: nf-core/{pipeline} v{X.Y.Z}
**Status**: ✅ Working | ⚠️ Testing | ❌ Failed

---

## Use Case

{Brief description of what this specific app does and what biological question it addresses}

## When to Use This App

You should use this app when:
- ✓ Condition 1 (e.g., you have tumor/normal paired samples)
- ✓ Condition 2 (e.g., you want to identify somatic mutations)
- ✓ Condition 3 (e.g., you have whole genome or exome sequencing data)

**Not suitable for**:
- ✗ Situation 1 (e.g., single samples without matched normal)
- ✗ Situation 2 (e.g., RNA-seq data)

---

## Input Requirements

### 1. Sequencing Data (FASTQ Files)

{Description of what sequencing data is needed}

**Required**:
- File format: FASTQ (gzipped or uncompressed)
- Read type: Paired-end (R1 and R2 files)
- Quality: {Recommended quality metrics}
- Coverage: {Recommended coverage depth}

**Typical Sources**:
- Illumina sequencing platforms
- {Other platforms if applicable}

### 2. Sample Information Sheet (CSV File)

Create a CSV file with the following format:

```csv
column1,column2,column3,column4
example1,value1,value2,value3
example2,value1,value2,value3
```

**Column Descriptions**:

| Column | Description | Example Values | Required |
|--------|-------------|----------------|----------|
| **column1** | {Detailed explanation} | {examples} | Yes |
| **column2** | {Detailed explanation} | {examples} | Yes |
| **column3** | {Detailed explanation} | {examples} | Yes/No |
| **column4** | {Detailed explanation} | {examples} | No |

**Important Notes**:
- Note 1: {Critical information about samplesheet}
- Note 2: {Constraints or requirements}
- Note 3: {Common mistakes to avoid}

**Example Samplesheet**:

See `test_samplesheet.csv` in this directory for a complete working example.

### 3. Reference Genome

Choose the appropriate reference genome for your organism:

| Organism | Recommended | Alternative | Notes |
|----------|-------------|-------------|-------|
| Human | GRCh38/hg38 | GRCh37/hg19 | Use GRCh38 for new studies |
| Mouse | GRCm39/mm39 | GRCm38/mm10 | Use GRCm39 for latest annotations |
| {Other} | {Version} | {Alt version} | {Notes} |

---

## Parameters

This app requires the following inputs:

### Required Parameters

1. **Sample Information Sheet**
   - What: CSV file with sample metadata
   - Format: See above
   - Example: `stash://username/my_samples.csv`

2. **Output Directory**
   - What: Where to save results
   - Format: Stash path
   - Example: `stash://username/results`

3. **Reference Genome**
   - What: Genome assembly to use
   - Options: {List available genomes}
   - Default: {Default genome}

### Optional Parameters

{If any parameters are optional, list them here with descriptions}

---

## Expected Outputs

When this analysis completes successfully, you will find:

### Primary Results

**Location**: `{output-dir}/results/`

1. **{Output Type 1}** (`path/to/files/*.ext`)
   - Description: What this output is
   - Format: File format
   - Interpretation: How to use/interpret these results

2. **{Output Type 2}** (`path/to/files/*.ext`)
   - Description: What this output is
   - Format: File format
   - Interpretation: How to use/interpret these results

### Quality Control Reports

**Location**: `{output-dir}/multiqc/`

- **MultiQC Report** (`multiqc_report.html`)
  - Comprehensive QC across all samples
  - Check for: {Key metrics to examine}
  - Red flags: {Warning signs in QC}

### Supporting Files

**Location**: `{output-dir}/pipeline_info/`

- Pipeline execution report
- Software versions used
- Parameters used for this run

---

## Expected Runtime

| Dataset Size | Node Size | Typical Runtime |
|--------------|-----------|-----------------|
| Test data | SMALL | 10-30 minutes |
| {Size 1} (e.g., 1-5 samples) | MEDIUM | {time range} |
| {Size 2} (e.g., 5-20 samples) | LARGE | {time range} |
| {Size 3} (e.g., 20+ samples) | XLARGE | {time range} |

**Factors affecting runtime**:
- Sample size (number of samples)
- Data size (sequencing depth)
- Genome size (human vs. bacteria)
- Complexity (WGS vs. targeted sequencing)

---

## Resource Requirements

**Recommended Node Size**: {SMALL | MEDIUM | LARGE | XLARGE}

| Node Size | Use For | Specs |
|-----------|---------|-------|
| SMALL | Test datasets only | 8 CPU, 30GB RAM |
| MEDIUM | {Use case} | 32 CPU, 120GB RAM |
| LARGE | {Use case} (Recommended) | 64 CPU, 360GB RAM |
| XLARGE | {Use case} | 96 CPU, 540GB RAM |

**Special Requirements**:
- GPU: {Yes/No - if needed, explain why}
- High memory: {If critical processes need extra RAM}
- Long runtime: {If certain steps take many hours}

---

## Testing Instructions

### Quick Test

Run with the included test data to verify the app works:

```bash
# 1. Upload test files to stash
cd /Users/david/git/prod_apps/nextflow/{pipeline}/{usecase}
camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
camber stash cp {pipeline}-{usecase}-config.config stash://username/test-{pipeline}/

# 2. Verify upload
camber stash ls test-{pipeline}/

# 3. Run test
camber app run {app-name} \
  --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
  --input output="stash://username/test-{pipeline}/results" \
  --input genome="GRCh38"

# 4. Monitor job (note the Job ID from previous command)
camber job get {job-id}

# 5. When complete, check logs
camber job logs {job-id}

# 6. Verify outputs
camber stash ls test-{pipeline}/results/
```

### Expected Test Results

When test completes successfully:
- ✅ Job status: COMPLETED
- ✅ Runtime: ~{X} minutes
- ✅ Output files: {List expected files}
- ✅ No errors in logs

### Testing with Your Own Data

1. **Prepare your samplesheet** following the format above
2. **Upload your data**:
   ```bash
   camber stash cp my_samplesheet.csv stash://username/my-project/
   camber stash cp my_data/*.fastq.gz stash://username/my-project/data/
   ```
3. **Run the analysis**:
   ```bash
   camber app run {app-name} \
     --input input="stash://username/my-project/my_samplesheet.csv" \
     --input output="stash://username/my-project/results" \
     --input genome="{appropriate-genome}"
   ```

---

## Troubleshooting

### Common Issues

#### Issue: Job fails with "File not found"
**Cause**: Samplesheet has incorrect paths or files not uploaded
**Solution**:
- Verify file paths in samplesheet match stash locations
- Check files uploaded: `camber stash ls {directory}`
- Use relative paths if files in same directory as samplesheet

#### Issue: Job fails with "Out of memory"
**Cause**: Selected node size too small for data
**Solution**:
- Increase node size to LARGE or XLARGE
- Check if your dataset is unusually large
- Review QC - excessive data size may indicate quality issues

#### Issue: Job completes but results look wrong
**Cause**: Incorrect parameters or poor quality input data
**Solution**:
- Review MultiQC report for quality issues
- Verify correct genome was selected
- Check samplesheet for errors (swapped samples, wrong metadata)

### Getting Help

If you encounter issues:

1. **Check logs**: `camber job logs {job-id}` for error messages
2. **Review QC**: Look at MultiQC report for data quality problems
3. **Consult pipeline docs**: https://nf-co.re/{pipeline}
4. **Check GitHub issues**: https://github.com/nf-core/{pipeline}/issues

---

## Scientific Background

### Method Overview

{1-2 paragraphs explaining the scientific method/algorithm used}

### Tools Used

This app uses the following tools:
- **Tool 1**: Brief description and purpose
- **Tool 2**: Brief description and purpose
- **Tool 3**: Brief description and purpose

### Key Publications

Cite key papers for:
1. The pipeline: [Citation]
2. Main algorithms: [Citations]
3. This specific approach: [Citations if applicable]

---

## Advanced Users

For users who want more control or need to understand the underlying pipeline:

### Full Pipeline Documentation
- nf-core docs: https://nf-co.re/{pipeline}
- GitHub repository: https://github.com/nf-core/{pipeline}
- Publication: [If available]

### Hardcoded Parameters

This app has pre-configured these parameters for optimal {use case}:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `--param1` | `value1` | {Why this value} |
| `--param2` | `value2` | {Why this value} |

### Custom Configuration

The custom configuration file (`{pipeline}-{usecase}-config.config`) includes:
- Process-specific resource allocations
- Container settings (Singularity, not Docker)
- Use-case-specific optimizations

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial release |
| YYYY-MM-DD | 1.1 | {Description of changes} |

---

## Files in This Directory

- `app.json` - App configuration for Camber platform
- `{pipeline}-{usecase}-config.config` - Nextflow configuration file
- `test_samplesheet.csv` - Example samplesheet for testing
- `README.md` - This file
- `TESTING_LOG.md` - Detailed testing history
- `STATUS.txt` - Current app status

---

## Contact & Support

**App Maintained By**: {Name/team}
**Last Updated**: YYYY-MM-DD

For issues with this specific app configuration, see TESTING_LOG.md.
For issues with the underlying nf-core pipeline, visit the pipeline GitHub.