# Testing Log: taxprofiler - microbiome-kraken2

**App Name**: `taxprofiler-microbiome-kraken2`

**Pipeline**: nf-core/taxprofiler v1.2.3

**Use Case**: Microbiome taxonomic profiling with Kraken2

**Testing Started**: 2025-09-30

---

## Testing Strategy

1. Start with XSMALL node and nf-core test data
2. Test command without separate config file (all params in command)
3. Use Singularity profile (Docker not available on Camber)
4. Maximum 5 attempts to get working

---

## Test Data

**Sample Sheet**: `https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/samplesheet.csv`

**Database Sheet**: `https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/database_v1.2.csv`

**Data Description**:
- Miniature Kraken2 test database (tiny, for testing only)
- 6 test samples (mix of FASTQ and FASTA, paired and single-end)
- Illumina and Nanopore data included

---

## Attempt 1 - [DATE] [TIME]

**Status**: PENDING

**Command Used**:
```bash
camber app create --file app.json
```

**Run Command**:
```bash
camber app run taxprofiler-microbiome-kraken2 \
  --input input="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/samplesheet.csv" \
  --input databases="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/database_v1.2.csv" \
  --input output="./taxprofiler-test-attempt1"
```

**Job ID**: [To be filled]

**Node Size**: XSMALL (4 CPUs, 15GB RAM)

**Expected Behavior**:
- Download test data and databases
- Run Kraken2 classification on test samples
- Generate Bracken abundance estimates
- Produce standardized output tables
- Complete MultiQC report

**Duration**: [To be filled]

**Result**: [COMPLETED/FAILED]

**Output Check**:
- [ ] Kraken2 reports generated
- [ ] Bracken outputs present
- [ ] TAXPASTA standardized tables created
- [ ] MultiQC report available
- [ ] No error messages in logs

**Error Messages** (if failed):
```
[To be filled if failed]
```

**Resolution** (if failed):
[Analysis of error and planned fix]

---

## Attempt 2 - [DATE] [TIME]

**Status**: [PENDING/IN_PROGRESS/COMPLETED/FAILED]

**Changes from Attempt 1**:
[What was modified based on Attempt 1 results]

**Command Used**:
```bash
[Updated command if different]
```

**Job ID**: [To be filled]

**Duration**: [To be filled]

**Result**: [COMPLETED/FAILED]

**Error Messages** (if failed):
```
[To be filled if failed]
```

**Resolution** (if failed):
[Analysis and next steps]

---

## Attempt 3 - [DATE] [TIME]

**Status**: [PENDING/IN_PROGRESS/COMPLETED/FAILED]

**Changes from Attempt 2**:
[What was modified]

**Command Used**:
```bash
[Command]
```

**Job ID**: [To be filled]

**Duration**: [To be filled]

**Result**: [COMPLETED/FAILED]

**Error Messages** (if failed):
```
[To be filled if failed]
```

**Resolution** (if failed):
[Analysis and next steps]

---

## Attempt 4 - [DATE] [TIME]

**Status**: [PENDING/IN_PROGRESS/COMPLETED/FAILED]

**Changes from Attempt 3**:
[What was modified]

**Command Used**:
```bash
[Command]
```

**Job ID**: [To be filled]

**Duration**: [To be filled]

**Result**: [COMPLETED/FAILED]

**Error Messages** (if failed):
```
[To be filled if failed]
```

**Resolution** (if failed):
[Analysis and next steps]

---

## Attempt 5 - [DATE] [TIME]

**Status**: [PENDING/IN_PROGRESS/COMPLETED/FAILED]

**Changes from Attempt 4**:
[What was modified]

**Command Used**:
```bash
[Command]
```

**Job ID**: [To be filled]

**Duration**: [To be filled]

**Result**: [COMPLETED/FAILED]

**Final Status**: [✅ Working | ❌ Failed after 5 attempts]

---

## Final Outcome - [Status]

### If Working (✅):

**Success Summary**:
- Working configuration identified in Attempt #: [number]
- Total attempts needed: [number]
- Final node size: [XSMALL/SMALL/MEDIUM/LARGE]
- Runtime: ~[X] minutes for test data
- All expected outputs generated successfully

**Working Configuration**:
```bash
[Final working command and any critical parameters]
```

**Resource Recommendations**:
- Testing/nf-core data: XSMALL
- Production (1-10 samples): SMALL to MEDIUM
- Large cohorts (20+ samples): LARGE

**Next Steps**:
- Deploy to production
- Document in PIPELINE_STATUS.md
- Update STATUS.txt to ✅ Working

---

### If Failed (❌):

**Failure Summary**:
- Attempts exhausted: 5/5
- Final error: [Brief description]
- Root cause: [Analysis of why it failed]

**Detailed Failure Analysis**:
[Comprehensive explanation of what went wrong and why]

**Potential Future Solutions**:
1. [Approach 1 that might work]
2. [Approach 2 that might work]
3. [Approach 3 that might work]

**Blockers Encountered**:
- [Blocker 1]: [Description]
- [Blocker 2]: [Description]

**Recommendation**:
[Should this be revisited later? Are there platform limitations? Alternative approaches?]

---

## Lessons Learned

### Key Insights:
1. [Insight about taxprofiler configuration]
2. [Insight about resource requirements]
3. [Insight about Camber platform specifics]
4. [Insight about test data]

### Configuration Patterns:
- [Pattern that worked or didn't work]
- [Critical parameter combinations]
- [Resource allocation lessons]

### Common Issues:
- [Issue 1]: [How to avoid/fix]
- [Issue 2]: [How to avoid/fix]

### Best Practices:
1. [Best practice 1]
2. [Best practice 2]
3. [Best practice 3]

---

## Technical Notes

### Command Structure:
- Pipeline: `nextflow run nf-core/taxprofiler`
- Version: `-r 1.2.3`
- Profile: `-profile singularity` (not docker - Camber requires Singularity)
- Platform config: `-c /etc/mpi/nextflow.camber.config`
- No separate custom config file (all params in command line)

### Critical Parameters:
- `--run_kraken2`: Enable Kraken2
- `--run_bracken`: Enable Bracken abundance refinement
- `--perform_runmerging`: Merge runs per sample
- `--skip_downstream_qc`: Skip optional QC steps
- `--skip_krona`: Skip Krona charts (can be slow)

### Database Requirements:
- Kraken2 database must be pre-built
- Test database provided by nf-core (~1-2MB compressed)
- Production databases much larger (50-100GB)

### Container System:
- Must use Singularity (not Docker)
- Platform handles container management via `/etc/mpi/nextflow.camber.config`

---

## Testing Checklist

- [ ] App created successfully with `camber app create`
- [ ] Job submitted with `camber app run`
- [ ] Job completes with COMPLETED status
- [ ] Kraken2 classification reports generated
- [ ] Bracken abundance estimates produced
- [ ] Standardized TAXPASTA tables created
- [ ] MultiQC report available
- [ ] No critical errors in logs
- [ ] Output files are valid and non-empty
- [ ] Results are scientifically meaningful

---

## References

- nf-core/taxprofiler: https://nf-co.re/taxprofiler
- Test datasets: https://github.com/nf-core/test-datasets/tree/taxprofiler
- Pipeline implementation plan: `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md`
- Node size guidance: `/nextflow/NODE_SIZE_GUIDANCE.md`