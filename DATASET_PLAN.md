# Dataset Plan and Row Targets

## Label contract

| Label | Rule |
|---|---|
| `hi-IN` | Hindi-only and Hindi-English Hinglish, provided genuine Punjabi is absent |
| `en-IN` | English-only |
| `pa-IN` | Punjabi-only or any genuine Punjabi-containing mix |
| `none` | Unsupported languages, solo or mixed with English |

This is utterance-level language classification, not script classification.

## A. Hindi and English

| Data type | Target | Source | Filtering requirements | Label |
|---|---:|---|---|---|
| Hindi-only, Devanagari | 20,000 | Trilingual Hinglish Corpus `hindi`; HinGE verified Hindi | Exclude Hinglish, Romanized Hindi, and other-language rows | `hi-IN` |
| English-only, Latin | 20,000 | Trilingual Hinglish Corpus `english`; HinGE verified English | Exclude code-mixed and other-language rows | `en-IN` |
| Hindi-English Hinglish | 20,000 | COMI-LINGUA | Keep genuine mixed utterances, including mixed-script words; review annotation and deduplicate | `hi-IN` |

## B. Punjabi combinations

| Data type | Target | Source plan | Limitations / action | Label |
|---|---:|---|---|---|
| Punjabi-only | 20,000 | Punjabi Gurmukhi Grammar Correction Corpus, plus other licensed Punjabi corpora if needed | Inspect schema/license; grammar-correction pairs may not contain enough unique utterances | `pa-IN` |
| Punjabi-Hindi | 20,000 | Synthetic Punjabi-Hindi CSV, reviewed and audited | Synthetic; deduplicate; keep every script variant of one base utterance in the same split | `pa-IN` |
| Punjabi-English | 20,000 | AI4Bharat Indic-Glossaries as a vocabulary resource plus verified mixed utterances or reviewed generation | Glossary entries are not utterances; do not count raw glossary rows as conversations | `pa-IN` |
| Punjabi-Hindi-English | 20,000 | Reviewed synthetic generation and/or licensed real code-mixed sources | Verify all three languages are genuinely present | `pa-IN` |

## C. Unsupported Indian languages

For each language below, target 20,000 solo utterances and 20,000 language-English mixed utterances. Both categories map to `none`. Track native and Romanized scripts separately when available.

| Language | Solo target | + English target | Candidate source/action |
|---|---:|---:|---|
| Assamese | 20,000 | 20,000 | IndicLID candidate rows and licensed Assamese corpus; separately validate English-mixed examples |
| Bengali (Bangla) | 20,000 | 20,000 | IndicLID candidate rows and licensed Bengali corpus; separately validate English-mixed examples |
| Bodo | 20,000 | 20,000 | IndicLID candidate rows and licensed Bodo corpus; separately validate English-mixed examples |
| Dogri | 20,000 | 20,000 | IndicLID candidate rows and licensed Dogri corpus; separately validate English-mixed examples |
| Gujarati | 20,000 | 20,000 | IndicLID candidate rows and licensed Gujarati corpus; separately validate English-mixed examples |
| Kannada | 20,000 | 20,000 | IndicLID candidate rows and licensed Kannada corpus; separately validate English-mixed examples |
| Kashmiri | 20,000 | 20,000 | IndicLID candidate rows and licensed Kashmiri corpus; separately validate English-mixed examples |
| Konkani | 20,000 | 20,000 | IndicLID candidate rows and licensed Konkani corpus; separately validate English-mixed examples |
| Maithili | 20,000 | 20,000 | IndicLID candidate rows and licensed Maithili corpus; separately validate English-mixed examples |
| Malayalam | 20,000 | 20,000 | IndicLID candidate rows and licensed Malayalam corpus; separately validate English-mixed examples |
| Manipuri (Meitei) | 20,000 | 20,000 | IndicLID candidate rows and licensed Manipuri corpus; separately validate English-mixed examples |
| Marathi | 20,000 | 20,000 | IndicLID candidate rows and licensed Marathi corpus; separately validate English-mixed examples |
| Nepali | 20,000 | 20,000 | IndicLID candidate rows and licensed Nepali corpus; separately validate English-mixed examples |
| Odia | 20,000 | 20,000 | IndicLID candidate rows and licensed Odia corpus; separately validate English-mixed examples |
| Sanskrit | 20,000 | 20,000 | IndicLID candidate rows and licensed Sanskrit corpus; separately validate English-mixed examples |
| Santali | 20,000 | 20,000 | IndicLID candidate rows and licensed Santali corpus; separately validate English-mixed examples |
| Sindhi | 20,000 | 20,000 | IndicLID candidate rows and licensed Sindhi corpus; separately validate English-mixed examples |
| Tamil | 20,000 | 20,000 | IndicLID candidate rows and licensed Tamil corpus; separately validate English-mixed examples |
| Telugu | 20,000 | 20,000 | IndicLID candidate rows and licensed Telugu corpus; separately validate English-mixed examples |
| Urdu | 20,000 | 20,000 | IndicLID candidate rows and licensed Urdu corpus; separately validate English-mixed examples |

IndicLID is a language-identification resource, not guaranteed conversational or code-mixed data. Record whether each row is source text, a transformed row or synthetic.

## Target count arithmetic

| Group | Categories | Rows/category | Target rows |
|---|---:|---:|---:|
| Hindi-only, English-only, Hindi-English | 3 | 20,000 | 60,000 |
| Punjabi-only and 3 Punjabi combinations | 4 | 20,000 | 80,000 |
| 20 unsupported languages, solo | 20 | 20,000 | 400,000 |
| 20 unsupported languages + English | 20 | 20,000 | 400,000 |
| **Total** | **47** | — | **940,000** |

All figures are targets. Do not pad categories with duplicates to reach them. Record shortfalls and find licensed supplementary data or explicitly marked, reviewed synthetic examples.

## Canonical schema

`text,label,language_type,script_type,source_dataset,source_row_id,is_synthetic,group_id,split,review_status`

Suggested `language_type` values include `hi_solo`, `en_solo`, `hi_en_mix`, `pa_solo`, `pa_hi_mix`, `pa_en_mix`, `pa_hi_en_mix`, `other_ta_solo`, and `other_ta_en_mix`.

## Data quality and split rules

1. Preserve source and license provenance.
2. Normalize Unicode and whitespace without changing language identity.
3. Detect duplicates after normalization.
4. Group translation pairs, synthetic siblings and script variants before splitting.
5. Keep a locked test set; never tune generation templates against it.
6. Audit samples from every source and language type, ideally with a fluent/native reviewer.
7. Report counts by final label, language type, script, source, and real/synthetic.
8. Exclude or review ambiguous utterances rather than guessing.
