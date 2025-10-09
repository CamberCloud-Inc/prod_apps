# Nextflow Apps Testing Log
## Testing Date: 2025-09-30
## Tester: Claude (david40962)
## Environment: Camber Cloud Platform

---

## Summary
This log documents comprehensive testing of 4 Nextflow applications on the Camber Cloud Platform:
- 2x CUT&RUN apps (Histone Modifications & Low-Input TF Mapping)
- 2x Nanoseq apps (RNA Isoform Detection & Bacterial Genome Assembly)

---

## 1. CUT&RUN: Histone Modification Mapping
**App Name:** `cutandrun-histone-modifications`
**Pipeline:** nf-core/cutandrun v3.2.2
**Location:** `/Users/david/git/prod_apps/nextflow/cutandrun/histone-modifications/`

### Testing Attempts

#### Attempt 1: FAILED (Job 4474)
- **Status:** FAILED
- **Job ID:** 4474
- **Duration:** 22 seconds
- **Error:** Config file not found
  ```
  The specified configuration file does not exist: /home/camber/histone-cutandrun.config
  ```
- **Root Cause:** The config file `histone-cutandrun.config` was referenced in the command but not available in the execution directory
- **Fix Applied:** Updated app.json to use git clone approach to fetch config file from GitHub repo

#### Attempt 2: FAILED (Job 4485)
- **Status:** FAILED
- **Job ID:** 4485
- **Duration:** 27 seconds
- **Error:** Input validation failed
  ```
  ERROR: Validation of pipeline parameters failed!
  * --input: the file or directory 'https://raw.githubusercontent.com/nf-core/test-datasets/cutandrun/samplesheet/v3.0/samplesheet_test.csv' does not exist.
  ```
- **Root Cause:** After cd-ing into output directory, the working directory context changed and nf-core/cutandrun couldn't validate the remote URL
- **Recommendation:** The command structure needs revision - either:
  1. Keep working directory at /home/camber and copy config there
  2. Use -work-dir parameter to maintain nextflow work directory
  3. Pre-download the samplesheet to local filesystem

### Configuration Files
- **histone-cutandrun.config:** Contains process-specific resource allocation optimized for histone mark analysis
  - Low processes: 2 CPUs, 12GB RAM, 4h
  - Medium processes: 6 CPUs, 36GB RAM, 8h
  - High processes: 12 CPUs, 72GB RAM, 16h
  - Bowtie2 alignment: 8 CPUs, 32GB RAM, 8h
  - MACS2/SEACR peak calling: 2-4 CPUs, 16-24GB RAM

### Test Data
- **Samplesheet:** https://raw.githubusercontent.com/nf-core/test-datasets/cutandrun/samplesheet/v3.0/samplesheet_test.csv
- **Genome:** GRCh38
- **Parameters:**
  - Peak callers: SEACR + MACS2
  - MACS2 mode: Broad peaks (for H3K27me3-like marks)
  - IgG control: Enabled
  - Min alignment Q: 20
  - Fragment size: 120bp

### Issues Found
1. **BUG:** Config file distribution - needs to be accessible in execution directory
2. **BUG:** Command structure incompatible with directory changes and remote URLs

### Status: ❌ FAILED - Requires fix

---

## 2. CUT&RUN: Low-Input TF Mapping
**App Name:** `cutandrun-low-input-tf`
**Pipeline:** nf-core/cutandrun v3.2.2
**Location:** `/Users/david/git/prod_apps/nextflow/cutandrun/low-input-tf-mapping/`

### Testing Attempts

#### Attempt 1: RUNNING (Job 4477)
- **Status:** RUNNING (still executing after 3+ minutes)
- **Job ID:** 4477
- **Start Time:** 2025-09-30 17:22:24Z
- **Node Size:** XSMALL (4 CPUs, 15GB RAM)
- **Pipeline Progress:**
  - ✅ Samplesheet validation completed
  - ✅ Genome preparation started
  - ✅ Chromatin sizes calculation
  - ✅ GTF to BED conversion
  - ✅ FASTQC and TrimGalore processes launched
  - ✅ Bowtie2 index staging from s3://ngi-igenomes
  - ⏳ Currently processing: Alignment and trimming steps

### Configuration Files
- **platform-constrained-config.config:** Resource constraints config successfully fetched from GitHub

