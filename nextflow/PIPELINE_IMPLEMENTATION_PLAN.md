# nf-core Pipeline Implementation Plan

**Goal**: Create biologist-friendly Camber apps for all released nf-core pipelines following the patterns established in `NEXTFLOW-DEVELOPMENT.md`.

**Strategy**: For each pipeline, create 5-15 use-case-specific apps rather than one monolithic app with all parameters exposed.

**Status Tracking**: Each pipeline will have its own subdirectory with status files tracking implementation and testing attempts.

---

## Implementation Priority

Pipelines sorted by biological impact and community usage (approximated based on typical nf-core adoption):

### Tier 1: High-Priority Genomics (Most Used)

These pipelines are widely used and have clear biological use cases.

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **rnaseq** | ✅ Exists | P0 | 8 apps | Bulk RNA sequencing - expand existing |
| **sarek** | ✅ Exists | P0 | 10 apps | Variant calling - expand existing |
| **scrnaseq** | ✅ Exists | P0 | 10 apps | Single-cell RNA - expand existing |
| **chipseq** | 🔲 Todo | P0 | 6 apps | Transcription factor binding, histone marks |
| **atacseq** | ✅ Exists | P0 | 5 apps | Chromatin accessibility - expand existing |
| **methylseq** | ✅ Exists | P1 | 4 apps | DNA methylation - expand existing |
| **cutandrun** | 🔲 Todo | P1 | 4 apps | Low-input ChIP-seq alternative |
| **differentialabundance** | 🔲 Todo | P1 | 4 apps | RNA-seq/proteomics downstream analysis |

### Tier 2: Specialized Genomics

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **ampliseq** | 🔲 Todo | P1 | 3 apps | 16S/ITS microbial sequencing |
| **nanoseq** | 🔲 Todo | P1 | 4 apps | Oxford Nanopore long-read sequencing |
| **crisprseq** | ✅ Exists | P1 | 3 apps | CRISPR screening analysis |
| **mag** | ✅ Exists | P1 | 3 apps | Metagenomics assembly |
| **viralrecon** | 🔲 Todo | P1 | 3 apps | Viral genome reconstruction (COVID-19, etc.) |
| **taxprofiler** | 🔲 Todo | P1 | 3 apps | Taxonomic profiling/classification |
| **fetchngs** | 🔲 Todo | P2 | 2 apps | Download data from public databases |
| **rnafusion** | 🔲 Todo | P1 | 3 apps | Gene fusion detection in RNA-seq |
| **smrnaseq** | 🔲 Todo | P1 | 3 apps | Small RNA sequencing (miRNA, etc.) |
| **splicevariant** | 🔲 Todo | P2 | 3 apps | Alternative splicing analysis |

### Tier 3: Structural & Long-Read

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **variantbenchmarking** | 🔲 Todo | P2 | 2 apps | Benchmark variant callers |
| **pangenome** | 🔲 Todo | P2 | 2 apps | Build pangenome graphs |
| **hlatyping** | 🔲 Todo | P2 | 2 apps | HLA genotyping from NGS |
| **bamtofastq** | 🔲 Todo | P3 | 1 app | Convert BAM to FASTQ |
| **hic** | 🔲 Todo | P2 | 3 apps | Hi-C chromosome conformation |
| **clipseq** | 🔲 Todo | P2 | 2 apps | CLIP-seq RNA-protein interactions |
| **dualrnaseq** | 🔲 Todo | P2 | 2 apps | Host-pathogen dual RNA-seq |

### Tier 4: Proteomics & Metabolomics

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **proteinfold** | 🔲 Todo | P1 | 3 apps | AlphaFold protein structure prediction |
| **mhcquant** | 🔲 Todo | P2 | 2 apps | Mass spec immunopeptidomics |
| **quantms** | 🔲 Todo | P2 | 3 apps | Quantitative proteomics |
| **metaboigniter** | 🔲 Todo | P2 | 2 apps | Metabolomics preprocessing |

