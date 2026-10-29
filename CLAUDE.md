# CLAUDE.md

## Vocabulary flashcards

I mark unfamiliar words in blue while reading, photograph the pages, and ask for them to be added to my Anki deck. Everything lives in `vocabulary/`.

When I send marked pages:

1. Extract every word highlighted in blue. List them back to me with the page number, flagging any mark that is faint or ambiguous, before treating the list as final.
2. Append one row per new word to `vocabulary/<book-slug>.csv` (create the file and add the title to `BOOKS` in `build_anki.py` for a new book). If a word is already in the file, add the new page to its `page` column instead of a second row.
   - `word`: the form used in the book (e.g. "jettisoned", not "jettison")
   - `part_of_speech`
   - `meaning_in_context`: the sense used in **this** sentence, not the most common dictionary sense
   - `synonym`: one simpler word, or "(no exact synonym)"
   - `note`: other common meanings, related forms, or easily confused words
   - `sentence`: the shortest quote from the book that shows the meaning, with the word in `**bold**`. Keep quotes short; never store whole passages.
   - `page`
3. Rebuild the deck: `pip install genanki && python3 vocabulary/build_anki.py`
4. Commit the CSV and `vocabulary/english-vocabulary.apkg`, push, and send me the `.apkg` file so I can open it with AnkiDroid.

Do not change the `MODEL_ID`, `DECK_ID`, or note `guid` scheme in `build_anki.py`: they let re-imports update existing cards without losing review history.
