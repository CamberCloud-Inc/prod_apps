# Quick Start Guide: Implementing a New nf-core Pipeline App

This guide walks you through creating a new app from an nf-core pipeline following our standardized approach.

## Before You Start

**Read these documents first**:
1. `/NEXTFLOW-DEVELOPMENT.md` - Complete development patterns
2. `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md` - Overall strategy and pipeline list
3. `/nextflow/_templates/` - All template files

**Prerequisites**:
- Familiarity with Nextflow basics
- Understanding of the biological use case
- Access to test data

---

## Step-by-Step Workflow

### Phase 1: Research (1-2 hours per pipeline)

#### 1. Choose Your Pipeline

Check `PIPELINE_IMPLEMENTATION_PLAN.md` for priority and select an unimplemented pipeline.

```bash
# Check current status
cat /Users/david/git/prod_apps/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md | grep "🔲 Todo"
```

#### 2. Create Pipeline Directory

```bash
cd /Users/david/git/prod_apps/nextflow
mkdir -p {pipeline}
cd {pipeline}
```

#### 3. Clone Pipeline for Reference

```bash
# In a separate location (not in prod_apps)
cd ~/git
git clone https://github.com/nf-core/{pipeline}.git
cd {pipeline}

# Review documentation
cat README.md
open docs/usage.md
cat nextflow_schema.json | jq '.definitions'
```

#### 4. Create Status Files from Templates

```bash
cd /Users/david/git/prod_apps/nextflow/{pipeline}

# Copy templates
cp ../_templates/PIPELINE_STATUS.template.md ./PIPELINE_STATUS.md
cp ../_templates/USE_CASES.template.md ./USE_CASES.md
touch IMPLEMENTATION_LOG.md

# Edit PIPELINE_STATUS.md
# - Replace {pipeline-name} with actual name
# - Fill in version, summary
# - Update from nf-co.re/{pipeline}
```

#### 5. Research & Document Use Cases

Edit `USE_CASES.md` to identify 5-15 biological use cases:

**Research Sources**:
- nf-core documentation: https://nf-co.re/{pipeline}
- Scientific literature: Search "{pipeline} use cases" or "{biological field} analysis"
- GitHub issues: https://github.com/nf-core/{pipeline}/issues
- nf-core Slack: https://nfcore.slack.com

**For Each Use Case, Document**:
- Biological question it addresses
- Target audience (who would use this)
- Typical experimental design
- Parameters to hardcode vs expose
- Tools/algorithms to use
- Expected outputs
- Priority (P0-P3)

**Example**:
```markdown
### Use Case 1: Transcription Factor Binding Sites (ChIP-seq)

**Biological Question**: Where does transcription factor X bind in the genome?

**Target Audience**: Molecular biologists studying gene regulation

**Typical Experimental Design**:
- Sample type: ChIP DNA from cells expressing TF of interest
- Data type: Illumina paired-end 75bp or 150bp
- Scale: 2-10 samples (TF + input control, multiple conditions)

**Key Parameters**:
- Hardcoded:
  - Peak type: narrow (MACS2 default)
  - q-value: 0.05
  - Fragment size: auto-detect
- Exposed:
  - Sample sheet (ChIP and input pairs)
  - Reference genome
  - Output directory

**Tools**: MACS2 (narrow peak calling), BWA-MEM (alignment)

**Priority**: P0 (most common ChIP-seq use case)
```

#### 6. Prioritize Use Cases

In `USE_CASES.md`, order use cases by:
1. **Frequency of use** (most common first)
2. **Availability of test data**
3. **Clarity of requirements**
4. **Biological impact**

---

### Phase 2: Implementation (2-4 hours per app)

#### 1. Create Use Case Directory

```bash
cd /Users/david/git/prod_apps/nextflow/{pipeline}
mkdir -p {usecase}
cd {usecase}
```

#### 2. Create Configuration File