### Tier 5: Spatial & Imaging

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **spatialvi** | 🔲 Todo | P1 | 4 apps | Spatial transcriptomics (Visium, etc.) |
| **imaging** | 🔲 Todo | P2 | 3 apps | Imaging mass cytometry |
| **molkart** | 🔲 Todo | P2 | 2 apps | Spatial multimodal analysis |

### Tier 6: Specialized & Emerging

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **bacass** | 🔲 Todo | P2 | 2 apps | Bacterial assembly |
| **funcscan** | 🔲 Todo | P2 | 2 apps | Functional screening annotation |
| **phageannotator** | 🔲 Todo | P3 | 1 app | Bacteriophage annotation |
| **circdna** | 🔲 Todo | P2 | 2 apps | Circular DNA detection |
| **raredisease** | 🔲 Todo | P1 | 4 apps | Rare disease diagnosis pipeline |
| **pgdb** | 🔲 Todo | P3 | 1 app | Prokaryotic genome database |
| **isoseq** | 🔲 Todo | P2 | 2 apps | PacBio Iso-Seq full-length transcripts |
| **scdownstream** | 🔲 Todo | P2 | 4 apps | Single-cell downstream analysis |
| **epitopeprediction** | 🔲 Todo | P2 | 2 apps | T-cell epitope prediction |
| **pathogensurveillance** | 🔲 Todo | P2 | 2 apps | Pathogen genomic surveillance |

### Tier 7: Other Scientific Fields

| Pipeline | Status | Priority | Apps Planned | Notes |
|----------|--------|----------|--------------|-------|
| **airrflow** | 🔲 Todo | P2 | 2 apps | Adaptive immune receptor repertoire |
| **eager** | 🔲 Todo | P3 | 2 apps | Ancient DNA analysis |
| **demultiplex** | 🔲 Todo | P2 | 2 apps | Demultiplex sequencing data |
| **genomeannotator** | 🔲 Todo | P2 | 2 apps | Genome annotation |

---

## Pipeline-Specific Implementation Plans

Each pipeline will have its own directory under `/nextflow/{pipeline}/` with subdirectories for each use-case app.

### Directory Structure Per Pipeline

```
nextflow/
├── {pipeline}/
│   ├── PIPELINE_STATUS.md                    # Overall pipeline status and notes
│   ├── USE_CASES.md                          # Identified use cases for this pipeline
│   ├── IMPLEMENTATION_LOG.md                 # Detailed log of all attempts
│   │
│   ├── {usecase1}/
│   │   ├── app.json
│   │   ├── {pipeline}-{usecase1}-config.config
│   │   ├── test_samplesheet.csv
│   │   ├── README.md
│   │   ├── TESTING_LOG.md                    # Test attempts for this app
│   │   └── STATUS.txt                        # ✅ Working | ⚠️ Issues | ❌ Failed
│   │
│   ├── {usecase2}/
│   │   └── ... (same structure)
│   │
│   └── ... (more use cases)
```

### Status File Format

**PIPELINE_STATUS.md**:
```markdown
# Pipeline: {pipeline-name}

**Latest Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Overall Status**: 🔲 Not Started | 🔄 In Progress | ✅ Complete | ❌ Failed

## Summary
Brief description of pipeline and biological applications.

## Use Cases Identified
1. Use case 1 - [Status]
2. Use case 2 - [Status]
3. ...

## Implementation Progress
- [ ] Research phase complete
- [ ] Use cases defined
- [ ] App 1: {usecase1} - [Status]
- [ ] App 2: {usecase2} - [Status]
- ...

## Issues Encountered
- Issue 1: Description and resolution
- Issue 2: ...

## Success Metrics
- X/Y apps working
- Z/Y apps tested successfully
```

