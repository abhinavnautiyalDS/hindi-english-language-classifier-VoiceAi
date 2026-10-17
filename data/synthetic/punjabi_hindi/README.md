# Synthetic Punjabi-Hindi Candidate Data

Four CSV shards make up 20,000 synthetic candidate rows (5,000 rows per shard; header included in each). Combine with pandas before analysis:

```python
from pathlib import Path
import pandas as pd
root = Path("data/synthetic/punjabi_hindi")
files = sorted(root.glob("punjabi_hindi_synthetic_20000_part*_of_4.csv"))
df = pd.concat([pd.read_csv(p) for p in files], ignore_index=True)
df = df.drop_duplicates(subset=["source_row_id"])
df.to_csv(root / "punjabi_hindi_synthetic_20000.csv", index=False)
print(df.shape, df["label"].value_counts().to_dict())
```

- Label: `pa-IN` (repository rule: genuine Punjabi present).
- Provenance: `synthetic_template_generator_v1`; all rows are marked `is_synthetic=true` and `synthetic_unreviewed`.
- Four related variants share a `group_id`; keep them together in train/validation/test splitting.
- These are template-generated candidates, not human-written or approved examples. Review language naturalness, Punjabi/Hindi balance, duplicates, and label correctness before training. Do not use for independent evaluation.