### Test Data
- **Samplesheet:** https://raw.githubusercontent.com/nf-core/test-datasets/cutandrun/samplesheet_2_0/test-GSE145187-small.csv
- **Genome:** GRCh38
- **Samples:** H3K27me3 + IgG control
- **Parameters:**
  - Peak caller: SEACR only
  - IgG control: Enabled
  - Mitochondrial filtering: Enabled (chrM)
  - Duplicate removal: Enabled
  - Min alignment Q: 20

### Command Structure
```bash
mkdir -p ${outputDir} && cd ${outputDir} && \
rm -rf prod_apps && \
git clone https://github.com/CamberCloud-Inc/prod_apps.git && \
cp prod_apps/nextflow/cutandrun/low-input-tf-mapping/platform-constrained-config.config ./ && \
rm -rf prod_apps && \
nextflow run nf-core/cutandrun -r 3.2.2 \
  --input ${input} \
  --outdir results \
  --peakcaller ${peakcaller} \
  --use_control ${use_control} \
  --genome ${genome} \
  --mito_name ${mito_name} \
  --minimum_alignment_q_score ${min_alignment_q} \
  --remove_linear_duplicates ${remove_duplicates} \
  --remove_mitochondrial_reads ${remove_mito} \
  -c /etc/mpi/nextflow.camber.config \
  -c platform-constrained-config.config \
  -profile k8s \
  -ansi-log false
```

### Success Factors
1. ✅ Git clone approach successfully fetches config file
2. ✅ Remote URL samplesheet works correctly with nf-core/cutandrun
3. ✅ Pipeline initialization successful
4. ✅ iGenomes reference data accessible via S3

### Status: ⏳ IN PROGRESS - Looking promising

---

## 3. Nanoseq: RNA Isoform Detection
**App Name:** `nanoseq-rna-isoform-detection`
**Pipeline:** nf-core/nanoseq v3.1.0
**Location:** `/Users/david/git/prod_apps/nextflow/nanoseq/rna-isoform-detection/`

### Testing Attempts

#### Attempt 1: FAILED (Job 4481)
- **Status:** FAILED
- **Job ID:** 4481
- **Duration:** 21 seconds
- **Error:** Parameter validation failed
  ```
  ERROR: Validation of pipeline parameters failed!
  * --outdir: expected type: String, found: Boolean (true)
  ```
- **Root Cause:** Parameter naming mismatch - the command uses `${outdir}` but the spec defines parameter as `outputDir`
- **Fix Applied:** Updated app.json command from `--outdir ${outdir}` to `--outdir ${outputDir}`

### Issues Found
1. **BUG:** Parameter name mismatch between command and spec
   - Command template used: `${outdir}`
   - Spec parameter name: `outputDir`
   - Result: Parameter not substituted, defaulting to boolean `true`

### Test Data
- **Samplesheet:** https://raw.githubusercontent.com/nf-core/test-datasets/nanoseq/samplesheet_nobc_dx.csv
- **Protocol:** cDNA (Direct cDNA sequencing)
- **Quantification:** Bambu (context-aware isoform discovery)
- **Skipped:** Demultiplexing, BigBed, BigWig, fusion analysis, modification analysis, differential analysis

### Configuration
```json
{
  "input": "https://raw.githubusercontent.com/nf-core/test-datasets/nanoseq/samplesheet_nobc_dx.csv",
  "outputDir": "stash://david40962/nanoseq-rna-test-results",
  "quantification_method": "bambu",
  "skip_demultiplexing": "true",
  "skip_quantification": "false"
}
```

### Status: ❌ FAILED - Fix applied, needs retest

---

## 4. Nanoseq: Bacterial Genome Assembly
**App Name:** `bacterial_genome_assembly`
**Pipeline:** nf-core/bacass v2.3.1
**Location:** `/Users/david/git/prod_apps/nextflow/nanoseq/bacterial-genome-assembly/`

### Testing Attempts

#### App Creation: FAILED (Validation Error)
- **Status:** NOT TESTED
- **Error:** API validation failed during app creation
  ```
  Error: API error: code=1, message=Validation failed
  ```
- **Root Cause:** Missing required field `title` in app.json
- **Fix Applied:** Added `"title": "Nanoseq: Bacterial Genome Assembly"` to app.json

### Issues Found
1. **BUG:** Missing `title` field in app.json (required by Camber API)
2. **CONCERN:** Complex command structure with SSH git clone and bash script execution
   - Uses: `git clone git@github.com:CamberCloud-Inc/prod_apps.git`
   - Requires SSH keys configured
   - Executes external bash script: `run_assembly.sh`