**TESTING_LOG.md** (per app):
```markdown
# Testing Log: {pipeline} - {usecase}

## Attempt 1 - YYYY-MM-DD HH:MM
**Command**: [Camber command used]
**Job ID**: XXXX
**Status**: PENDING | RUNNING | COMPLETED | FAILED
**Duration**: X hours
**Error**: [If failed, error message]
**Resolution**: [What was tried to fix]

## Attempt 2 - YYYY-MM-DD HH:MM
...

## Attempt 3 - YYYY-MM-DD HH:MM
...

## Attempt 4 - YYYY-MM-DD HH:MM
...

## Attempt 5 - YYYY-MM-DD HH:MM
**Final Status**: ✅ Working | ❌ Abandoned after 5 attempts

## Lessons Learned
- Key insight 1
- Key insight 2
- Configuration patterns that worked/didn't work
```

---

## High-Priority Pipeline Details

### 1. chipseq (ChIP-seq)

**Biological Applications**: Identify where transcription factors bind to DNA and map histone modifications across the genome.

**Use Cases to Implement**:
1. **Transcription Factor ChIP-seq** (narrow peaks)
   - Focus: Transcription factor binding sites
   - Tool: MACS2 narrow peak calling
   - Target: Researchers studying gene regulation

2. **Histone Mark ChIP-seq** (broad peaks)
   - Focus: Histone modifications (H3K27me3, H3K4me3, etc.)
   - Tool: MACS2 broad peak calling
   - Target: Epigenetics researchers

3. **ChIP-seq with Input Control**
   - Focus: Standard ChIP with matched input DNA
   - Tool: Full MACS2 with control
   - Target: Standard experimental design

4. **ChIP-seq without Input**
   - Focus: Situations where input control unavailable
   - Tool: Modified peak calling
   - Target: Limited sample situations

5. **Differential Binding Analysis**
   - Focus: Compare ChIP signal between conditions
   - Tool: DiffBind integration
   - Target: Comparative studies

6. **ChIP-seq Quality Assessment**
   - Focus: QC-only mode for assessing library quality
   - Tool: All QC modules, minimal peak calling
   - Target: Library validation

**Key Parameters**:
- Hardcode: Peak calling algorithm, QC thresholds
- Expose: Sample sheet, genome, peak type (narrow/broad), output dir

**Resource Requirements**: MEDIUM (most ChIP-seq), LARGE (very deep sequencing)

**Expected Challenges**:
- Input control handling (paired samples)
- Broad vs narrow peak configuration
- Multiple peak callers available

---

### 2. cutandrun (CUT&RUN)

**Biological Applications**: Low-input alternative to ChIP-seq for studying protein-DNA interactions.

**Use Cases to Implement**:
1. **Low-Input Transcription Factor Mapping**
   - Focus: TF binding with minimal cells
   - Advantage: More sensitive than ChIP-seq

2. **Histone Modification Mapping**
   - Focus: Histone marks with CUT&RUN
   - Advantage: Lower background than ChIP

3. **CUT&Tag Protocol**
   - Focus: Tagmentation-based variant
   - Advantage: Even higher efficiency

4. **Spike-In Normalized Analysis**
   - Focus: Quantitative comparisons using spike-ins
   - Advantage: Absolute quantification

**Key Parameters**:
- Hardcode: CUT&RUN-specific processing, normalization
- Expose: Sample sheet, genome, spike-in genome (optional), output dir

---

### 3. differentialabundance (Differential Expression/Abundance)

**Biological Applications**: Statistical analysis of gene expression or protein abundance differences between conditions.

**Use Cases to Implement**:
1. **RNA-seq Differential Expression**
   - Focus: Two-group comparison (treatment vs control)
   - Tools: DESeq2, edgeR, limma

2. **Time Series Analysis**
   - Focus: Multiple time points
   - Tools: Time-course specific models

3. **Multi-Factor Design**
   - Focus: Complex experimental designs (batch effects, multiple factors)
   - Tools: Model matrices, batch correction

