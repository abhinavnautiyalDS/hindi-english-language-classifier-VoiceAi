#!/usr/bin/env python3
"""Build the planned 12-label multilingual candidate dataset (26 categories)."""
from pathlib import Path
import argparse, json, re, zipfile
import numpy as np
import pandas as pd

SEED = 20261017
LABEL_MAP = {
    "english_only": "en-IN", "hindi_only": "hi-IN", "hindi_english_mixed_script": "hi-IN",
    "punjabi_only": "pa-IN", "punjabi_english_mixed_script": "pa-IN",
    "punjabi_hindi_synthetic": "pa-IN", "punjabi_hindi_english_synthetic": "pa-IN",
    "bengali_only": "bn-IN", "bengali_english_mixed_script": "bn-IN",
    "gujarati_only": "gu-IN", "gujarati_english_mixed_script": "gu-IN",
    "kannada_only": "kn-IN", "kannada_english_mixed_script": "kn-IN",
    "malayalam_only": "ml-IN", "malayalam_english_mixed_script": "ml-IN",
    "marathi_only": "mr-IN", "marathi_english_mixed_script": "mr-IN", "marathi_hindi_synthetic": "mr-IN",
    "telugu_only": "te-IN", "telugu_english_mixed_script": "te-IN",
    "assamese_only": "as-IN", "assamese_english_mixed_script": "as-IN",
    "tamil_only": "ta-IN", "tamil_english_mixed_script": "ta-IN",
    "unsupported_language_only": "none", "unsupported_language_english_mixed_script": "none",
}
SYNTH_CATS = {"punjabi_hindi_synthetic", "punjabi_hindi_english_synthetic", "marathi_hindi_synthetic"}
SUPPORTED_CATS = [c for c in LABEL_MAP if c not in {"unsupported_language_only", "unsupported_language_english_mixed_script"}]
UNSUPPORTED_CATS = ["unsupported_language_only", "unsupported_language_english_mixed_script"]

def clean(x):
    if pd.isna(x): return ""
    return re.sub(r"\\s+", " ", str(x).replace("\\ufeff", "")).strip()