### Configuration Complexity
The app uses a multi-layered approach:
1. Git clone entire prod_apps repo
2. Execute `run_assembly.sh` script
3. Script hard-codes many parameters
4. Creates samplesheet.csv dependency

This approach has several issues:
- Requires SSH authentication
- Less transparent to users
- Hard to debug
- Doesn't follow convention of other apps

### Recommendations
1. Simplify command structure similar to other apps
2. Remove bash script dependency
3. Pass parameters directly to nextflow command
4. Use HTTPS git clone instead of SSH

### Status: ❌ BLOCKED - Needs restructuring

---

## Platform Observations

### Camber CLI Behavior
1. **Node Size:** Must be lowercase (e.g., `xsmall` not `XSMALL`)
2. **Input Parameters:** Use `--input key=value` format (not `--param`)
3. **Hidden Parameters:** System size in jobConfig is hidden and shouldn't be passed as input
4. **No Update Command:** Must delete and recreate apps to update

### Nextflow Integration
1. **Config Files:** Need to be present in execution directory
2. **Profile:** Backend automatically adds `-profile k8s`
3. **Working Directory:** Changes to output directory affect relative paths
4. **iGenomes:** Accessible via s3://ngi-igenomes URLs
5. **Remote Samplesheets:** Work correctly with URLs when in proper working directory

### Resource Constraints
- XSMALL nodes (4 CPUs, 15GB RAM) suitable for test data
- Max resources available from config:
  - CPUs: 64
  - Memory: 360 GB
  - Time: 24 hours

---

## Key Findings & Recommendations

### Working Patterns
1. ✅ **Git Clone Approach:** Successfully distributes config files
   ```bash
   git clone https://github.com/CamberCloud-Inc/prod_apps.git && \
   cp prod_apps/path/to/config.config ./ && \
   rm -rf prod_apps
   ```

2. ✅ **URL Samplesheets:** Work with nf-core pipelines when in correct working directory

3. ✅ **Parameter Passing:** Direct parameter substitution in nextflow commands

### Failing Patterns
1. ❌ **Config Reference Without Distribution:** Config files must be present in execution directory
2. ❌ **Directory Change + URL Validation:** Some pipelines fail to validate remote URLs after cd
3. ❌ **Parameter Name Mismatches:** Command templates must match spec parameter names exactly

### Required Fixes

#### High Priority
1. **Histone Modifications App:** Fix command structure to handle config distribution and URL validation
2. **RNA Isoform App:** Already fixed - parameter name corrected to `outputDir`
3. **Bacterial Assembly App:** Major restructuring needed - remove bash script dependency

#### Medium Priority
1. Add proper error handling and validation
2. Document config file requirements in app descriptions
3. Standardize command structures across all apps

#### Low Priority
1. Optimize resource allocations based on actual usage
2. Add more test data options
3. Improve parameter descriptions

---

## Test Environment Details
- **Platform:** Camber Cloud
- **Username:** david40962
- **Stash:** stash://david40962/
- **Nextflow Version:** 24.10.5 (platform-managed)
- **Profile:** k8s (automatically added by backend)
- **Container Engine:** Singularity

---

## Next Steps
1. ⏳ Wait for Job 4477 completion to verify low-input-tf app fully works
2. 🔧 Fix histone-modifications app command structure
3. ✅ Retest rna-isoform-detection with fixed parameter name
4. 🔨 Restructure bacterial-genome-assembly app
5. 📝 Update all STATUS.txt files
6. 💾 Commit all fixes to git

---

## Files Modified
- ✏️ `/Users/david/git/prod_apps/nextflow/cutandrun/histone-modifications/app.json` - Added git clone for config distribution
- ✏️ `/Users/david/git/prod_apps/nextflow/nanoseq/rna-isoform-detection/app.json` - Fixed parameter name `outdir` → `outputDir`
- ✏️ `/Users/david/git/prod_apps/nextflow/nanoseq/bacterial-genome-assembly/app.json` - Added missing `title` field

---

## Jobs Log
| Job ID | App | Status | Duration | Notes |
|--------|-----|--------|----------|-------|
| 4474 | cutandrun-histone-modifications | ❌ FAILED | 22s | Config file not found |
| 4477 | cutandrun-low-input-tf | ⏳ RUNNING | 3m+ | Progressing successfully |
| 4481 | nanoseq-rna-isoform-detection | ❌ FAILED | 21s | Parameter type mismatch |
| 4485 | cutandrun-histone-modifications (v2) | ❌ FAILED | 27s | Input URL validation failed |

---

*End of Testing Log - 2025-09-30*
