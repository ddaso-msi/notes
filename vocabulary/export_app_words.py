"""Export the vocabulary CSVs as one JSON document per word for the Highlighted Words app.

Usage: python3 vocabulary/export_app_words.py OUT_DIR

Writes OUT_DIR/<doc_id>.json for each word. Claude then writes these into the
app's `words` collection (doc id = file name) with the ArtifactData tool.
"""

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

# CSV filename (without .csv) -> (title, author)
BOOKS = {
    "the-argumentative-indian": ("The Argumentative Indian", "Amartya Sen"),
}


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for csv_path in sorted(HERE.glob("*.csv")):
        slug = csv_path.stem
        title, author = BOOKS.get(slug, (slug.replace("-", " ").title(), ""))
        with csv_path.open(newline="") as f:
            for order, row in enumerate(csv.DictReader(f)):
                doc_id = slug + "~" + re.sub(r"[^a-z0-9-]+", "-", row["word"].lower()).strip("-")
                doc = {
                    "word": row["word"],
                    "pos": row["part_of_speech"],
                    "meaning": row["meaning_in_context"],
                    "synonym": row["synonym"],
                    "note": row["note"],
                    "sentence": row["sentence"],
                    "page": row["page"],
                    "book": title,
                    "author": author,
                    "bookSlug": slug,
                    "order": order,
                }
                (out / f"{doc_id}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2))
                print(doc_id)


if __name__ == "__main__":
    main(sys.argv[1])
