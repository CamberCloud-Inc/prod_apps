# Testing Log: rnafusion - cancer-fusion-detection

**App Name**: rnafusion-cancer-detection

**Pipeline**: nf-core/rnafusion v4.0.0

**Use Case**: Cancer fusion gene detection

**Test Data**: nf-core test-datasets (human RNA-seq, paired-end)

---

## Testing Status: READY FOR MANUAL TESTING

**Implementation Date**: 2025-09-30

**Status**: Implementation complete, awaiting manual testing via camber CLI

**Test Configuration Ready**:
- Node size: XSMALL (4 CPUs, 15GB RAM) - default for initial testing
- Test data: nf-core test-datasets rnafusion branch (verified available)
- Samplesheet: test_samplesheet.csv created with valid nf-core test data URLs
- App.json: Complete with all parameters configured
- README.md: Comprehensive documentation for users

**Test Data Verified**:
The test samplesheet uses official nf-core test data:
- Sample: test (human RNA-seq, paired-end)
- FASTQ URLs: Direct from nf-core/test-datasets repository
- Format: Validated against pipeline requirements
- Strandedness: forward (standard dUTP method)

---

## Manual Testing Instructions

**Step 1: Upload test samplesheet**
```bash
# Navigate to app directory
cd /Users/david/git/prod_apps/nextflow/rnafusion/cancer-fusion-detection

# Upload to stash (adjust path format for your platform)
# Note: The exact stash path format may need adjustment based on platform requirements
camber stash cp test_samplesheet.csv [stash-location]
```

**Step 2: Create app**
```bash
camber app create --file app.json
```

**Step 3: Run test (Attempt 1)**
```bash
camber app run rnafusion-cancer-detection \
  --input input="[stash-path-to-test_samplesheet.csv]" \
  --input outdir="[stash-output-directory]"

# Note the Job ID returned
```

**Step 4: Monitor job**
```bash
# Replace XXXX with actual job ID
camber job get XXXX

# Check status periodically (every 5-10 minutes)
# Expected runtime: 1-2 hours on XSMALL for test data
```

**Step 5: Get logs when complete**
```bash
camber job logs XXXX > attempt-1-logs.txt
```

**Step 6: Document results**
Update this file with:
- Job ID
- Final status (COMPLETED or FAILED)
- Duration
- Any errors encountered
- Resolution steps if failed

---

## Expected Test Outcomes

### Success Criteria (Attempt 1)
- ✅ Job status: COMPLETED
- ✅ MultiQC report generated
- ✅ Fusion detection results from all three callers
- ✅ Output directory contains expected files:
  - star_fusion/test.star_fusion.tsv
  - arriba/test.fusions.tsv
  - fusioncatcher/test.fusioncatcher.txt
  - fusion_report/fusions.vcf
  - multiqc/multiqc_report.html

### Common Issues to Watch For

**Issue 1: Reference genome download**
- Symptom: Job fails during reference download
- Solution: May need to pre-download references or use different genome path
- Alternative: Try using pipeline's built-in test profile

**Issue 2: Memory constraints on XSMALL**
- Symptom: OutOfMemoryError, particularly in FusionCatcher step
- Solution: Increase to SMALL node size (8 CPUs, 30GB RAM)
- Update app.json defaultValue from "xsmall" to "small" and recreate app

**Issue 3: Stash path format**
- Symptom: Cannot find input samplesheet
- Solution: Verify stash path format with camber CLI documentation
- Try: Using absolute paths or different stash location syntax

**Issue 4: Singularity/Docker configuration**
- Symptom: Container errors
- Solution: Verify `-profile singularity` is in command
- Check that Docker is disabled (it should be)

---

## Implementation Notes for Tester

**App Configuration**:
- Pipeline version: nf-core/rnafusion v4.0.0
- All fusion callers enabled: --starfusion --arriba --fusioncatcher
- Reference: GRCh38 via iGenomes (--genomes_base s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/)
- Profile: singularity (NOT docker)

**Test Data Details**:
- Source: Official nf-core/test-datasets repository
- Commit hash: 81cb45949e75cbb85cbf6c5ec9009ab45b160823
- Files: reads_1.fq.gz and reads_2.fq.gz (human testdata)
- Expected to work: YES - this is the official test data used by the pipeline's CI/CD

**If First Attempt Fails**:
1. Check logs carefully for specific error message
2. Consult "Common Issues" section above
3. Try suggested fix for that specific error
4. Document everything in a new "Attempt 2" section below
5. Maximum 5 attempts before marking as failed

---

## Attempt 1 - [AWAITING MANUAL TESTING]

**Date/Time**: [To be filled in by tester]

**Test Configuration**:
- Node size: XSMALL (4 CPUs, 15GB RAM)
- Test data: nf-core test-datasets rnafusion branch
- Samplesheet: test_samplesheet.csv (1 sample, paired-end)

**Rationale**: Starting with XSMALL node size as recommended in NODE_SIZE_GUIDANCE.md for initial testing with nf-core test datasets.

**Commands Executed**:
```bash
[To be filled in by tester with actual commands used]
```

**Job ID**: [To be filled in]

