#!/usr/bin/env python3
"""Auditable dataset candidate checks for the multilingual mixed-script classifier.

This tool intentionally creates CANDIDATE outputs only. It never marks rows approved.
Run: python scripts/dataset_prep_pipeline.py --input PATH.csv --text-column text --category Bengali-English --label bn-IN
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import pandas as pd

LABELS = {"en-IN","hi-IN","pa-IN","bn-IN","gu-IN","kn-IN","ml-IN","mr-IN","te-IN","as-IN","ta-IN","none"}
SCRIPT_RANGES = {
    "hi-IN": r"[\u0900-\u097F]",  # Devanagari (Hindi and Marathi; language must be reviewed separately)
    "pa-IN": r"[\u0A00-\u0A7F]",  # Gurmukhi
    "bn-IN": r"[\u0980-\u09FF]",  # Bengali/Assamese blocks overlap in Unicode; review language identity
    "gu-IN": r"[\u0A80-\u0AFF]",
    "kn-IN": r"[\u0C80-\u0CFF]",
    "ml-IN": r"[\u0D00-\u0D7F]",
    "te-IN": r"[\u0C00-\u0C7F]",
    "as-IN": r"[\u0980-\u09FF]",
    "ta-IN": r"[\u0B80-\u0BFF]",
}
MIXED_SCRIPT_CATEGORIES = {
    "Hindi-English": ("hi-IN", r"[\u0900-\u097F]"),
    "Punjabi-English": ("pa-IN", r"[\u0A00-\u0A7F]"),
    "Bengali-English": ("bn-IN", r"[\u0980-\u09FF]"),
    "Gujarati-English": ("gu-IN", r"[\u0A80-\u0AFF]"),
    "Kannada-English": ("kn-IN", r"[\u0C80-\u0CFF]"),
    "Malayalam-English": ("ml-IN", r"[\u0D00-\u0D7F]"),
    "Marathi-English": ("mr-IN", r"[\u0900-\u097F]"),
    "Telugu-English": ("te-IN", r"[\u0C00-\u0C7F]"),
    "Assamese-English": ("as-IN", r"[\u0980-\u09FF]"),
    "Tamil-English": ("ta-IN", r"[\u0B80-\u0BFF]"),
}
REQUIRED = ["text","label","language_category","source_dataset","source_url","source_row_id",
            "group_id","source_split","is_synthetic","review_status","license_status"]

def normalize(text: object) -> str:
    return re.sub(r"\s+", " ", str(text).casefold()).strip()

def audit_file(args: argparse.Namespace) -> None:
    source = Path(args.input)
    df = pd.read_csv(source, low_memory=False)
    text_col = args.text_column
    if text_col not in df.columns:
        raise ValueError(f"Text column {text_col!r} missing. Available: {list(df.columns)}")
    if args.label not in LABELS:
        raise ValueError(f"Unsupported label: {args.label!r}; allowed labels: {sorted(LABELS)}")
    if args.category in MIXED_SCRIPT_CATEGORIES:
        expected_label, native_script = MIXED_SCRIPT_CATEGORIES[args.category]
        if args.label != expected_label:
            raise ValueError(f"{args.category} must use {expected_label}, not {args.label}")
    else:
        native_script = None

    out = df.copy()
    out["source_row_id"] = out.get("source_row_id", pd.Series(range(len(out))))
    out["text"] = out[text_col].fillna("").astype(str).str.strip()
    out["normalized_text"] = out["text"].map(normalize)
    out["label"] = args.label
    out["language_category"] = args.category
    out["source_dataset"] = args.source_name or source.stem
    out["source_url"] = args.source_url or ""
    out["group_id"] = out["group_id"] if "group_id" in out.columns else out["source_row_id"].astype(str)
    out["source_split"] = out["source_split"] if "source_split" in out.columns else "unknown"
    out["is_synthetic"] = out["is_synthetic"] if "is_synthetic" in out.columns else False
    out["review_status"] = "pending_manual_language_and_quality_review"
    out["license_status"] = args.license_status
    out["has_latin_letters"] = out["text"].str.contains(r"[A-Za-z]", regex=True)
    if native_script:
        out["has_native_script"] = out["text"].str.contains(native_script, regex=True)
        out["passes_two_script_gate"] = out["has_native_script"] & out["has_latin_letters"]
        candidates = out[out["passes_two_script_gate"] & out["normalized_text"].ne("")].copy()
    else:
        out["passes_two_script_gate"] = pd.NA
        candidates = out[out["normalized_text"].ne("")].copy()

    duplicate_rows = int(candidates["normalized_text"].duplicated().sum())
    report = {
        "input_file": str(source), "input_rows": int(len(df)),
        "nonempty_rows": int(out["normalized_text"].ne("").sum()),
        "category": args.category, "candidate_label": args.label,
        "candidate_rows_before_dedup": int(len(candidates)),
        "unique_normalized_candidate_texts": int(candidates["normalized_text"].nunique()),
        "duplicate_rows_after_casefold_whitespace_normalization": duplicate_rows,
        "mixed_script_gate_applied": bool(native_script),
        "rows_passing_both_script_gate": int(len(candidates)) if native_script else None,
        "license_status": args.license_status,
        "approval_status": "NOT_APPROVED_CANDIDATES_ONLY",
        "notes": "Script checks are necessary but not sufficient. Review actual language use, brand-only cases, quality, licensing, provenance, and source splits."
    }
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = out_dir / f"{source.stem}_{args.category.lower().replace('-', '_').replace(' ', '_')}_candidates.csv"
    report_path = out_dir / f"{source.stem}_audit.json"
    candidates.drop(columns=["normalized_text"], errors="ignore").to_csv(candidate_path, index=False)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Candidate CSV: {candidate_path}")
    print(f"Audit JSON: {report_path}")

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Input CSV path")
    p.add_argument("--text-column", default="text")
    p.add_argument("--category", required=True, choices=[
        "English-only","Hindi-only","Hindi-English","Punjabi-only","Punjabi-Hindi",
        "Punjabi-English","Punjabi-Hindi-English","Bengali-only","Bengali-English",
        "Gujarati-only","Gujarati-English","Kannada-only","Kannada-English",
        "Malayalam-only","Malayalam-English","Marathi-only","Marathi-English","Marathi-Hindi",
        "Telugu-only","Telugu-English","Assamese-only","Assamese-English","Tamil-only","Tamil-English",
        "Unsupported-only","Unsupported-English"])
    p.add_argument("--label", required=True, choices=sorted(LABELS))
    p.add_argument("--source-name")
    p.add_argument("--source-url")
    p.add_argument("--license-status", default="review_required")
    p.add_argument("--output-dir", default="data/interim/candidates")
    audit_file(p.parse_args())

if __name__ == "__main__":
    main()