def read_synth(root, folder, pattern, category, label):
    files = sorted((root / folder).glob(pattern))
    if not files: raise FileNotFoundError(f"Missing synthetic shards: {folder}/{pattern}")
    raw = pd.concat([pd.read_csv(p, dtype=str, keep_default_na=False) for p in files], ignore_index=True)
    tc = next((c for c in ["text", "utterance", "sentence", "transcript"] if c in raw.columns), None)
    if not tc: raise ValueError(f"No text column in {folder}: {list(raw.columns)}")
    def pick(row, keys, default=""):
        for k in keys:
            if k in row.index and row[k] != "": return str(row[k])
        return default
    out = pd.DataFrame()
    out["text"] = raw[tc].map(clean)
    out["label"] = label
    out["category"] = category
    out["source"] = "synthetic_template_generator_v1"
    out["source_file"] = folder
    out["source_row_id"] = raw.apply(lambda r: pick(r, ["source_row_id", "row_id", "id"]), axis=1)
    out["source_group_id"] = raw.apply(lambda r: pick(r, ["group_id", "source_group_id", "source_row_id"]), axis=1)
    out["review_status"] = raw.apply(lambda r: pick(r, ["review_status"], "synthetic_unreviewed"), axis=1)
    out["is_synthetic"] = True
    out["generator"] = "synthetic_template_generator_v1"
    out = out[out.text.str.len().gt(0)].drop_duplicates(subset=["source_row_id", "text"])
    if len(out) != 20000: raise ValueError(f"{category}: expected 20,000 unique rows, got {len(out)}")
    if out.source_group_id.eq("").any(): raise ValueError(f"{category}: missing group IDs")
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-zip", required=True); p.add_argument("--output-dir", required=True)
    p.add_argument("--repo-root", default="."); a = p.parse_args()
    root, output = Path(a.repo_root), Path(a.output_dir); output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(a.input_zip) as z:
        with z.open("candidate_pool.csv") as f: base = pd.read_csv(f, encoding="utf-8-sig", dtype={"source_group_id": str})
    base["text"] = base.text.map(clean); base = base[base.text.str.len().gt(0)].copy()
    base["category"] = base.category.astype(str)
    unknown = sorted(set(base.category) - set(LABEL_MAP))
    if unknown: raise ValueError(f"Unexpected categories: {unknown}")
    base["label"] = base.category.map(LABEL_MAP)
    for c, default in [("source", "unknown"), ("source_file", ""), ("source_row_id", ""), ("source_group_id", "")]:
        if c not in base: base[c] = default
        base[c] = base[c].fillna(default).astype(str)
    base["review_status"] = "candidate_unreviewed"; base["is_synthetic"] = False; base["generator"] = ""

    pa_hi = read_synth(root, "data/synthetic/punjabi_hindi", "punjabi_hindi_synthetic_20000_part*_of_4.csv", "punjabi_hindi_synthetic", "pa-IN")
    mr_hi = read_synth(root, "data/synthetic/marathi_hindi", "marathi_hindi_synthetic_20000_part*_of_4.csv", "marathi_hindi_synthetic", "mr-IN")
    # Plan category: Punjabi-Hindi-English. Explicitly mark generated English insertions as synthetic/unreviewed.
    english = ["please check this", "I will call you", "send me the details", "we can discuss this", "please confirm",
               "I need an update", "let us plan this", "share the information", "that is fine", "I will do it today",
               "please help me", "we can start now", "tell me the status", "I will send it", "please wait a moment",
               "we should do this", "I have one question", "can you explain", "please make a note", "we can talk later"]
    pa_hi_en = pa_hi.copy().reset_index(drop=True)
    pa_hi_en["text"] = [f"{t} {english[i % len(english)]}" for i, t in enumerate(pa_hi_en.text)]
    pa_hi_en["category"] = "punjabi_hindi_english_synthetic"
    pa_hi_en["source"] = "synthetic_template_generator_v1_punjabi_hindi_plus_english"
    pa_hi_en["source_file"] = "generated_from_punjabi_hindi_synthetic_candidates"
    pa_hi_en["source_row_id"] = pa_hi_en.source_row_id.astype(str) + "_enmix"
    pa_hi_en["source_group_id"] = pa_hi_en.source_group_id.astype(str)
    pa_hi_en["review_status"] = "synthetic_unreviewed"; pa_hi_en["is_synthetic"] = True
    pa_hi_en["generator"] = "english_segment_insertion_v1"

    base = base.drop_duplicates(subset=["text"], keep="first")
    parts = []
    for c in SUPPORTED_CATS:
        if c in SYNTH_CATS: continue
        pool = base[base.category.eq(c)]
        if len(pool) < 20000: raise ValueError(f"{c}: need 20,000, found {len(pool)}")
        parts.append(pool.sample(n=20000, random_state=SEED + len(c)))
    for c in UNSUPPORTED_CATS:
        pool = base[base.category.eq(c)]
        if len(pool) < 10000: raise ValueError(f"{c}: need 10,000, found {len(pool)}")
        parts.append(pool.sample(n=10000, random_state=SEED + len(c)))
    selected = pd.concat(parts + [pa_hi, pa_hi_en, mr_hi], ignore_index=True)
    selected = selected.drop_duplicates(subset=["text"], keep="first").copy()
    if len(selected) != 500000:
        raise ValueError(f"Expected 500,000 unique rows, got {len(selected)}; counts={selected.category.value_counts().to_dict()}")
    selected.loc[selected.source_group_id.eq(""), "source_group_id"] = (
        selected.loc[selected.source_group_id.eq(""), "source"] + "::" + selected.loc[selected.source_group_id.eq(""), "source_row_id"]
    )
    rng = np.random.default_rng(SEED); groups = selected.source_group_id.astype(str).unique().tolist(); rng.shuffle(groups)
    n = len(groups); train = set(groups[:int(n*.8)]); val = set(groups[int(n*.8):int(n*.9)])
    selected["split"] = selected.source_group_id.astype(str).map(lambda g: "train" if g in train else ("validation" if g in val else "test"))
    if set(selected.label.unique()) != set(LABEL_MAP.values()): raise ValueError(f"Label set mismatch: {selected.label.unique()}")
    overlap = {}
    sets = {s: set(selected.loc[selected.split.eq(s), "source_group_id"]) for s in ["train", "validation", "test"]}
    overlap = {"train_validation": len(sets["train"] & sets["validation"]), "train_test": len(sets["train"] & sets["test"]), "validation_test": len(sets["validation"] & sets["test"])}
    if any(overlap.values()): raise ValueError(f"Group leakage: {overlap}")
    cols = ["text","label","split","category","source","source_file","source_row_id","source_group_id","review_status","is_synthetic","generator"]
    selected = selected[cols].sort_values(["split","label","category","source_group_id"], kind="stable")
    for s in ["train","validation","test"]:
        selected[selected.split.eq(s)].drop(columns="split").to_csv(output/f"{s}.csv.gz", index=False, compression="gzip", encoding="utf-8")
    cc = selected.groupby(["split","category"]).size().reset_index(name="count"); lc = selected.groupby(["split","label"]).size().reset_index(name="count")
    cc.to_csv(output/"category_counts.csv", index=False); lc.to_csv(output/"label_counts.csv", index=False)
    manifest = {
      "dataset_name":"multilingual_language_classifier_candidates_v2","plan":"FINAL_DATASET_PLAN.md","seed":SEED,
      "target_rows":500000,"total_rows":len(selected),"labels":sorted(LABEL_MAP.values()),
      "split_rows":selected.split.value_counts().to_dict(),
      "label_counts_by_split":{s:selected[selected.split.eq(s)].label.value_counts().to_dict() for s in ["train","validation","test"]},
      "category_counts":selected.category.value_counts().to_dict(),
      "group_overlap_checks":overlap,"exact_text_duplicates_after_processing":int(selected.text.duplicated().sum()),
      "synthetic_rows":int(selected.is_synthetic.astype(str).str.lower().isin(["true","1"]).sum()),
      "all_rows_unreviewed":True,
      "limitations":["Source labels are not human-verified.","Punjabi-Hindi and Marathi-Hindi are synthetic_unreviewed.",
       "Punjabi-Hindi-English category is generated by English-segment insertion and is synthetic_unreviewed.",
       "Do not use candidate/synthetic rows as independent real-call evaluation.","Verify source licensing and redistribution permissions."]
    }
    (output/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (output/"README.md").write_text("""# Multilingual language-classifier candidates v2

Matches FINAL_DATASET_PLAN.md: 12 labels, 26 categories, 500,000 candidate rows.
24 supported categories target 20,000 rows each; two unsupported-language categories target 10,000 each.
Labels: en-IN, hi-IN, pa-IN, bn-IN, gu-IN, kn-IN, ml-IN, mr-IN, te-IN, as-IN, ta-IN, none.

Synthetic Punjabi-Hindi and Marathi-Hindi rows are included and remain synthetic_unreviewed. The Punjabi-Hindi-English category is created by adding English segments to Punjabi-Hindi synthetic seeds and is also synthetic_unreviewed. This is a candidate pool, not approved training data. Human language review, licensing checks, duplicate/near-duplicate audits, and independent real-call evaluation are required before fine-tuning.
""", encoding="utf-8")
    print(json.dumps({"rows":len(selected),"labels":selected.label.value_counts().to_dict(),"categories":selected.category.value_counts().to_dict(),"splits":selected.split.value_counts().to_dict(),"group_overlap":overlap}, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
