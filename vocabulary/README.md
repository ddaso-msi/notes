# Vocabulary

Words marked while reading, with the sentence each one appeared in.

- [the-argumentative-indian.csv](the-argumentative-indian.csv): *The Argumentative Indian*, Amartya Sen

Columns: `word`, `part_of_speech`, `meaning_in_context`, `synonym`, `note`, `sentence` (with the word in `**bold**`), `page`.

## Highlighted Words app

Study the words at https://claude.ai/artifact/6QBZ7N6g78SXr4sn5df2cY (source: [app/index.html](app/index.html)).

- Two buttons: **I knew this word** / **I didn't know this word**
- Words you know come back after 1, 3, 7, 21 and 60 days; a word you miss starts over and comes back later in the same session
- After two correct answers a card switches to fill-in-the-blank
- Level 3 or above counts as mastered; progress shows per book

`export_app_words.py` turns the CSVs into one JSON document per word for the app's `words` collection.

## Anki (optional)

`build_anki.py` builds `english-vocabulary.apkg` from the same CSVs (`pip install genanki`).
