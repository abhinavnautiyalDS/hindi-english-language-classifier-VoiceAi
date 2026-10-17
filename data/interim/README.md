# Interim Data

Store normalized/filtered outputs from each upstream source separately here. Include provenance and log input, accepted and rejected row counts before merging datasets.

## Current safety gate

Raw datasets and candidate CSVs are intentionally not committed here yet. Source license/redistribution rights, schema, language labels, duplicate handling, and source split restrictions must be checked first.

Run `python scripts/dataset_prep_pipeline.py --help` for the auditable candidate-generation tool. It writes candidate CSV and JSON audit files locally and explicitly marks them as not approved.

When adding approved artifacts, retain source URL, source row ID, group ID, source split, synthetic flag, review status, and license status. Do not commit private call data, credentials, or data that the source license does not permit redistributing.