```bash
# Start from working example
cp ../../scrnaseq/scrnaseq-10xv3-config.config ./{pipeline}-{usecase}-config.config

# Edit for your use case
```

**Key Configuration Sections**:

```groovy
// 1. Process Resources (adjust for your pipeline)
process {
  withLabel:process_low {
    cpus   = { 2     * task.attempt }
    memory = { 12.GB * task.attempt }
    time   = { 4.h   * task.attempt }
  }

  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }

  withLabel:process_high {
    cpus   = { 12    * task.attempt }
    memory = { 72.GB * task.attempt }
    time   = { 16.h  * task.attempt }
  }

  // Specific process overrides (check pipeline for process names)
  withName:'.*:PROCESS_NAME.*' {
    cpus   = { 8     * task.attempt }
    memory = { 48.GB * task.attempt }
    time   = { 12.h  * task.attempt }
  }
}

// 2. Container Configuration (CRITICAL - always include)
singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false  // Must be false on Camber
}

// 3. Use-Case Specific Parameters (hardcode everything you can)
params {
  // Hardcoded for this use case
  parameter1 = 'value1'
  parameter2 = true

  // Skip irrelevant tools
  skip_tools = 'tool1,tool2'
}
```

#### 3. Find or Create Test Data

**Option A: Use nf-core test data** (preferred - always try this first!)

The nf-core community maintains test datasets for most pipelines at:
https://github.com/nf-core/test-datasets

**Each pipeline has its own branch** with curated test data:

```bash
# Check available branches (pipelines)
git ls-remote --heads https://github.com/nf-core/test-datasets

# Clone specific pipeline branch
git clone -b {pipeline} --single-branch https://github.com/nf-core/test-datasets.git test-datasets-{pipeline}

# Example for chipseq
git clone -b chipseq --single-branch https://github.com/nf-core/test-datasets.git test-datasets-chipseq

# Browse test data
cd test-datasets-{pipeline}
ls -la
```

**Common test data locations in each branch**:
- Root directory: Test FASTQ files, samplesheets
- `test/`: Minimal test datasets
- `testdata/`: Alternative test data
- `README.md`: Descriptions of test data

**How to use test data**:

1. **Find the test samplesheet** (usually in pipeline repo):
   ```bash
   # Check pipeline's test configuration
   cd ~/git/{pipeline}  # Your cloned pipeline repo
   cat conf/test.config
   # Look for: params.input = 'https://...'
   ```

2. **Download test samplesheet directly**:
   ```bash
   # Example from nf-core/chipseq
   curl -L -o test_samplesheet.csv \
     "https://raw.githubusercontent.com/nf-core/test-datasets/chipseq/samplesheet/v2.0/samplesheet_test.csv"
   ```

3. **Or create samplesheet pointing to test data**:
   ```bash
   # Use URLs from test-datasets repository
   # Example for chipseq:
   cat > test_samplesheet.csv << 'EOF'
   sample,fastq_1,fastq_2,antibody,control
   WT_BCATENIN_IP,https://raw.githubusercontent.com/nf-core/test-datasets/chipseq/testdata/SRR389222_sub1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/chipseq/testdata/SRR389222_sub2.fastq.gz,BCATENIN,WT_INPUT
   WT_INPUT,https://raw.githubusercontent.com/nf-core/test-datasets/chipseq/testdata/SRR389226_sub1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/chipseq/testdata/SRR389226_sub2.fastq.gz,,
   EOF
   ```

**Benefits of nf-core test data**:
- ✅ Known to work with the pipeline
- ✅ Small file sizes (fast testing)
- ✅ Exercises all major features
- ✅ Community-validated
- ✅ Already used by pipeline CI/CD

**Option B: Create minimal test samplesheet** (only if no test data available)

```bash
# Create test_samplesheet.csv
# Use smallest possible data that exercises the pipeline
# Synthetic or highly subsampled data
```

**Option C: Use pipeline's built-in test profile** (for initial testing only)

