# Testing Log: fetchngs - sra-download-rnaseq

**App Name**: fetchngs-sra-download
**Use Case**: Download sequencing data from SRA/ENA/GEO for RNA-seq analysis
**Pipeline Version**: nf-core/fetchngs v1.12.0
**Test Started**: 2025-09-30

---

## Test Configuration

**Test Data**: nf-core test accessions (SRR9984183, SRR13191702)
**Node Size**: XSMALL (4 CPUs, 15GB RAM)
**Expected Runtime**: 5-10 minutes
**Test File**: test_ids.csv (2 accessions)

---

## Attempt 1 - 2025-09-30

**Status**: 🔄 PENDING

**Command**:
```bash
camber app run fetchngs-sra-download \
  --input input="stash://username/fetchngs-test/test_ids.csv" \
  --input output="stash://username/fetchngs-test/results-attempt-1" \
  --input pipeline_format="rnaseq"
```

**Job ID**: TBD

**Configuration**:
- Node Size: XSMALL
- Pipeline Format: rnaseq
- Download Method: FTP (default)
- Test IDs: SRR9984183, SRR13191702

**Execution Details**:
- Start Time: TBD
- End Time: TBD
- Duration: TBD
- Status: TBD

**Output**:
TBD

**Error** (if any):
TBD

**Resolution**:
TBD

---

## Attempt 2 - TBD

(If needed)

---

## Attempt 3 - TBD

(If needed)

---

## Attempt 4 - TBD

(If needed)

---

## Attempt 5 - TBD

(If needed)

---

## Final Outcome

**Status**: 🔄 In Progress
**Total Attempts**: 0/5
**Successful**: TBD

### Summary
Testing not yet started.

### Key Findings
TBD

### Lessons Learned
TBD

### Recommendations for Production
TBD

---

## Configuration Details

### App.json Command
```bash
nextflow run nf-core/fetchngs -r 1.12.0 \
  --input ${input} \
  --outdir ${output} \
  --nf_core_pipeline ${pipeline_format} \
  -profile singularity \
  -c /etc/mpi/nextflow.camber.config
```

### Key Parameters
- No separate config file (all params in command)
- Uses singularity profile (not docker)
- Relies on platform config: /etc/mpi/nextflow.camber.config
- Minimal resource requirements (XSMALL sufficient)

### Expected Success Criteria
- ✅ Job completes with COMPLETED status
- ✅ FastQ files downloaded to output/fastq/
- ✅ Samplesheet generated in output/samplesheet/samplesheet.csv
- ✅ ID mappings created in output/metadata/id_mappings.csv
- ✅ MD5 checksums verified
- ✅ No download failures or network errors

---

## Notes

- This is a lightweight pipeline (no heavy computation)
- Main dependency is network connectivity for downloads
- XSMALL should be sufficient as it's I/O bound, not CPU bound
- Test data consists of very small files for fast testing