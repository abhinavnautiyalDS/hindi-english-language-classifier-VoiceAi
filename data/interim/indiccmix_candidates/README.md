# IndicCMix Unprocessed Candidate Pool

The Colab collection run produced an unprocessed candidate pool from AI4Bharat IndicCMix:

- 440,000 rows total in `candidate_pool.csv`
- `category_counts.csv`
- `collection_summary.json`
- Original row text remains candidate-only, with source file/group IDs and `candidate_unreviewed` status.

The uploaded ZIP is currently kept outside this GitHub branch because it is a 54 MB archive containing a 200 MB CSV, and the repository's data policy requires checking redistribution rights before publicly committing source-derived text. Do not treat this README as evidence that the ZIP itself is already committed. Once redistribution terms are confirmed, place the ZIP here or store it in approved dataset storage and add a SHA-256 checksum and retrieval instructions.

Important: the run achieved category counts, not verified language labels. Hindi/Marathi and Bengali/Assamese need language-level validation; script filters alone are insufficient. IndicCMix is translation-derived and its audio is English TTS, so this is text candidate/augmentation data, not independent real-call evaluation.
