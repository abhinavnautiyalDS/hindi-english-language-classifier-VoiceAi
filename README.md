# Multilingual Voice-Agent Language Classifier

Dataset foundation for a four-class, utterance-level language classifier used to route voice-agent responses. This repository organizes source data, synthetic data, provenance, cleaning outputs, model artifacts, and evaluation.

## Label contract

| Label | Meaning | Examples |
|---|---|---|
| `hi-IN` | Hindi without genuine Punjabi | Hindi-only; Hindi-English Hinglish |
| `en-IN` | English-only | English in Latin script |
| `pa-IN` | Genuine Punjabi is present | Punjabi-only; Punjabi-Hindi; Punjabi-English; Punjabi-Hindi-English |
| `none` | Unsupported language | Other Indian languages, solo or mixed with English |

Classify the **language**, not the script. Devanagari, Gurmukhi, and Latin script by themselves do not determine a label. Romanized text must also be language-verified.

## Dataset target plan

The target is **20,000 rows per data type**, not per final class:

- Hindi-only: 20,000
- English-only: 20,000
- Hindi-English Hinglish: 20,000
- Punjabi-only, Punjabi-Hindi, Punjabi-English, Punjabi-Hindi-English: 20,000 each
- Each of 20 unsupported Indian languages: 20,000 solo + 20,000 mixed with English

Planning total: **47 data types, 940,000 target rows**. These are targets, not claims that all rows are already collected. Never pad data with duplicates just to meet a target. If a source is too small, record the gap and add a licensed source or clearly marked and reviewed synthetic data.

Detailed source and row targets: [DATASET_PLAN.md](DATASET_PLAN.md). See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for sources and limitations.

## Current source policy

- **Trilingual Hinglish Corpus:** verified English-Latin and Hindi-Devanagari columns only; exclude Hinglish, Romanized and other-language rows.
- **HinGE:** verified English-Latin and Hindi-Devanagari only; exclude Hinglish, Romanized and other-language rows.
- **COMI-LINGUA:** genuine Hinglish utterances, including mixed-script words, for `hi-IN`.
- **Punjabi Gurmukhi Grammar Correction Corpus:** Punjabi-only seed; inspect schema/license and supplement if unique rows are insufficient.
- **Synthetic Punjabi-Hindi:** use as a synthetic seed, not as human-written data. Audit naturalness, labels, duplicates, and script variants.
- **AI4Bharat Indic-Glossaries:** vocabulary resource for Punjabi-English, not a ready-made conversational utterance dataset. Do not count glossary entries as utterances without documented construction and validation.
- **AI4Bharat IndicLID:** candidate source for filtering/identifying unsupported languages, not a guarantee of naturally code-mixed examples. Audit schema, license and text composition.

## Repository layout

```text
data/
  raw/                  # upstream downloads, local only by default
  interim/              # source-specific filtered/normalized data
  processed/
    four_class/          # merged train/validation/test + audit
    legacy/              # previous splits/audits, if imported
  synthetic/
    punjabi_hindi/       # synthetic CSV + generation/audit metadata
  manifests/             # source registry, checksums and acquisition log
  legacy/                # documented previous-data snapshots
configs/                 # label map, source and generation configs
docs/                    # dataset plan, source policy and schema
scripts/
  data/                  # acquisition, filtering, synthesis, merge/audit
src/
  data/                  # reusable validation, cleaning and split utilities
  models/                # future four-class training/inference interfaces
notebooks/               # exploration only; finalized logic goes in scripts/src
models/
  four_class/            # future four-class model + config + evaluation
  legacy/                 # legacy model artifacts if transferred
evaluation/
  heldout/                # locked holdout predictions/error analysis
  reports/                # metrics, confusion matrix and comparisons
tests/
  data/                   # schema, labels, split integrity and leakage tests
```

## Data storage and integrity rules

1. Never overwrite previous dataset/model artifacts during preparation.
2. New merged data goes only to `data/processed/four_class/`.
3. Keep raw downloads in `data/raw/` locally. Commit raw source files only if their license allows redistribution.
4. Record each source URL, license, accessed date, checksum, original columns, filters, and row counts in `data/manifests/`.
5. Canonical row schema: `text,label,language_type,script_type,source_dataset,source_row_id,is_synthetic,group_id,split,review_status`.
6. Group translation pairs, script variants, and synthetic siblings before splitting to prevent leakage.
7. Keep an untouched test set; synthetic test data must not share generation templates/base sentences with training data.
8. Deduplicate after normalization, preserve source attribution, and audit samples from every source/type.
9. Keep real-source and synthetic rows distinguishable.
10. Record rejected-row counts and reasons. Do not silently guess ambiguous labels.

## Planned generated outputs

- `data/processed/four_class/train.csv`
- `data/processed/four_class/validation.csv`
- `data/processed/four_class/test.csv`
- `data/processed/four_class/dataset_audit.json`
- `data/processed/four_class/class_counts.csv`
- `data/manifests/source_registry.csv`
- `data/manifests/acquisition_log.csv`

These outputs are generated by the data pipeline after source/license audit, cleaning, deduplication, grouping, splitting and review.

## Development checklist

- [x] Define four output labels and source-to-category policy.
- [x] Define 20,000-row targets for each data type.
- [x] Set up storage structure and manifests.
- [ ] Verify exact upstream schema, license, and downloadable rows for every source.
- [ ] Implement reproducible acquisition and filtering scripts.
- [ ] Generate/review missing synthetic combinations.
- [ ] Build group-aware, leakage-checked train/validation/test splits.
- [ ] Train and evaluate model; report per-class precision/recall/F1, macro-F1, confusion matrix and latency.
- [ ] Validate on a locked, representative, consented and anonymized STT/call test set before production claims.

**Status:** Repository scaffold only. The 940,000 target rows have not yet all been acquired or validated.
