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

## Attempt 1 - 2025-09-30 08:55

**Status**: FAILED

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

**Job ID**: 4358

**Node Size**: XSMALL (4 CPUs, 15GB RAM)

**Duration**: ~2 minutes (failed early)

**Result**: FAILED

**Error Messages**:
```
ERROR ~ Error executing process > 'NFCORE_TAXPROFILER:TAXPROFILER:UNTAR (2)'

Caused by:
  Failed to pull singularity image
    command: singularity pull  --name depot.galaxyproject.org-singularity-ubuntu-22.04.img.pulling.1759222538778 https://depot.galaxyproject.org/singularity/ubuntu:22.04 > /dev/null
    status : 127
    message:
      bash: line 1: singularity: command not found
```

**Resolution**: The error was due to using `-profile singularity` explicitly. On Camber, the platform automatically sets the profile to `k8s` and manages containers. The command should not include a profile flag - the backend handles this automatically.

---

## Attempt 2 - 2025-09-30 08:57

**Status**: FAILED

**Changes from Attempt 1**:
Removed explicit `-profile singularity` from command, letting Camber backend handle profile automatically.

**Command Used**:
```bash
# Updated app.json command (no explicit profile)
nextflow run nf-core/taxprofiler --input ${input} --databases ${databases} --outdir ${output} --run_kraken2 --run_bracken --perform_runmerging -r 1.2.3 -c /etc/mpi/nextflow.camber.config
```

**Job ID**: 4360

**Duration**: ~1 minute (failed early)

**Result**: FAILED

**Error Messages**:
Same singularity error - issue was the logs were from previous cached attempt.

**Resolution**: Need to ensure clean run without cached failures.

---

## Attempt 3 - 2025-09-30 09:10

**Status**: PARTIALLY SUCCESSFUL (interrupted)

**Changes from Attempt 2**:
Clean test run after understanding Camber profile handling.

**Command Used**:
```bash
camber app run taxprofiler-microbiome-kraken2 \
  --input input="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/samplesheet.csv" \
  --input databases="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/database_v1.2.csv" \
  --input output="./test-taxprofiler/attempt3-results"
```

**Job ID**: Unknown (from previous session)

**Duration**: Unknown (was running successfully but interrupted)

**Result**: INTERRUPTED

**Notes**:
Pipeline was running successfully with all processes submitting correctly (UNTAR, FASTQC, KRAKEN2, BRACKEN, MULTIQC all submitted). Logs showed:
```
[5d/d4742c] Submitted process > NFCORE_TAXPROFILER:TAXPROFILER:UNTAR (testdb-kraken2.tar.gz)
[0e/add277] Submitted process > NFCORE_TAXPROFILER:TAXPROFILER:UNTAR (testdb-bracken.tar.gz)
[Multiple FASTQC, KRAKEN2, and BRACKEN processes submitted]
[f1/a5a47f] Submitted process > NFCORE_TAXPROFILER:TAXPROFILER:MULTIQC
```

**Resolution**: Run clean test to completion.

---

## Attempt 4 - 2025-09-30 09:17

**Status**: COMPLETED ✅

**Changes from Attempt 3**:
Clean complete run with monitoring.

**Command Used**:
```bash
camber app create --file app.json
# (with app name: taxprofiler-microbiome-kraken2-david40962)

camber app run taxprofiler-microbiome-kraken2-david40962 \
  --input input="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/samplesheet.csv" \
  --input databases="https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/database_v1.2.csv" \
  --input output="stash://david40962/test-taxprofiler/attempt4-results"
```

**Job ID**: 4392

**Duration**: 4m42s

**Result**: COMPLETED ✅

**Output Check**:
- ✅ Pipeline launched successfully
- ✅ Test databases downloaded and extracted (UNTAR)
- ✅ FASTQC quality control completed
- ✅ MERGE_RUNS completed for multi-run samples
- ✅ Kraken2 classification ran on all samples
- ✅ Bracken abundance estimation completed
- ✅ MultiQC report generated
- ✅ No error messages in final output
- ✅ Pipeline completed successfully message displayed

**Final Log Message**:
```
-[nf-core/taxprofiler] Pipeline completed successfully-
```

**Success!** The pipeline completed successfully on the first clean attempt after understanding the Camber platform requirements.

---

## Final Outcome - ✅ Working

### Success Summary:
- Working configuration identified in Attempt #: 4
- Total attempts needed: 4 (1 was main issue diagnosis, 2 was cached error, 3 was interrupted, 4 succeeded)
- Final node size: XSMALL
- Runtime: 4m42s for test data (6 samples)
- All expected outputs generated successfully

**Working Configuration**:
```bash
# app.json command (critical: no -profile flag, backend handles it)
nextflow run nf-core/taxprofiler \
  --input ${input} \
  --databases ${databases} \
  --outdir ${output} \
  --run_kraken2 \
  --run_bracken \
  --perform_runmerging \
  -r 1.2.3 \
  -c /etc/mpi/nextflow.camber.config

# Key insights:
# 1. NO -profile flag (backend automatically sets to k8s)
# 2. Use /etc/mpi/nextflow.camber.config for platform config
# 3. XSMALL node is sufficient for test data
# 4. All parameters can be passed in command line (no custom config file needed)
```

**Resource Recommendations**:
- Testing/nf-core data: XSMALL (4 CPUs, 15GB RAM) - ✅ Confirmed working
- Production (1-10 samples, standard Kraken2 DB): MEDIUM (32 CPUs, 120GB RAM)
- Large cohorts (20-50 samples): LARGE (64 CPUs, 360GB RAM)
- Note: Resource needs scale with database size and sample count

**Next Steps**:
- ✅ Deploy to production (app created)
- ⏳ Document in PIPELINE_STATUS.md
- ⏳ Update STATUS.txt to ✅ Working
- ⏳ Update app.json to use production name (taxprofiler-microbiome-kraken2)

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