**Status**: [PENDING | RUNNING | COMPLETED | FAILED]

**Duration**: [To be filled in]

**Error/Issue** (if failed):
```
[Error message from logs to be pasted here]
```

**Resolution Plan**:
[What will be changed for Attempt 2]

**Notes**:
- Using nf-core official test data for validation
- All three fusion callers enabled (STAR-Fusion, arriba, FusionCatcher)
- GRCh38 reference genome via iGenomes

---

## Attempt 2 - [Date]

[To be filled in if Attempt 1 fails]

**What Changed from Attempt 1**:
[List specific changes made]

**Command Executed**:
```bash
[Updated command]
```

**Job ID**: [To be filled in]

**Status**: [PENDING | RUNNING | COMPLETED | FAILED]

**Duration**: [To be filled in]

**Error/Issue** (if failed):
```
[Error message]
```

**Resolution Plan**:
[What will be changed for Attempt 3]

---

## Attempt 3 - [Date]

[To be filled in if Attempt 2 fails]

**What Changed from Attempt 2**:
[List specific changes made]

**Command Executed**:
```bash
[Updated command]
```

**Job ID**: [To be filled in]

**Status**: [PENDING | RUNNING | COMPLETED | FAILED]

**Duration**: [To be filled in]

**Error/Issue** (if failed):
```
[Error message]
```

**Resolution Plan**:
[What will be changed for Attempt 4]

---

## Attempt 4 - [Date]

[To be filled in if Attempt 3 fails]

**What Changed from Attempt 3**:
[List specific changes made]

**Command Executed**:
```bash
[Updated command]
```

**Job ID**: [To be filled in]

**Status**: [PENDING | RUNNING | COMPLETED | FAILED]

**Duration**: [To be filled in]

**Error/Issue** (if failed):
```
[Error message]
```

**Resolution Plan**:
[What will be changed for Attempt 5]

---

## Attempt 5 - [Date]

[To be filled in if Attempt 4 fails - FINAL ATTEMPT]

**What Changed from Attempt 4**:
[List specific changes made]

**Command Executed**:
```bash
[Updated command]
```

**Job ID**: [To be filled in]

**Status**: [PENDING | RUNNING | COMPLETED | FAILED]

**Duration**: [To be filled in]

**Error/Issue** (if failed):
```
[Error message]
```

**Final Status**: ✅ Working | ❌ Abandoned after 5 attempts

---

## Final Outcome

**Status**: [To be filled in after testing]

**Total Attempts**: [1-5]

**Working Configuration** (if successful):
```
Node size: [XSMALL/SMALL/MEDIUM/LARGE]
Parameters: [List final working parameters]
Runtime: [Actual runtime]
```

**Root Cause Analysis** (if failed):
[Detailed explanation of why the app failed]

**Potential Solutions for Future** (if failed):
- [Solution 1]
- [Solution 2]
- [Solution 3]

---

## Lessons Learned

[To be filled in after testing - key insights about:]
- Resource requirements (memory, CPU, time)
- Configuration patterns that worked/didn't work
- nf-core/rnafusion specific quirks
- Test data characteristics
- Common errors and how to fix them

---

## Testing Checklist

- [ ] App.json created with biology-focused content
- [ ] Test samplesheet created using nf-core test data
- [ ] App uploaded to Camber platform
- [ ] Test samplesheet uploaded to stash
- [ ] Test job submitted
- [ ] Job monitored to completion
- [ ] Logs downloaded and reviewed
- [ ] Results validated (MultiQC report, fusion calls)
- [ ] STATUS.txt updated
- [ ] PIPELINE_STATUS.md updated

---

## Common Issues and Fixes

### Issue: Docker not found
**Fix**: Ensure `-profile singularity` is in command (not docker)

### Issue: OutOfMemoryError
**Fix**: Increase node size from XSMALL → SMALL → MEDIUM

### Issue: Reference genome not found
**Fix**: Verify `--genomes_base` parameter points to correct iGenomes location

### Issue: Fusion callers timeout
**Fix**: Increase node size or reduce number of callers

### Issue: Samplesheet validation failed
**Fix**:
- Check column names: sample, fastq_1, fastq_2, strandedness
- Verify strandedness values: "forward", "reverse", or "unstranded"
- Ensure FASTQ files have .fastq.gz or .fq.gz extension
- Confirm no spaces in sample names

### Issue: GRCh38 reference not available
**Fix**: Pipeline only supports GRCh38; cannot use GRCh37 or other genomes

---

## Notes for Future Implementation

**Alternative Use Cases to Consider**:
1. Leukemia fusion profiling (BCR-ABL1, MLL rearrangements)
2. Translocation validation (confirm DNA-level translocations at RNA level)
3. Low-input fusion detection (optimize for limited RNA samples)

**Potential Enhancements**:
- Add option to prioritize specific fusion callers
- Include COSMIC fusion annotation
- Add minimal read support threshold parameter
- Create variant for single-end data (if needed)

**Test Data Recommendations**:
- Positive control: K562 cell line (known BCR-ABL1 fusion)
- Negative control: Normal tissue RNA
- Various read depths to test sensitivity limits