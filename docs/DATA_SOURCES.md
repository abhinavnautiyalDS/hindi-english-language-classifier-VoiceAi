# Data Source Registry

Verify exact current schema, source license, and downloadable row counts at acquisition time. Do not redistribute source files unless the license permits it.

| Source | Intended use | Link | Notes/status |
|---|---|---|---|
| Trilingual Hinglish Corpus | Hindi-Devanagari and English-Latin solo utterances | Exact upstream URL to be entered in the source registry | Exclude Hinglish, Romanized and other-language columns |
| HinGE | Hindi-Devanagari and English-Latin solo utterances | Exact upstream URL to be entered in the source registry | Inspect columns; exclude Hinglish, Romanized and other-language rows |
| COMI-LINGUA | Hindi-English Hinglish | https://github.com/lingo-iitgn/COMI-LINGUA | Verify annotations and license before acquisition |
| Punjabi Gurmukhi Grammar Correction Corpus | Punjabi-only seed | https://huggingface.co/datasets/Nam-toon-studio/Punjabi-Gurmukhi-Grammar-Correction-Corpus | Check schema/license and supplement if unique utterances are insufficient |
| Synthetic Punjabi-Hindi CSV | Punjabi-Hindi mixed seed | Local file: `punjabi_hindi_synthetic_20000.csv` | Template-generated; not human-written; review and deduplicate |
| AI4Bharat Indic-Glossaries | Punjabi-English vocabulary resource | https://github.com/AI4Bharat/Indic-Glossaries | Entries are glossary terms, not conversational utterances |
| AI4Bharat IndicLID | Candidate data for unsupported-language filtering | https://github.com/AI4Bharat/IndicLID | LID resource, not necessarily naturally code-mixed data |
| Additional licensed corpora | Supplement missing categories | Enter exact URL per source | Do not include until license and provenance are documented |

## Acquisition log fields

`source_id,source_url,license,accessed_at,download_filename,sha256,source_rows,accepted_rows,rejected_rows,transform_script,transform_version,notes`

The companion CSV files in `data/manifests/` are trackers and do not imply that the sources have been downloaded or approved.
