# Dataset Preparation Status

Last updated: 2026-10-17

## Current decision

**NOT READY FOR FINAL FINE-TUNING.** This branch adds the agreed 500,000-row target plan, source registry, category tracker, and candidate audit script. The plan targets are not claims about collected or approved rows.

## What we currently know from prior local audits

| Category | Candidate count | Caveat |
|---|---:|---|
| English-only | 17,909 | Source-column candidates; not label-approved |
| Hindi-only | 14,066 | Source-column candidates; mixed-script/language review pending |
| Hindi-English mixed-script | 14,964 | COMI-LINGUA candidates; quality and domain review pending |
| Punjabi-only | 2,280 | Grammar-correction seed; 1,140 paired groups; narrow domain |
| Punjabi-Hindi | 20,000 | Synthetic-only candidates; 5,000 groups, four variants per group, 150 normalized duplicate rows reported |

The above assets were available in the prior local audit context. They are **not yet committed as raw training data to this repository**, and none is certified as approved by this status report.

## Work committed on this branch

- Updated `DATASET_PLAN.md` with all 26 categories and 12 output labels.
- Added `data/manifests/category_tracker.csv`.
- Expanded `data/manifests/source_registry.csv`.
- Added `scripts/dataset_prep_pipeline.py` to create auditable candidate files and reports.
- Next work: acquire each source, inspect license/schema, apply category-specific script/language filters, then review and split.

## Mixed-script gate

Every language-English category requires both native-script text and Latin-script English in the same utterance. A script gate is necessary but not sufficient: language identity and genuine code-switching require review. Bengali and Assamese use related Unicode ranges, so character ranges cannot distinguish those languages by themselves.

## Repository data policy

- Commit code, source manifests, small audit reports, and license/provenance documentation.
- Do not commit source data until licensing and redistribution rights are confirmed.
- Large or restricted datasets should remain external or in an approved storage location; store retrieval instructions and checksums in the repository.
- Keep synthetic data marked, grouped, and excluded from independent natural evaluation.
- Keep official source test splits and related examples group-safe.
- Never mark a row approved just because a script/column heuristic passed.

## Fine-tuning readiness checklist

- [ ] Source licenses verified for intended use
- [ ] All 26 category targets collected or an explicit revised target approved
- [ ] Genuine language labels reviewed, including mixed-script combos
- [ ] Duplicate and near-duplicate audit passed
- [ ] Group-safe train/validation/test split built
- [ ] No source-test or group leakage
- [ ] Real voice/call-style independent evaluation set ready
- [ ] Per-class precision, recall, F1, confusion matrix and CPU latency measured