4. **Proteomics Differential Abundance**
   - Focus: Mass spec protein quantification
   - Tools: Limma for proteomics

**Key Parameters**:
- Hardcode: Statistical method, p-value thresholds
- Expose: Count matrix, sample metadata, comparison groups, output dir

---

### 4. ampliseq (16S/ITS Amplicon Sequencing)

**Biological Applications**: Characterize microbial communities from amplicon sequencing.

**Use Cases to Implement**:
1. **16S Bacterial Community Profiling**
   - Focus: Bacterial diversity (V3-V4 or other regions)
   - Target: Microbiome researchers

2. **ITS Fungal Community Profiling**
   - Focus: Fungal diversity
   - Target: Mycobiome studies

3. **18S Eukaryotic Profiling**
   - Focus: Eukaryotic microorganisms
   - Target: Environmental samples

**Key Parameters**:
- Hardcode: Database (SILVA, UNITE), classification method
- Expose: Sample sheet, amplicon type (16S/ITS/18S), output dir

---

### 5. nanoseq (Nanopore Long-Read Sequencing)

**Biological Applications**: Analyze Oxford Nanopore long-read sequencing data for genome assembly, RNA isoforms, and structural variants.

**Use Cases to Implement**:
1. **Genome Assembly** (bacterial/small genomes)
   - Focus: De novo assembly with long reads

2. **Full-Length Transcript Sequencing**
   - Focus: Direct RNA sequencing, isoform detection

3. **Structural Variant Detection**
   - Focus: Large SVs missed by short reads

4. **Targeted Long-Read Sequencing**
   - Focus: Enriched regions (adaptive sampling)

**Key Parameters**:
- Hardcode: Basecalling params, assembly algorithm
- Expose: Sample sheet, analysis type, genome (if mapping), output dir

---

### 6. viralrecon (Viral Genome Reconstruction)

**Biological Applications**: Reconstruct viral genomes from sequencing data (COVID-19, influenza, etc.).

**Use Cases to Implement**:
1. **SARS-CoV-2 Surveillance**
   - Focus: COVID-19 variant identification
   - Target: Public health labs

2. **Influenza Genotyping**
   - Focus: Flu strain identification
   - Target: Seasonal surveillance

3. **Generic Viral Assembly**
   - Focus: Any virus with reference
   - Target: Research labs

**Key Parameters**:
- Hardcode: Assembly method, variant calling
- Expose: Sample sheet, virus type, reference genome, output dir

---

### 7. proteinfold (Protein Structure Prediction)

**Biological Applications**: Predict 3D protein structures using AlphaFold2 and related tools.

**Use Cases to Implement**:
1. **Single Protein Structure Prediction**
   - Focus: AlphaFold2 for single sequences

2. **Protein Complex Prediction**
   - Focus: Multi-chain complexes

3. **Batch Structure Prediction**
   - Focus: Many proteins from proteome

**Key Parameters**:
- Hardcode: AlphaFold version, model type
- Expose: FASTA sequences, prediction mode, output dir

---

### 8. spatialvi (Spatial Transcriptomics)

**Biological Applications**: Analyze spatial gene expression (10x Visium, Slide-seq, etc.).

**Use Cases to Implement**:
1. **10x Visium Analysis**
   - Focus: Standard Visium slides

2. **Slide-seq Analysis**
   - Focus: High-resolution spatial data

3. **Spatial Clustering**
   - Focus: Identify spatial domains

4. **Ligand-Receptor Analysis**
   - Focus: Cell-cell communication in space

**Key Parameters**:
- Hardcode: Platform-specific parameters
- Expose: Sample sheet, platform type, genome, output dir

---

### 9. raredisease (Rare Disease Diagnosis)

**Biological Applications**: Identify disease-causing variants in rare genetic disorders.