```bash
# Many pipelines have a test profile that downloads test data automatically
# In your command:
nextflow run nf-core/{pipeline} -profile test,singularity -c config.config
# Note: This may not work on Camber platform due to dynamic data download
```

**Save as**: `test_samplesheet.csv` in your `{usecase}/` directory

**Important Notes**:
- Always prefer nf-core test-datasets (Option A)
- Check the pipeline's specific branch: `https://github.com/nf-core/test-datasets/tree/{pipeline}`
- If the branch doesn't exist, check `conf/test.config` in the pipeline repo for test data URLs
- Small test data = faster iteration during development

#### 4. Create app.json

```bash
# Copy template (edit all {placeholders})
cp ../../_templates/README.template.md ./README.md
```

Then create `app.json`:

```json
{
  "name": "{pipeline}-{usecase}",
  "title": "{Biology-Focused Title}",
  "description": "{1-2 sentence description in plain language for biologists}",
  "content": "{HTML content - see template or examples}",
  "imageUrl": "https://raw.githubusercontent.com/nf-core/{pipeline}/master/docs/images/{pipeline}_logo.png",
  "command": "nextflow run nf-core/{pipeline} --input ${input} --outdir ${output} --genome ${genome} --param1 value1 --param2 value2 -r X.Y.Z -c /etc/mpi/nextflow.camber.config -c {pipeline}-{usecase}-config.config",
  "engineType": "NEXTFLOW",
  "jobConfig": [
    {
      "type": "Select",
      "label": "System Size",
      "name": "system_size",
      "hidden": true,
      "options": [
        {
          "label": "Small - Test datasets",
          "value": "small",
          "mapValue": {"nodeSize": "SMALL", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "Medium - {use case}",
          "value": "medium",
          "mapValue": {"nodeSize": "MEDIUM", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "Large - {use case} (Recommended)",
          "value": "large",
          "mapValue": {"nodeSize": "LARGE", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "XLarge - {use case}",
          "value": "xlarge",
          "mapValue": {"nodeSize": "XLARGE", "numNodes": 1, "withGpu": false}
        }
      ],
      "defaultValue": "large"
    }
  ],
  "spec": [
    {
      "type": "Stash File",
      "label": "Sample Information Sheet",
      "name": "input",
      "description": "CSV file with format: {describe columns}. Each row represents {description}.",
      "required": true
    },
    {
      "type": "Stash File",
      "label": "Output Directory",
      "name": "output",
      "description": "Where to save analysis results and reports",
      "defaultValue": "./{pipeline}-results",
      "required": true
    },
    {
      "type": "Select",
      "label": "Reference Genome",
      "name": "genome",
      "description": "Genome matching your organism (use GRCh38 for human)",
      "defaultValue": "GRCh38",
      "options": [
        {"label": "Human GRCh38/hg38 (latest)", "value": "GRCh38"},
        {"label": "Human GRCh37/hg19 (legacy)", "value": "GRCh37"},
        {"label": "Mouse GRCm39/mm39 (latest)", "value": "GRCm39"}
      ]
    }
  ],
  "tags": [
    {"name": "genomics", "type": "subfield"},
    {"name": "{analysis-type}", "type": "task"},
    {"name": "biology", "type": "field"}
  ]
}
```

**Critical**: Write biology-focused content section (see NEXTFLOW-DEVELOPMENT.md)

#### 5. Create README.md

```bash
# Copy and fill in template
cp ../../_templates/README.template.md ./README.md

# Edit all sections thoroughly
```

#### 6. Initialize TESTING_LOG.md

```bash
cp ../../_templates/TESTING_LOG.template.md ./TESTING_LOG.md

# Fill in header information
```

#### 7. Create STATUS.txt

```bash
echo "🔄 Testing - Implementation complete, testing in progress" > STATUS.txt
```

---

### Phase 3: Testing (2-8 hours per app, up to 5 attempts)

