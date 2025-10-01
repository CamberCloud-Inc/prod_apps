# Nextflow Pipelines for Camber Platform

**Comprehensive nf-core bioinformatics workflow collection**

Production-ready Nextflow pipeline configurations optimized for the Camber cloud computing platform. All pipelines leverage nf-core community standards for reproducibility, containerization, and best practices.

---

## 📊 Current Status

**Total Apps:** 195 (189 deployed + 6 duplicates)
**Unique Pipelines:** 135 nf-core pipelines
**Progress:** 97% pipelines (135/139), 65% apps (189/290)

[**→ View Detailed Implementation Progress**](IMPLEMENTATION_PROGRESS.md)

---

## 🔬 Pipeline Categories

### Transcriptomics (18 apps)
- **RNA-seq**: Differential expression, splicing, fusion detection
- **Single-cell**: scRNA-seq, scDownstream, Smart-seq2, scNanoseq
- **Isoform Analysis**: Iso-Seq, Nanoseq RNA, RNAsplice
- **Small RNA**: miRNA profiling (smrnaseq)
- **Specialized**: Ribo-seq, CAGE-seq, nascent, SLAM-seq, CLIP-seq

### Genomics & Variant Calling (14 apps)
- **WGS/WES**: Sarek germline & somatic, RNAvar
- **Specialized**: Ancient DNA (EAGER), PacBio variants, rare disease
- **Cancer**: Oncoanalyser (tumor-normal, targeted panels)
- **Long-read**: Nanoseq DNA, structural variants

### Epigenomics & Chromatin (10 apps)
- **ChIP-seq**: TF binding, histone modifications
- **ATAC-seq**: Chromatin accessibility, regulatory landscape
- **CUT&RUN**: Low-input profiling
- **Methylseq**: DNA methylation, targeted analysis
- **Hi-C**: 3D genome architecture, TAD analysis
- **MNase-seq**: Nucleosome positioning

### Metagenomics & Microbiology (15 apps)
- **Taxonomic Profiling**: Taxprofiler, ampliseq (16S, ITS)
- **Assembly**: Bacass (bacterial genomes), metatranscriptome
- **Functional Screening**: Funcscan (AMR, BGCs, virulence)
- **Specialized**: Pangenome, phage annotation, phylogenetic placement

### Proteomics & Structure (3 apps)
- **Quantification**: QuantMS (LFQ, TMT, SILAC)
- **Structure Prediction**: AlphaFold2 (Proteinfold)

### Specialized Applications (12 apps)
- **CRISPR**: Editing efficiency & variant analysis
- **HLA Typing**: High-resolution genotyping
- **Immune Repertoire**: BCR/TCR sequencing (AIRRflow)
- **Host-Pathogen**: Dual RNA-seq
- **NanoString**: Targeted gene expression
- **Demultiplexing**: NGS sample demux
- **Circular DNA**: ecDNA detection
- **Data Download**: FetchNGS (SRA/ENA/GEO)

---

## 🎯 Implementation Batches

| Batch | Pipelines | Apps | Status |
|-------|-----------|------|--------|
| Previous | 19 | 38 | ✅ Deployed |
| Batch 1-4 | 13 | 33 | ✅ Deployed |
| Batch 5 | 0 | 0 | ❌ Memory limits |
| Batch 6-7 | 3 | 8 | ✅ Deployed |
| Batch 8-10 | 9 | 13 | ✅ Deployed |
| Batch 11 | 6 | 6 | ✅ Deployed |
| Batch 12 | 10 | 10 | ✅ Deployed |
| Batch 13 | 11 | 11 | ✅ Deployed |
| Batch 14 | 10 | 10 | ✅ Deployed |
| Batch 15 | 10 | 10 | ✅ Deployed |
| Batch 16 | 10 | 10 | ✅ Deployed |
| Batch 17 | 10 | 10 | ✅ Deployed |
| Batch 18 | 10 | 10 | ✅ Deployed |
| Batch 19 | 10 | 10 | ✅ Deployed |
| Batch 20 | 10 | 10 | ✅ Deployed |
| **Total** | **135** | **195** | **189 deployed** |

---

## 🚀 Getting Started

Each pipeline directory contains:
- `app.json` - Camber platform configuration
- Optimized compute resources (SMALL → XLARGE nodes)
- Comprehensive scientific documentation
- Use-case specific parameter presets

**Deploy via Camber CLI:**
```bash
camber app create --file <pipeline>/app.json
```

---

## 📖 Documentation

- **[IMPLEMENTATION_PROGRESS.md](IMPLEMENTATION_PROGRESS.md)** - Detailed batch tracking
- **[COMPREHENSIVE_IMPLEMENTATION_PLAN.md](COMPREHENSIVE_IMPLEMENTATION_PLAN.md)** - Full roadmap (139 pipelines)
- **[BATCH_1_TESTING_LOG.md](BATCH_1_TESTING_LOG.md)** - Testing results & learnings

---

## 🏗️ Platform Details

**Camber Cloud Platform:**
- Nextflow 24.10.5 (DSL2 required)
- Per-process memory limit: 3.9GB
- Node sizes: XSMALL, SMALL, MEDIUM, LARGE, XLARGE
- Stash storage integration

---

## 📝 Notes

- All pipelines use stable nf-core releases (no dev branches)
- Memory-intensive pipelines (MAG, viralrecon) require platform updates
- Duplicate apps from previous sessions exist (6 duplicates in 114 total)
- Testing performed on selected pipelines (riboseq validated)

**Last Updated:** 2025-10-01
