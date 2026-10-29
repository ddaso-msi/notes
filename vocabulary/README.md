# Vocabulary

Words marked while reading, with the sentence each one appeared in.

- [the-argumentative-indian.csv](the-argumentative-indian.csv): *The Argumentative Indian*, Amartya Sen

Columns: `word`, `part_of_speech`, `meaning_in_context`, `synonym`, `note`, `sentence` (with the word in `**bold**`), `page`.

## Anki

`english-vocabulary.apkg` is built from the CSV files:

```
pip install genanki
python3 vocabulary/build_anki.py
```

Each word gives two cards: **Recognise** (word in its sentence → meaning) and **Recall** (sentence with the word blanked → word). Notes have fixed IDs, so importing a rebuilt deck updates existing cards without losing review history.
