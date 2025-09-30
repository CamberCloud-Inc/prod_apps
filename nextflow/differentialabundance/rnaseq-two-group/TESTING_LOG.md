# Testing Log: differentialabundance - rnaseq-two-group

**App Name**: differentialabundance-rnaseq-twogroup
**Use Case**: RNA-seq Two-Group Differential Expression Analysis
**Pipeline Version**: nf-core/differentialabundance v1.5.0
**Started**: 2025-09-30

---

## Test Data Information

**Dataset**: Mouse RNA-seq (SRP254919) from nf-core/test-datasets
**Source**: https://github.com/nf-core/test-datasets (modules branch)
**Size**: Top 1000 genes, 6 samples across 2 conditions
**Expected Runtime**: 10-20 minutes on XSMALL node

**Test Files**:
- Samplesheet: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.samplesheet.csv
- Contrasts: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.contrasts.csv
- Matrix: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.salmon.merged.gene_counts.top1000cov.tsv

---

## Attempt 1 - 2025-09-30

**Node Size**: XSMALL (4 CPUs, 15GB RAM)
**Rationale**: Starting with XSMALL as recommended for initial testing with nf-core test dataset per NODE_SIZE_GUIDANCE.md

### Command Used
```bash
camber app create --file app.json
camber app run differentialabundance-rnaseq-twogroup
```

**App Configuration**:
- All parameters embedded in command (no separate config file)
- Using default test data URLs
- Singularity profile via /etc/mpi/nextflow.camber.config

### Job Details
- **Job ID**: [To be filled]
- **Submission Time**: [To be filled]
- **Status**: [To be filled]

### Results
- **Status**: [PENDING/RUNNING/COMPLETED/FAILED]
- **Duration**: [To be filled]
- **Exit Code**: [To be filled]

### Error Messages (if failed)
```
[To be filled if job fails]
```

### Analysis
[To be filled after job completes]

### Resolution for Next Attempt
[To be filled if needed]

---

## Attempt 2 - [Date]

[To be filled if Attempt 1 fails]

**Changes from Attempt 1**:
- [List specific changes]

---

## Attempt 3 - [Date]

[To be filled if Attempt 2 fails]

---

## Attempt 4 - [Date]

[To be filled if Attempt 3 fails]

---

## Attempt 5 - [Date]

[To be filled if Attempt 4 fails]

---

## Final Outcome

**Status**: [✅ Working | ❌ Failed after 5 attempts]

### If Working (✅)
- **Successful Attempt**: #[N]
- **Final Configuration**: [Describe working setup]
- **Node Size Used**: [Size that worked]
- **Runtime**: [Actual duration]
- **Key Success Factors**:
  1. [Factor 1]
  2. [Factor 2]
  3. [Factor 3]

### If Failed (❌)
- **Attempts Made**: 5
- **Primary Issue**: [Root cause]
- **Attempted Solutions**:
  1. [Solution 1] - [Outcome]
  2. [Solution 2] - [Outcome]
  3. [Solution 3] - [Outcome]
- **Recommendation**: [What would be needed to fix]

---

## Lessons Learned

### What Worked
- [Key pattern or configuration that succeeded]

### What Didn't Work
- [Approaches that failed and why]

### Configuration Patterns
- [Reusable patterns for future apps]

### Pipeline-Specific Notes
- [Anything unique to differentialabundance pipeline]

---

## Recommendations for Future Use

### Node Sizing
- **Testing**: [Recommended size]
- **Small datasets (5-10 samples)**: [Recommended size]
- **Standard datasets (10-30 samples)**: [Recommended size]

### Common Issues to Avoid
1. [Issue 1 and how to prevent]
2. [Issue 2 and how to prevent]
3. [Issue 3 and how to prevent]

### Best Practices
1. [Practice 1]
2. [Practice 2]
3. [Practice 3]

---

## Next Steps

- [ ] Update STATUS.txt with final outcome
- [ ] Update PIPELINE_STATUS.md
- [ ] Commit to git with descriptive message
- [ ] [If working] Consider implementing next use case
- [ ] [If failed] Document blockers for future resolution