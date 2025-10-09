# Testing Log: smrnaseq - Biomarker Discovery (Circulating miRNA)

## Test Configuration

**App**: smrnaseq-biomarker-discovery
**Pipeline**: nf-core/smrnaseq v2.4.0
**Test Data**: nf-core test-datasets (8 human samples)
**Genome**: GRCh38
**Species**: hsa (human)
**Protocol**: illumina (default)
**Special Features**: UMI deduplication enabled (`--with_umi`)

## Testing Status

🔲 Not yet tested

---

## Attempt Log

Attempts will be documented here following the 5-attempt protocol.

---

## Configuration Notes

- UMI deduplication: Enabled with `--with_umi` flag
- Protocol: Explicitly specified (illumina)
- Test data: Same as standard profiling but with UMI processing
- Expected difference: Additional UMI deduplication step and statistics

---

## Lessons Learned

Will be documented after testing.
