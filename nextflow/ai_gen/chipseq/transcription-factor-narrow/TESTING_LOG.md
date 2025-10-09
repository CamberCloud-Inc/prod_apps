# ChIP-seq Transcription Factor (Narrow Peak) Testing Log

**Date:** 2025-09-30
**Tester:** Claude Code
**Username:** david40962
**App Name:** chipseq-tf-narrow
**nf-core Pipeline:** nf-core/chipseq v2.0.0

## Test Configuration

- **Node Size:** XSMALL (4 CPUs, 15GB RAM)
- **Genome:** R64-1-1 (Yeast)
- **Test Data:** nf-core test datasets (SPT5 ChIP-seq)
- **Samplesheet:** test_samplesheet.csv (uploaded to stash://david40962/chipseq-tf-narrow/)

## Test Attempts Summary

### Attempt 1 - Job ID: 4472
**Status:** FAILED
**Duration:** 27s
**Error:** `Cannot a find a file system provider for scheme: stash`

**Command:**
```bash
nextflow run nf-core/chipseq --input stash://david40962/chipseq-tf-narrow/test_samplesheet.csv --outdir stash://david40962/chipseq-tf-narrow/results --genome R64-1-1 --macs_gsize 2.7e9 --narrow_peak true -r 2.0.0
```

**Root Cause:** Nextflow cannot directly read input files from stash:// URLs. The --input parameter must point to a local file or HTTP/S3 URL.

**Fix Applied:** Changed to use relative path for samplesheet (test_samplesheet.csv) which is available in the working directory via --path parameter.

---

### Attempt 2 - Job ID: 4479
**Status:** FAILED
**Duration:** 11s
**Error:** `/home/camber/chipseq-tf-narrow/results`

**Command:**
```bash
nextflow run nf-core/chipseq --input test_samplesheet.csv --outdir results --genome R64-1-1 --macs_gsize 2.7e9 --narrow_peak true -r 2.0.0
```

**Root Cause:** Output directory path validation issue. Relative path may not have proper permissions or location.

**Fix Applied:** Changed to use ./results with explicit relative path notation.

---

### Attempt 3 - Job ID: 4484
**Status:** FAILED
**Duration:** 11s
**Error:** `/home/camber/chipseq-tf-narrow/results`

**Command:**
```bash
nextflow run nf-core/chipseq --input test_samplesheet.csv --outdir ./results --genome R64-1-1 --macs_gsize 2.7e9 --narrow_peak true -r 2.0.0
```

**Root Cause:** Same output directory issue persisted.

**Fix Applied:** Changed to use absolute path in /camber_work directory.

---

### Attempt 4 - Job ID: 4488
**Status:** FAILED
**Duration:** 16s
**Error:** `ERROR: Validation of pipeline parameters failed! * --macs_gsize: expected type: Number, found: String (2.7e9)`

**Command:**
```bash
nextflow run nf-core/chipseq --input test_samplesheet.csv --outdir /camber_work/results --genome R64-1-1 --macs_gsize 2.7e9 --narrow_peak true -r 2.0.0
```

**Root Cause:** The --macs_gsize parameter expects a numeric type but scientific notation '2.7e9' is being parsed as a string by the pipeline's parameter validation schema.

**Fix Applied:** Removed --macs_gsize from command entirely to test if pipeline can auto-detect.

---

### Attempt 5 - Job ID: 4492
**Status:** FAILED
**Duration:** 30s
**Error:** `Both '--read_length' and '--macs_gsize' not specified! Please specify either to infer MACS2 genome size for peak calling.`

**Command:**
```bash
nextflow run nf-core/chipseq --input test_samplesheet.csv --outdir /camber_work/results --genome R64-1-1 --narrow_peak true -r 2.0.0
```

**Root Cause:** Pipeline requires either --macs_gsize (as proper number) OR --read_length for genome size calculation. Neither was provided after removing --macs_gsize.

**Fix Applied:** Updated app.json to include --read_length 50 instead of --macs_gsize. This allows the pipeline to auto-calculate genome size using khmer unique-kmers.py.

---

## Key Findings

1. **Stash URL Limitation:** Nextflow's --input parameter cannot directly access stash:// URLs. Input files must be:
   - Local files in the working directory (uploaded via --path parameter)
   - HTTP/HTTPS URLs
   - S3 URLs (with proper credentials)

2. **Output Directory:** Use absolute paths like /camber_work/results for output directories on Camber platform.

3. **Parameter Type Validation:** nf-core/chipseq v2.0.0 has strict parameter type validation:
   - --macs_gsize must be a pure number (not string with 'e' notation)
   - Scientific notation like '2.7e9' fails validation
   - Alternative: use --read_length parameter to auto-calculate genome size

4. **App.json Fix Required:** The original command in app.json had `--macs_gsize 2.7e9` which causes validation errors. Changed to `--read_length 50` for better compatibility.

## Updated app.json Command

**Before:**
```
nextflow run nf-core/chipseq --input ${input} --outdir ${outdir} --genome ${genome} --macs_gsize 2.7e9 --narrow_peak true -r 2.0.0
```

**After:**
```
nextflow run nf-core/chipseq --input ${input} --outdir ${outdir} --genome ${genome} --narrow_peak true --read_length 50 -r 2.0.0
```

## Recommendations

1. **For app.json:**
   - Use --read_length parameter instead of --macs_gsize
   - Ensure input samplesheet references HTTP URLs for FASTQ files (not stash:// URLs)
   - Use template variables ${input}, ${outdir}, ${genome} as intended

2. **For testing:**
   - Always upload samplesheet to stash directory specified in --path
   - Samplesheet should contain HTTP/S3 URLs for FASTQ files
   - Use XSMALL nodes for initial testing with small datasets
   - Consider using nf-core test profile: `-profile test,k8s` for validation

3. **For production use:**
   - Document that FASTQ files must be accessible via HTTP/S3 URLs
   - Provide example samplesheets with proper URL format
   - Scale to MEDIUM or LARGE nodes based on dataset size
   - Typical resources: 5-20 samples = MEDIUM, 20-50 samples = LARGE

## Next Steps

- Re-run test with updated app.json (attempt 6 if within limit)
- Monitor for successful completion
- Validate output files are generated correctly
- Document final success/failure in STATUS.txt
- Commit all changes to git

## Test Data Details

**Sample Sheet:** test_samplesheet.csv
**Samples:**
- SPT5_T0 (2 replicates) - ChIP samples with SPT5 antibody
- SPT5_T15 (2 replicates) - ChIP samples with SPT5 antibody
- SPT5_INPUT (2 replicates) - Input control samples

**FASTQ Files:** Sourced from nf-core/test-datasets on GitHub (HTTP URLs)
**Expected Behavior:** Small test dataset should complete in 30-60 minutes on XSMALL node.