**Use Cases to Implement**:
1. **Trio Analysis** (parents + affected child)
   - Focus: De novo mutation detection

2. **Singleton Analysis**
   - Focus: Single affected individual

3. **Compound Heterozygote Detection**
   - Focus: Recessive disease genes

4. **Mitochondrial Variant Analysis**
   - Focus: mtDNA disorders

**Key Parameters**:
- Hardcode: Variant filtering, pathogenicity prediction
- Expose: Sample sheet with pedigree, genome, output dir

---

## Implementation Workflow

### Phase 1: Research & Planning (Per Pipeline)

1. **Review Pipeline Documentation**
   ```bash
   # Clone pipeline repo
   git clone https://github.com/nf-core/{pipeline}.git
   cd {pipeline}

   # Review docs
   cat README.md
   cat docs/usage.md
   cat nextflow_schema.json | jq
   ```

2. **Identify Use Cases**
   - Review scientific literature
   - Check nf-core Slack discussions
   - Consult with domain experts (if available)
   - Document in `USE_CASES.md`

3. **Create Pipeline Directory Structure**
   ```bash
   mkdir -p /Users/david/git/prod_apps/nextflow/{pipeline}
   cd /Users/david/git/prod_apps/nextflow/{pipeline}

   # Create status files
   touch PIPELINE_STATUS.md USE_CASES.md IMPLEMENTATION_LOG.md
   ```

### Phase 2: Implementation (Per Use Case)

1. **Create Use Case Directory**
   ```bash
   mkdir -p {usecase}
   cd {usecase}
   ```

2. **Create Config File**
   - Start from working example (e.g., scrnaseq)
   - Adapt process resources
   - Hardcode use-case-specific parameters
   - Save as `{pipeline}-{usecase}-config.config`

3. **Create app.json**
   - Use biology-focused language
   - Detailed samplesheet instructions
   - Minimal exposed parameters (3-5)
   - Complete HTML content section

4. **Create Test Samplesheet**
   - Use nf-core test data (preferred)
   - Or minimal example data
   - Document in README.md

5. **Create README.md**
   - Use case description
   - Input requirements
   - Expected outputs
   - Testing instructions

6. **Initialize TESTING_LOG.md**
   - Prepare for attempt tracking

### Phase 3: Testing (Up to 5 Attempts)

For each app, follow this testing protocol:

**Attempt Loop** (max 5 attempts):

1. **Upload Test Files**
   ```bash
   camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
   camber stash cp {pipeline}-{usecase}-config.config stash://username/test-{pipeline}/
   ```

2. **Create/Update App**
   ```bash
   # First time
   camber app create --file app.json

   # Updates
   camber app delete {app-name} && camber app create --file app.json
   ```

3. **Run Test**
   ```bash
   camber app run {app-name} \
     --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
     --input output="stash://username/test-{pipeline}/results-attempt-N" \
     --input genome="GRCh38"  # or appropriate

   # Record Job ID
   JOB_ID=XXXX
   ```

4. **Monitor Job**
   ```bash
   # Check status every 5-10 minutes
   camber job get $JOB_ID

   # When complete or failed, get logs
   camber job logs $JOB_ID > logs-attempt-N.txt
   ```

5. **Document in TESTING_LOG.md**
   - Record attempt number, timestamp
   - Job ID and status
   - Error messages (if failed)
   - Duration
   - Resolution attempted

6. **If Failed: Diagnose and Fix**

   Common issues and fixes:

   **Issue: Docker not found**
   ```groovy
   // In config file
   docker { enabled = false }
   singularity { enabled = true; autoMounts = true }
   ```

   **Issue: OutOfMemoryError**
   ```groovy
   // Increase process memory
   withLabel:process_high {
     memory = { 96.GB * task.attempt }
   }
   // Or increase jobConfig nodeSize
   ```

   **Issue: File not found**
   - Check samplesheet paths
   - Verify stash upload
   - Confirm relative vs absolute paths

   **Issue: Parameter validation failed**
   - Check parameter names in app.json
   - Verify against pipeline schema
   - Ensure required parameters included

   **Issue: Process timeout**
   ```groovy
   // Increase time limits
   withLabel:process_high {
     time = { 48.h * task.attempt }
   }
   ```

