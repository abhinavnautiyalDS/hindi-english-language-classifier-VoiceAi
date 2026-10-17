# Synthetic Marathi-Hindi Candidate Data

Four CSV shards make up 20,000 synthetic candidate rows (5,000 rows per shard; header included in each). Combine with pandas before analysis:

```python
from pathlib import Path
import pandas as pd
root = Path("data/synthetic/marathi_hindi")
files = sorted(root.glob("marathi_hindi_synthetic_20000_part*_of_4.csv"))
df = pd.concat([pd.read_csv(p) for p in files], ignore_index=True)
df = df.drop_duplicates(subset=["source_row_id"])
df.to_csv(root / "marathi_hindi_synthetic_20000.csv", index=False)
print(df.shape, df["label"].value_counts().to_dict())
```

- Label: `mr-IN` per the dataset plan (Marathi-Hindi).
- Provenance: `synthetic_template_generator_v1`; all rows are marked `is_synthetic=true` and `synthetic_unreviewed`.
- Four related variants share a `group_id`; keep them together during splitting.
- Marathi and Hindi both use Devanagari. Script detection cannot validate this label: review lexical language identity, naturalness, duplicates, and Marathi dominance before training. Do not use for independent evaluation.
