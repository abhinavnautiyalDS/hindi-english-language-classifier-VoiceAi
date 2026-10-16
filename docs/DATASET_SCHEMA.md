# Canonical Dataset Schema

| Column | Type | Meaning |
|---|---|---|
| `text` | string | Normalized utterance |
| `label` | category | `hi-IN`, `en-IN`, `pa-IN`, or `none` |
| `language_type` | string | Solo or language-combination data type |
| `script_type` | string | Latin, Devanagari, Gurmukhi, other native script, or mixed |
| `source_dataset` | string | Dataset/source name |
| `source_row_id` | string | Original row ID when available |
| `is_synthetic` | boolean | Whether the utterance was generated |
| `group_id` | string | Links translation pairs, variants and related synthetic examples |
| `split` | category | train, validation, or test |
| `review_status` | category | unreviewed, reviewed, accepted, or rejected |

## Label rules

- Hindi-only and Hindi-English Hinglish without genuine Punjabi: `hi-IN`.
- English-only: `en-IN`.
- Any utterance containing genuine Punjabi: `pa-IN`.
- Other unsupported languages, solo or mixed with English: `none`.
- Never classify by script alone. Review ambiguous rows rather than guessing.