7. **After Each Attempt**
   - Update TESTING_LOG.md with full details
   - Commit changes to git with descriptive message
   - If fixed: Mark as ✅ Working in STATUS.txt
   - If 5 attempts exhausted: Mark as ❌ Failed

8. **Update PIPELINE_STATUS.md**
   - Track overall progress
   - Document common issues
   - Share lessons learned

### Phase 4: Success Criteria

**App is considered working when**:
- ✅ Test job completes with status COMPLETED
- ✅ Expected output files are generated
- ✅ MultiQC report (if applicable) shows reasonable QC
- ✅ No errors in job logs
- ✅ Results are scientifically meaningful

**App is marked failed when**:
- ❌ 5 attempts completed without success
- ❌ Documented reason for failure in TESTING_LOG.md
- ❌ Updated STATUS.txt with ❌ Failed
- ❌ Moved to next use case or pipeline

### Phase 5: Production Deployment

Once app is working:

1. **Final Testing**
   - Run with different test datasets (if available)
   - Verify resource allocation appropriate

2. **Documentation Review**
   - Ensure README.md is complete
   - Verify app.json descriptions are biology-focused
   - Check that samplesheet instructions are clear

3. **Deployment**
   ```bash
   # Deploy to production
   camber app create --file app.json
   ```

4. **Mark Complete**
   - Update STATUS.txt: ✅ Working (Deployed)
   - Update PIPELINE_STATUS.md
   - Commit to git

---

## Parallel Implementation Strategy ("Swarming")

To accelerate implementation, multiple apps can be developed in parallel:

### Approach 1: Parallel Pipelines
- Assign different pipelines to different "workers"
- Each worker follows full implementation workflow for their pipeline
- Minimal dependencies between pipelines

### Approach 2: Parallel Use Cases Within Pipeline
- One person researches and defines all use cases
- Multiple people implement different use cases simultaneously
- Requires coordination on shared config patterns

### Approach 3: Pipeline Phases
- Team 1: Research & planning phase (create USE_CASES.md)
- Team 2: Implementation phase (create app.json, configs)
- Team 3: Testing phase (run tests, fix issues)

### Recommended: Hybrid Approach
1. **Week 1-2**: Research phase for Tier 1 pipelines (8 pipelines)
   - Create PIPELINE_STATUS.md and USE_CASES.md for all

2. **Week 3-6**: Parallel implementation and testing
   - Split into teams, each taking 2-3 pipelines
   - Implement all use cases for assigned pipelines
   - Test in parallel

3. **Week 7-8**: Tier 2 pipelines (10 pipelines)
   - Apply lessons learned from Tier 1
   - Faster implementation due to established patterns

4. **Week 9-12**: Tier 3-4 pipelines
   - More specialized, lower priority
   - Can be done opportunistically

---

## Git Workflow for Parallel Work

### Branch Strategy

```bash
# Main branch for stable apps
git checkout main

# Feature branch per pipeline
git checkout -b pipeline/{pipeline-name}

# Work on pipeline
cd nextflow/{pipeline}
# ... implement use cases ...

# Commit frequently
git add .
git commit -m "pipeline/{pipeline}: Add {usecase} app - Attempt N"

# Push to remote
git push origin pipeline/{pipeline-name}

# When complete and tested
git checkout main
git merge pipeline/{pipeline-name}
git push origin main
```

### Commit Message Convention

```
pipeline/{pipeline}: {action} - {detail}

Examples:
- pipeline/chipseq: Add transcription-factor-narrow app
- pipeline/chipseq: Fix OOM error in histone-marks-broad (attempt 3)
- pipeline/chipseq: Mark differential-binding as failed after 5 attempts
- pipeline/chipseq: Update PIPELINE_STATUS with completion summary
```

