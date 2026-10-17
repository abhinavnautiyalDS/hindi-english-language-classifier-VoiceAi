# Multilingual Mixed-Script Dataset Plan

## Objective
Prepare a low-latency voice-agent language identifier with 12 output labels: 11 supported tags and `none`. Dataset target: 500,000 candidate examples across 26 categories. Targets are not achieved counts; rows remain unapproved until quality, licensing, and leakage checks pass.

## Labels and category targets

Every category targets 20,000 examples except the two `none` categories, which target 10,000 each.

| Category | Label | Target |
|---|---|---:|
| English-only | `en-IN` | 20,000 |
| Hindi-only (Devanagari) | `hi-IN` | 20,000 |
| Hindi-English Hinglish mixed-script | `hi-IN` | 20,000 |
| Punjabi-only | `pa-IN` | 20,000 |
| Punjabi-Hindi | `pa-IN` | 20,000 |
| Punjabi-English mixed-script | `pa-IN` | 20,000 |
| Punjabi-Hindi-English | `pa-IN` | 20,000 |
| Bengali-only | `bn-IN` | 20,000 |
| Bengali-English mixed-script | `bn-IN` | 20,000 |
| Gujarati-only | `gu-IN` | 20,000 |
| Gujarati-English mixed-script | `gu-IN` | 20,000 |
| Kannada-only | `kn-IN` | 20,000 |
| Kannada-English mixed-script | `kn-IN` | 20,000 |
| Malayalam-only | `ml-IN` | 20,000 |
| Malayalam-English mixed-script | `ml-IN` | 20,000 |
| Marathi-only | `mr-IN` | 20,000 |
| Marathi-English mixed-script | `mr-IN` | 20,000 |
| Marathi-Hindi | `mr-IN` | 20,000 |
| Telugu-only | `te-IN` | 20,000 |
| Telugu-English mixed-script | `te-IN` | 20,000 |
| Assamese-only | `as-IN` | 20,000 |
| Assamese-English mixed-script | `as-IN` | 20,000 |
| Tamil-only | `ta-IN` | 20,000 |
| Tamil-English mixed-script | `ta-IN` | 20,000 |
| Unsupported language only | `none` | 10,000 |
| Unsupported language + English | `none` | 10,000 |

**Total target: 500,000.** The `none` class is 20,000 combined across diverse unsupported languages, not 20,000 per language.

## Non-negotiable mixed-script rule

For every supported-language + English combo, one utterance must contain BOTH:
- text in the language's native script, and
- English text written in Latin script.

This applies to Hinglish (Devanagari + Latin), Punjabi-English (Gurmukhi + Latin), Bengali-English (Bengali + Latin), Gujarati-English, Kannada-English, Malayalam-English, Marathi-English (Devanagari + Latin), Telugu-English, Assamese-English, and Tamil-English. Latin-only romanization does not qualify for these specific mixed-script categories. A brand name, acronym, or URL alone is not sufficient evidence of English code-switching.

## Sources and planned use

- Trilingual Hinglish Corpus: English and Hindi columns for language-only candidate pools; do not blindly accept its Hinglish column. Preserve source splits and paired row provenance. Reported source license has commercial-use implications; verify before use.
- HinGE: English and Hindi candidates after language/script filtering; verify current license and split rules.
- COMI-LINGUA: Hindi-English code-mixing candidates; review annotator agreement and domain suitability; protect official test split.
- Punjabi Gurmukhi Grammar Correction Corpus: Punjabi seed only. Related incorrect/corrected pairs must stay in one split group.
- AI4Bharat Indic-Glossaries: vocabulary seeds only where language pairs exist; glossary entries are not automatically natural utterances.
- BnSentMix: selected as a candidate source for Bengali-English, but it must pass the strict Bengali-script + Latin-script gate. It was built for sentiment analysis; ignore sentiment labels for language ID. Verify the current license and upstream content terms.
- Punjabi-Hindi and Marathi-Hindi synthetic data: mark provenance, group by template/generator, and do not use synthetic-only evaluation.
- Other language categories: source licensed text/code-mix corpora and preserve source URLs, licenses, row IDs, splits, and groups.

## Required row metadata
`text,label,language_category,source_dataset,source_url,source_row_id,group_id,source_split,is_synthetic,review_status,license_status`

## Quality gates before fine-tuning
1. Verify labels by language, not script alone.
2. Apply both-script gate to every language-English category and manually confirm real code-switching.
3. Deduplicate normalized text and audit near-duplicates.
4. Keep translations, correction pairs, template siblings, and near-duplicates group-safe across splits.
5. Keep official source test sets protected.
6. Verify source licenses/attribution and do not redistribute data without permission.
7. Evaluate on real voice/call-style examples and report per-class precision, recall, F1, and confusion matrix.
8. Keep realistic deployment evaluation separate from balanced training targets.

## Status
This file describes targets and collection rules. It does not certify that data has been collected or approved. Read `docs/DATASET_PREPARATION_STATUS.md` and `data/manifests/category_tracker.csv` for current status.
