"""Build an Anki deck (.apkg) from the vocabulary CSV files in this folder.

Usage: pip install genanki && python3 vocabulary/build_anki.py

Each word becomes two cards:
  1. Recognise: the word in its book sentence -> meaning
  2. Recall: the sentence with the word blanked out -> the word

Model, deck and note IDs are fixed, so importing a rebuilt deck updates
existing cards and keeps their review history instead of duplicating them.
"""

import csv
import html
import re
from pathlib import Path

import genanki

HERE = Path(__file__).parent

# CSV filename (without .csv) -> book title shown on the cards
BOOKS = {
    "the-argumentative-indian": "The Argumentative Indian (Amartya Sen)",
}

MODEL_ID = 1730226001
DECK_ID = 1730226002

CSS = """
.card { font-family: sans-serif; font-size: 20px; text-align: center;
        color: #222; background: #fafafa; padding: 12px; }
.nightMode .card, .night_mode .card { color: #eee; background: #1e1e1e; }
.word { font-size: 32px; font-weight: bold; margin: 8px 0; }
.sentence { font-style: italic; margin: 16px 0; line-height: 1.5; }
.hint { color: #888; font-size: 16px; }
.meaning { font-size: 22px; margin: 12px 0; }
.detail { font-size: 16px; color: #666; margin: 6px 0; }
.nightMode .detail, .night_mode .detail { color: #aaa; }
.source { font-size: 13px; color: #999; margin-top: 20px; }
"""

ANSWER_DETAILS = """
<div class="meaning">{{Meaning}}</div>
<div class="detail"><i>{{PartOfSpeech}}</i> · ≈ {{Synonym}}</div>
{{#Note}}<div class="detail">{{Note}}</div>{{/Note}}
<div class="source">{{Source}}, p. {{Page}}</div>
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Book Vocabulary",
    fields=[
        {"name": "Word"},
        {"name": "Sentence"},
        {"name": "BlankedSentence"},
        {"name": "Meaning"},
        {"name": "PartOfSpeech"},
        {"name": "Synonym"},
        {"name": "Note"},
        {"name": "Page"},
        {"name": "Source"},
    ],
    templates=[
        {
            "name": "Recognise",
            "qfmt": '<div class="word">{{Word}}</div>'
                    '<div class="sentence">{{Sentence}}</div>'
                    '<div class="hint">What does it mean here?</div>',
            "afmt": '{{FrontSide}}<hr id="answer">' + ANSWER_DETAILS,
        },
        {
            "name": "Recall",
            "qfmt": '<div class="sentence">{{BlankedSentence}}</div>'
                    '<div class="hint">{{Meaning}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">'
                    '<div class="word">{{Word}}</div>'
                    '<div class="sentence">{{Sentence}}</div>'
                    '<div class="detail"><i>{{PartOfSpeech}}</i> · ≈ {{Synonym}}</div>',
        },
    ],
    css=CSS,
)

BOLD = re.compile(r"\*\*(.+?)\*\*")


def blank(sentence):
    """Replace the bolded word with its first letter and a gap, e.g. 'j________'."""
    return BOLD.sub(lambda m: m.group(1)[0] + "_" * 8, sentence)


def main():
    deck = genanki.Deck(DECK_ID, "English Vocabulary")
    total = 0
    for csv_path in sorted(HERE.glob("*.csv")):
        slug = csv_path.stem
        title = BOOKS.get(slug, slug.replace("-", " ").title())
        with csv_path.open(newline="") as f:
            for row in csv.DictReader(f):
                sentence = html.escape(row["sentence"], quote=False)
                note = genanki.Note(
                    model=MODEL,
                    fields=[
                        row["word"],
                        BOLD.sub(r"<b>\1</b>", sentence),
                        blank(sentence),
                        html.escape(row["meaning_in_context"], quote=False),
                        row["part_of_speech"],
                        html.escape(row["synonym"], quote=False),
                        html.escape(row["note"], quote=False),
                        row["page"],
                        html.escape(title, quote=False),
                    ],
                    tags=[slug],
                    guid=genanki.guid_for(slug, row["word"]),
                )
                deck.add_note(note)
                total += 1
    out = HERE / "english-vocabulary.apkg"
    genanki.Package(deck).write_to_file(out)
    print(f"{total} words ({total * 2} cards) -> {out}")


if __name__ == "__main__":
    main()
