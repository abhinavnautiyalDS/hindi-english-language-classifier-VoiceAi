#!/usr/bin/env python3
"""Build grouped, balanced candidate data for hi-IN / en-IN / none classification."""
from pathlib import Path
import argparse, json, re, zipfile
import numpy as np
import pandas as pd

SEED = 20261017
LABEL_MAP = {
    "hindi_only": "hi-IN",
    "hindi_english_mixed_script": "hi-IN",
    "english_only": "en-IN",
}
NONE_CATEGORIES = [
    "punjabi_only", "punjabi_english_mixed_script",
    "bengali_only", "bengali_english_mixed_script",
    "gujarati_only", "gujarati_english_mixed_script",
    "kannada_only", "kannada_english_mixed_script",
    "malayalam_only", "malayalam_english_mixed_script",
    "marathi_only", "marathi_english_mixed_script",
    "telugu_only", "telugu_english_mixed_script",
    "assamese_only", "assamese_english_mixed_script",
    "tamil_only", "tamil_english_mixed_script",
    "unsupported_language_only", "unsupported_language_english_mixed_script",
]

def clean_text(value):
    value = str(value).replace("\ufeff", "")
    return re.sub(r"\s+", " ", value).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-zip", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.input_zip) as archive:
        with archive.open("candidate_pool.csv") as stream:
            df = pd.read_csv(stream, encoding="utf-8-sig", dtype={"source_group_id": str})

    df["text"] = df["text"].map(clean_text)
    df = df[df["text"].str.len().gt(0)].copy()
    df = df.drop_duplicates(subset=["text"], keep="first").copy()
    df["label"] = df["category"].map(LABEL_MAP).fillna("none")
    df["source"] = df["source"].fillna("unknown")
    df["review_status"] = "candidate_unreviewed"
    df["is_synthetic"] = False

    groups = df["source_group_id"].dropna().astype(str).unique().tolist()
    rng = np.random.default_rng(SEED)
    rng.shuffle(groups)
    n_groups = len(groups)
    train_groups = set(groups[:int(n_groups * 0.8)])
    validation_groups = set(groups[int(n_groups * 0.8):int(n_groups * 0.9)])
    def assign_split(group):
        if group in train_groups:
            return "train"
        if group in validation_groups:
            return "validation"
        return "test"
    df["split"] = df["source_group_id"].astype(str).map(assign_split)

    selected_parts = []
    for category in ["hindi_only", "hindi_english_mixed_script", "english_only"]:
        selected_parts.append(df[df["category"] == category])

    targets = {"train": 1600, "validation": 200, "test": 200}
    for category in NONE_CATEGORIES:
        category_rows = df[df["category"] == category]
        if len(category_rows) < 2000:
            raise ValueError(f"Insufficient rows for {category}: {len(category_rows)}")
        for split, target in targets.items():
            pool = category_rows[category_rows["split"] == split]
            if len(pool) < target:
                raise ValueError(f"Insufficient rows for {category}/{split}: {len(pool)} < {target}")
            selected_parts.append(pool.sample(n=target, random_state=SEED + len(category) + len(split)))

    selected = pd.concat(selected_parts, ignore_index=True)
    selected = selected.drop_duplicates(subset=["text"], keep="first").copy()
    columns = ["text", "label", "split", "category", "source", "source_file",
               "source_group_id", "review_status", "is_synthetic"]
    selected = selected[columns].sort_values(
        ["split", "label", "category", "source_group_id"], kind="stable"
    ).reset_index(drop=True)

    for split in ["train", "validation", "test"]:
        subset = selected[selected["split"] == split].drop(columns=["split"])
        subset.to_csv(output / f"{split}.csv.gz", index=False,
                      compression="gzip", encoding="utf-8")

    split_groups = {
        split: set(selected.loc[selected["split"] == split, "source_group_id"])
        for split in ["train", "validation", "test"]
    }
    overlap = {
        "train_validation": len(split_groups["train"] & split_groups["validation"]),
        "train_test": len(split_groups["train"] & split_groups["test"]),
        "validation_test": len(split_groups["validation"] & split_groups["test"]),
    }
    counts = selected.groupby(["split", "label"]).size().unstack(fill_value=0).to_dict(orient="index")
    manifest = {
        "dataset_name": "multilingual_language_classifier_candidates_v1",
        "source": "ai4bharat/IndicCMix candidate pool",
        "seed": SEED,
        "label_contract": {
            "hi-IN": "Hindi-only and Hindi-English mixed-script candidates",
            "en-IN": "English-only candidates",
            "none": "all other supported/unsupported language categories",
        },
        "total_rows": int(len(selected)),
        "split_rows": {split: int((selected["split"] == split).sum())
                       for split in ["train", "validation", "test"]},
        "label_counts_by_split": counts,
        "category_counts_by_split": {
            f"{split}|{category}": int(count)
            for (split, category), count in selected.groupby(["split", "category"]).size().items()
        },
        "unique_source_groups": int(selected["source_group_id"].nunique()),
        "group_overlap_checks": overlap,
        "exact_text_duplicates_after_processing": int(selected["text"].duplicated().sum()),
        "all_rows_candidate_unreviewed": True,
        "excluded": [
            "synthetic Punjabi-Hindi and Marathi-Hindi files; excluded pending audit",
            "call-data evaluation set",
        ],
        "important_limitations": [
            "Labels are inherited from source category and are not human-verified.",
            "IndicCMix can be template/translation-like and is not natural call audio transcription.",
            "The none label merges multiple languages; source-language errors must be reviewed.",
            "This dataset is for initial experiments only, not final evaluation.",
            "Verify source licensing and redistribution permissions before public redistribution.",
        ],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    selected.groupby(["split", "label"]).size().rename("rows").reset_index().to_csv(
        output / "label_counts.csv", index=False
    )
    selected.groupby(["split", "category", "label"]).size().rename("rows").reset_index().to_csv(
        output / "category_counts.csv", index=False
    )
    if any(overlap.values()):
        raise RuntimeError(f"Group leakage detected: {overlap}")
    if selected["text"].duplicated().any():
        raise RuntimeError("Exact text duplicates remain after processing")
    print(json.dumps({
        "total_rows": len(selected),
        "split_rows": manifest["split_rows"],
        "label_counts_by_split": counts,
        "group_overlap_checks": overlap,
        "output_dir": str(output),
    }, indent=2))

if __name__ == "__main__":
    main()
