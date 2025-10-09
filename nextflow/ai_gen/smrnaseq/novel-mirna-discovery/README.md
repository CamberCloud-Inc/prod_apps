# Novel miRNA Discovery

## Overview

Discover novel, previously unannotated microRNAs using MIRDeep2 via the nf-core/smrnaseq pipeline. Identifies species-specific, tumor-specific, or tissue-specific miRNAs.

## Use Case

**Research Question**: Are there novel miRNAs in my samples that haven't been annotated yet?

**Perfect For**:
- Non-model organism researchers
- Cancer biologists studying tumor-specific miRNAs
- Plant scientists
- Evolutionary biologists
- Virology (viral miRNAs)

## Key Features

- **MIRDeep2 Prediction**: Computational discovery of novel miRNAs
- **Hairpin Structure**: Identifies characteristic precursor structures
- **Confidence Scoring**: Statistical scores for predictions
- **Combined Quantification**: Known + novel miRNA expression
- **Standard QC**: Full quality control pipeline

## Input Requirements

- **Sequencing Depth**: Minimum 10M reads, recommended 20-50M reads per sample
- **Multiple Samples**: Increases confidence in predictions
- **Single-End**: Small RNA-seq is typically single-end

Deep sequencing is critical for novel discovery!

## Outputs

- `mirdeep2/novel_mature.fa`: Novel miRNA sequences
- `mirdeep2/novel_precursors.fa`: Hairpin structures
- `mirdeep2/result.html`: Discovery report with scores
- `edger/counts.tsv`: Expression of known + novel miRNAs

## MIRDeep2 Score Interpretation

- **>10**: High confidence (likely genuine)
- **5-10**: Medium confidence (validate)
- **0-5**: Low confidence (likely false positive)
- **<0**: Very low confidence (exclude)

## Validation Required

Novel miRNAs are computational predictions and require experimental validation:
1. Northern blot (gold standard)
2. qPCR with specific primers
3. Independent RNA-seq
4. Functional studies

## Expected Discovery Rates

- **Human/Mouse**: 0-10 novel (well-annotated)
- **Non-Model Organisms**: 10-100+ novel
- **Cancer Samples**: 5-20 tumor-specific
- **Rare Tissues**: 5-30 tissue-specific

## Compute Resources

Novel discovery is computationally intensive:
- **SMALL**: Testing only
- **MEDIUM**: Recommended (5-20 samples)
- **LARGE**: Large studies (>20 samples)

Runtime: 30-60 minutes per sample

## Important Notes

- Requires reference genome (not just pre-built indices)
- Predictions need experimental validation
- Multiple replicates strengthen confidence
- Use closest related species code for non-model organisms

## Submission to miRBase

Successfully validated novel miRNAs can be submitted to miRBase (https://mirbase.org) to contribute to the community annotation database.
