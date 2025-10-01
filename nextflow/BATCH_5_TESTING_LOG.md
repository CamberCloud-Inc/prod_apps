# Batch 5: Metagenomics & Viromics - Testing Log

**Date**: 2025-10-01
**Goal**: Test pipelines with nf-core test data before creating apps
**Approach**: Use `-profile test` with nf-core test-datasets

---

## Testing Results Summary

| Pipeline | Version | Test Status | Issue | Resolution |
|----------|---------|-------------|-------|------------|
| **mag** | 3.1.0 | ❌ FAILED | Memory req 6GB > available 3.9GB per process | Needs XLARGE+ or skip memory-heavy processes |
| **viralrecon** | 2.6.0 | ❌ FAILED | Memory req 6GB > available 3.9GB per process | Same memory issue |
| **ampliseq** | - | ⏳ NOT TESTED | - | - |
| **taxprofiler** | - | ⏳ NOT TESTED | - | - |
| **fetchngs** | - | ⏳ NOT TESTED | - | - |

---

## Detailed Test Results

### 1. nf-core/mag (Metagenome Assembly & Binning)

**Version**: 3.1.0
**Test Command**:
```bash
nextflow run nf-core/mag -r 3.1.0 -profile test --outdir mag_test_results
```

**Jobs Tested**:
- Job 4531 (MEDIUM node): FAILED in 6s - cd: /home/camber/test: No such directory
- Job 4532 (MEDIUM node): FAILED in 56s - Memory issue
- Job 4534 (LARGE node): FAILED in 26s - Memory issue

**Errors**:
```
ERROR ~ Error executing process > 'NFCORE_MAG:MAG:KRONA_KRONADB'
Caused by:
  Process requirement exceeds available memory -- req: 6 GB; avail: 3.9 GB
```

```
ERROR ~ Error executing process > 'NFCORE_MAG:MAG:BOWTIE2_PHIX_REMOVAL_BUILD'
Caused by:
  Process requirement exceeds available memory -- req: 6 GB; avail: 3.9 GB
```

**Analysis**:
- Test profile works (downloads data from https://raw.githubusercontent.com/nf-core/test-datasets/mag/)
- Multiple processes require 6GB memory minimum
- LARGE node still only provides 3.9GB available per process
- Platform may have per-process memory limits regardless of node size

**Test Data Used**:
- Input: `https://raw.githubusercontent.com/nf-core/test-datasets/mag/samplesheets/samplesheet.multirun.csv`
- Databases: minigut_kraken.tgz, minigut_cf.tar.gz, BUSCO bacteria_odb10
- PhiX reference: GCA_002596845.1_ASM259684v1_genomic.fna.gz

---

### 2. nf-core/viralrecon (Viral Assembly & Variant Calling)

**Version**: 2.6.0
**Test Command**:
```bash
nextflow run nf-core/viralrecon -r 2.6.0 -profile test --platform illumina --outdir viralrecon_test_results
```

**Jobs Tested**:
- Job 4535 (LARGE node): FAILED in 37s - Memory issue

**Error**:
```
ERROR ~ Error executing process > 'NFCORE_VIRALRECON:ILLUMINA:PREPARE_GENOME:CUSTOM_GETCHROMSIZES'
Caused by:
  Process requirement exceeds available memory -- req: 6 GB; avail: 3.9 GB

Command:
  samtools faidx nCoV-2019.reference.fasta
  cut -f 1,2 nCoV-2019.reference.fasta.fai > nCoV-2019.reference.fasta.sizes
```

**Analysis**:
- Even simple processes (samtools faidx) request 6GB
- Same per-process memory limit issue as MAG
- Pipeline itself is fine, platform memory allocation is the constraint

---

## Platform Memory Constraints

**Discovered Issue**: Camber platform appears to limit per-process memory to **3.9 GB** regardless of node size chosen.

**Evidence**:
- MEDIUM node: 3.9GB available per process
- LARGE node: Still 3.9GB available per process
- Multiple different processes fail with same "req: 6 GB; avail: 3.9 GB" error

**Node Sizes Tested**:
- MEDIUM: 28GB total RAM, 14 CPUs → 3.9GB per process
- LARGE: (higher total) → Still 3.9GB per process

**Implication**: Many nf-core pipelines with `-profile test` cannot run as-is on platform due to conservative default memory requests (often 6GB minimum per process).

---

## Workarounds

### Option 1: Skip Memory-Heavy Processes
```bash
nextflow run nf-core/mag -r 3.1.0 -profile test \
  --skip_krona \
  --skip_quast \
  --skip_busco \
  --outdir results
```

### Option 2: Custom Config to Override Memory
Create `custom.config`:
```nextflow
process {
  memory = { 3.GB * task.attempt }
  maxRetries = 3
}
```

Run with:
```bash
nextflow run nf-core/mag -r 3.1.0 -profile test -c custom.config
```

### Option 3: Use Smaller Test Datasets
Some pipelines may have "test_small" or similar profiles.

---

## Recommendations

### For App Deployment

1. **Document Memory Requirements**: Clearly state in app descriptions that some pipelines need XLARGE+ nodes
2. **Custom Configs**: Provide platform-optimized config files that reduce memory requests
3. **Skip Options**: Expose skip parameters (e.g., `--skip_krona`, `--skip_busco`) in app specs
4. **Alternative Pipelines**: For metagenomics, consider lighter alternatives or custom workflows

### Pipelines Likely to Work

Based on previous successes:
- ✅ **scrnaseq**: Tested and working (Job 4145)
- ✅ **chipseq, atacseq, methylseq**: Likely work (simpler peak calling)
- ⚠️ **mag, taxprofiler**: Need memory workarounds
- ⚠️ **viralrecon**: Need memory workarounds

### Next Steps

1. Test with custom memory configs
2. Try simpler pipelines (ampliseq, fetchngs)
3. Contact Camber support about per-process memory limits
4. Create apps with skip parameters exposed

---

## Test Data Branches Confirmed

All pipelines have test data in nf-core/test-datasets:
- ✅ `mag` branch exists
- ✅ `viralrecon` branch exists
- ✅ `ampliseq` branch exists
- ✅ `taxprofiler` branch exists

---

*Testing Log - 2025-10-01*