---

## Success Metrics

### Per Pipeline
- Number of use case apps defined
- Number of apps working / total
- Number of apps failed after 5 attempts
- Common issues encountered and resolved

### Overall Project
- Total pipelines with at least 1 working app
- Total working apps across all pipelines
- Percentage of Tier 1 pipelines complete
- Documentation quality (completeness of logs)

### Targets
- **Tier 1**: 90%+ success rate (apps working / apps attempted)
- **Tier 2**: 75%+ success rate
- **Tier 3+**: 50%+ success rate (more experimental)

---

## Risk Management

### Pipeline May Fail Due To:

1. **Platform Incompatibility**
   - Requires features not available on Camber
   - Needs interactive input
   - Resolution: Mark as failed with clear reason

2. **Resource Constraints**
   - Requires more memory/CPU than available
   - Resolution: Try on XLARGE; if still fails, mark as failed

3. **Container Issues**
   - Containers don't work with Singularity
   - Resolution: Check nf-core issues, try alt versions

4. **Data Requirements**
   - No suitable test data available
   - Input format too complex for testing
   - Resolution: Mark with "needs test data" flag

### Mitigation Strategies

1. **Start with Known-Working Pipelines**
   - Use scrnaseq, sarek, rnaseq as templates
   - Copy config patterns that work

2. **Use nf-core Test Data**
   - Most pipelines have test profile
   - Proven to work with pipeline

3. **Leverage Community**
   - Check nf-core Slack for common issues
   - Review GitHub issues for pipeline

4. **Document Everything**
   - Future attempts benefit from past failures
   - Patterns emerge from multiple attempts

---

## Next Steps

### Immediate Actions

1. **Create Status Files for Existing Pipelines**
   ```bash
   for pipeline in atacseq crisprseq mag methylseq rnaseq sarek scrnaseq; do
     cd /Users/david/git/prod_apps/nextflow/$pipeline
     touch PIPELINE_STATUS.md USE_CASES.md IMPLEMENTATION_LOG.md
   done
   ```

2. **Document Current State**
   - For each existing pipeline, create PIPELINE_STATUS.md
   - List what apps exist already
   - Identify what additional use cases to add

3. **Prioritize Tier 1 Pipelines**
   - Start with chipseq (no existing implementation)
   - Research and create USE_CASES.md

4. **Begin First Implementation**
   - chipseq: transcription-factor-narrow
   - Full workflow from research to testing
   - Document extensively for template

---

## Templates

### Quick Reference Template Files

**Location**: `/Users/david/git/prod_apps/nextflow/_templates/`

Files to create:
- `PIPELINE_STATUS.template.md`
- `USE_CASES.template.md`
- `IMPLEMENTATION_LOG.template.md`
- `TESTING_LOG.template.md`
- `README.template.md`
- `app.template.json`
- `config.template.config`

These templates speed up creation of new pipeline implementations.

---

## Conclusion

This plan provides:
- ✅ Comprehensive list of nf-core pipelines to implement
- ✅ Priority ordering based on biological impact
- ✅ Detailed workflow for each implementation phase
- ✅ Clear success/failure criteria (5 attempts max)
- ✅ Parallel work strategy for "swarming"
- ✅ Extensive documentation requirements
- ✅ Risk management and mitigation

**Estimated Effort**:
- Tier 1 (8 pipelines, ~65 apps): 8-12 weeks with parallel work
- Tier 2 (10 pipelines, ~30 apps): 6-8 weeks
- Tier 3-7 (30+ pipelines): Ongoing, opportunistic

**Expected Success Rate**:
- ~85% of apps working after ≤5 attempts (based on Tier 1)
- ~15% marked as failed with documented reasons
- 100% with complete documentation for learning