# Processed multilingual language-classifier dataset v1

This folder is generated from data/interim/indiccmix_candidates/multilingual_dataset_candidates.zip for the project's current three-label contract:

- hi-IN: Hindi-only and Hindi-English mixed-script candidates
- en-IN: English-only candidates
- none: every other language category, including non-Hindi Indic-English mixtures and unsupported-language candidates

Expected generated files:
- train.csv.gz, validation.csv.gz, test.csv.gz
- manifest.json
- label_counts.csv
- category_counts.csv

CSV columns: text, label, category, source, source_file, source_group_id, review_status, is_synthetic.

## Processing choices
- Normalize whitespace, remove empty rows and exact duplicate text.
- Map hindi_only and hindi_english_mixed_script to hi-IN; english_only to en-IN; all other categories to none.
- Deterministic 80/10/10 split by source_group_id; sibling rows stay in one split.
- Keep all Hindi and English candidates. Sample 2,000 rows from each of 20 none categories (1,600 train / 200 validation / 200 test per category).
- Seed: 20261017.

## Important limitations
These are candidate-unreviewed labels, not human-verified ground truth. IndicCMix may be template/translation-like and is not a substitute for natural call transcripts. Do not treat metrics on this data as real-world accuracy. Keep call_data(3).txt entirely separate for final evaluation. Synthetic Punjabi-Hindi and Marathi-Hindi data are excluded pending audit; under the current three-label contract, such categories map to none. Verify source licensing and redistribution permission before public release or use beyond permitted research.