#### Attempt 1: Initial Test

**1. Upload test files**
```bash
cd /Users/david/git/prod_apps/nextflow/{pipeline}/{usecase}

camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
camber stash cp {pipeline}-{usecase}-config.config stash://username/test-{pipeline}/

# Verify
camber stash ls test-{pipeline}/
```

**2. Create app**
```bash
camber app create --file app.json
```

**3. Run test**
```bash
camber app run {pipeline}-{usecase} \
  --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
  --input output="stash://username/test-{pipeline}/results-attempt-1" \
  --input genome="GRCh38"

# Note the Job ID: XXXX
```

**4. Monitor**
```bash
# Check every 5-10 minutes
camber job get XXXX

# When done (COMPLETED or FAILED)
camber job logs XXXX > attempt-1-logs.txt
```

**5. Document in TESTING_LOG.md**
- Copy the "Attempt 1" section from template
- Fill in all details: commands, job ID, status, errors, etc.
- Add error messages from logs
- Diagnose the issue
- Plan resolution for Attempt 2

#### Attempts 2-5: Debug and Fix

**Common Issues & Fixes**:

**Issue: "docker: command not found"**
```groovy
// In config file, ensure:
docker { enabled = false }
singularity { enabled = true; autoMounts = true }
```

**Issue: OutOfMemoryError**
```groovy
// Increase memory for problematic process
withName:'.*:PROCESS_NAME.*' {
  memory = { 96.GB * task.attempt }  // Was 72GB
}
// Or increase jobConfig node size
```

**Issue: "File not found"**
- Check samplesheet paths are correct
- Verify files uploaded to stash
- Use relative paths if files in same dir as samplesheet

**Issue: Process timeout**
```groovy
// Increase time limit
withName:'.*:SLOW_PROCESS.*' {
  time = { 48.h * task.attempt }  // Was 24h
}
```

**For Each Attempt**:
1. Make changes based on previous error
2. Update app if needed: `camber app delete {app-name} && camber app create --file app.json`
3. Upload updated config if changed
4. Run test with new attempt number in output path
5. Monitor and get logs
6. Document everything in TESTING_LOG.md
7. If fixed: Proceed to Phase 4
8. If not fixed and <5 attempts: Try again
9. If 5 attempts exhausted: Mark as failed

---

### Phase 4: Success or Failure

#### If Working (Status: COMPLETED, outputs look good)

**1. Update STATUS.txt**
```bash
echo "✅ Working - Tested and verified" > STATUS.txt
```

**2. Final Documentation**
- Complete TESTING_LOG.md "Final Outcome" section
- Update README.md with actual runtime from test
- Verify all files are complete

**3. Deploy to Production**
```bash
# If not already deployed
camber app create --file app.json
```

**4. Update PIPELINE_STATUS.md**
```markdown
1. **{usecase}** - ✅ Working
   - Directory: `{usecase}/`
   - Tested: YYYY-MM-DD
   - Runtime: ~X hours
```

**5. Commit to Git**
```bash
git add .
git commit -m "pipeline/{pipeline}: {usecase} app working - all tests passed"
git push
```

#### If Failed After 5 Attempts

**1. Update STATUS.txt**
```bash
echo "❌ Failed - 5 attempts exhausted, see TESTING_LOG.md" > STATUS.txt
```

**2. Complete TESTING_LOG.md**
- Fill in "Final Outcome - Failed" section
- Document root cause clearly
- Note any potential future solutions

**3. Update PIPELINE_STATUS.md**
```markdown
1. **{usecase}** - ❌ Failed
   - Directory: `{usecase}/`
   - Attempts: 5
   - Reason: {brief reason}
   - Details: See {usecase}/TESTING_LOG.md
```

**4. Commit to Git**
```bash
git add .
git commit -m "pipeline/{pipeline}: {usecase} app failed after 5 attempts - {brief reason}"
git push
```

**5. Move to Next Use Case**

---

