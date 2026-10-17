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


## Update — source selection and monolingual collection notebook

- Reviewed the BnSentMix source description. The paper describes Bengali-English code-mixed text written in English characters; this does **not** satisfy our strict Bengali-native-script + Latin-English rule by default. It is now marked research-only, not an accepted source for that category unless row-level evidence proves both scripts are present.
- Selected AI4Bharat IndicCorpV2 as a candidate source for monolingual language-only pools and diverse unsupported-language examples. Its dataset card reports CC-0 for created data, but license metadata/upstream terms must be rechecked. The corpus is large and mainly web-derived, so the notebook streams subsets rather than downloading the entire corpus.
- Added `notebooks/indiccorp_v2_monolingual_candidate_collection.ipynb` to stream 20,000 candidate rows per supported language-only category. The notebook has not been run in this environment; no new rows are counted as collected yet.
- This source cannot fill any mixed-script language-English category. Those require actual code-mixed data containing native script + Latin English, and must pass the two-script gate plus language review.

## Update — mixed-script source identified

- Added `notebooks/indiccmix_mixed_script_candidate_collection.ipynb` for AI4Bharat IndicCMix. Its dataset card reports an MIT license, 11 Indic languages, and a `native_script_codemixed` field intended to preserve Indic native script plus Latin-script English. Re-check current license/provenance before commercial use. Source: https://huggingface.co/datasets/ai4bharat/IndicCMix
- The notebook filters for both a language-specific native-script block and Latin letters in the same utterance, writes candidate-only CSVs, and preserves source row/group IDs. It does not approve labels or create final splits.
- Important caveat: the dataset is translation-derived and its audio is English TTS, not natural code-mixed voice-call audio. Treat it as text candidate/augmentation data only, review linguistic quality and domain suitability, and keep related English-source sentence variants in the same split to prevent leakage.
- The notebook has **not** been executed here. No IndicCMix rows are counted as collected or approved yet.