## Parallel Work Strategy

### Working Solo
1. Complete one use case fully (research → implement → test)
2. Learn from experience
3. Apply lessons to next use case
4. Build momentum with successes

### Working in Team ("Swarming")

**Option A: Divide by Pipeline**
- Person 1: Pipeline X (all use cases)
- Person 2: Pipeline Y (all use cases)
- Minimizes conflicts

**Option B: Divide by Phase**
- Person 1: Research all pipelines (create USE_CASES.md)
- Person 2-3: Implement apps based on research
- Person 4: Test apps as they're implemented

**Option C: Divide by Use Case**
- All work on same pipeline
- Each person takes different use case
- Requires branch coordination

**Recommended for Teams**: Option A (divide by pipeline)

---

## Quick Reference: File Checklist

Before considering an app complete, verify these files exist and are complete:

### Per Use Case Directory
- [ ] `app.json` - Complete with biology-focused content
- [ ] `{pipeline}-{usecase}-config.config` - Nextflow config
- [ ] `test_samplesheet.csv` - Test data
- [ ] `README.md` - Complete user documentation
- [ ] `TESTING_LOG.md` - All attempts documented
- [ ] `STATUS.txt` - Current status (✅/❌/⚠️)
- [ ] `attempt-N-logs.txt` - Log files from tests (at least 1)

### Per Pipeline Directory
- [ ] `PIPELINE_STATUS.md` - Overview and progress
- [ ] `USE_CASES.md` - All use cases identified
- [ ] `IMPLEMENTATION_LOG.md` - High-level notes
- [ ] One or more `{usecase}/` subdirectories

---

## Time Estimates

**Per Use Case** (Individual work):
- Research: 0.5-1 hour (if USE_CASES.md done)
- Implementation: 2-4 hours
- Testing (if works on attempt 1): 1-2 hours
- Testing (if needs debugging): 4-8 hours
- Documentation: 1-2 hours
- **Total**: 4-15 hours per app

**Per Pipeline** (5-10 use cases):
- Research: 2-4 hours (all use cases)
- Implementation: 10-40 hours (all use cases)
- Testing: 10-80 hours (all use cases)
- **Total**: 22-124 hours per pipeline

**Optimization with Experience**:
- After 3-5 apps: Time per app drops 30-50%
- Reusable config patterns accelerate implementation
- Familiarity with common errors speeds debugging

---

## Success Tips

1. **Start with Test Data** - Don't write configs until you have test data
2. **Copy Working Examples** - Start from scrnaseq config, modify incrementally
3. **Test Early** - Test after every change, don't accumulate changes
4. **Document Everything** - Future you (or others) will thank you
5. **Read Error Logs Carefully** - The answer is usually in the logs
6. **Check nf-core Docs** - Pipeline docs often have common issues/solutions
7. **Use Small Test Data** - Faster iteration during debugging
8. **One Change at a Time** - When debugging, change one thing per attempt
9. **Biology Focus** - Always write for biologists, not bioinformaticians
10. **Take Breaks** - After 2-3 failed attempts, step away and come back fresh

---

## Getting Unstuck

**If stuck on an error for >1 hour**:
1. Search GitHub issues for the pipeline
2. Check nf-core Slack for similar problems
3. Re-read pipeline documentation carefully
4. Try simplifying (remove optional parameters)
5. Compare to working app (e.g., scrnaseq)
6. Ask for help (if working in team)
7. Document well and move to different use case
8. Return with fresh perspective later

**If 5 attempts exhausted**:
- It's okay to mark as failed!
- Document the issue thoroughly
- Someone may solve it in the future
- Move on to make progress elsewhere

---

## Questions?

Refer to:
- `/NEXTFLOW-DEVELOPMENT.md` - Comprehensive guide
- `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md` - Overall strategy
- Working examples in `/nextflow/scrnaseq/`, `/nextflow/sarek/`
- Templates in `/nextflow/_templates/`