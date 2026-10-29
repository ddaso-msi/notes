# CLAUDE.md

## Vocabulary flashcards

I mark unfamiliar words in blue while reading, photograph the pages, and ask for them to be added to my flashcards. I study them in the **Highlighted Words** app: https://claude.ai/artifact/6QBZ7N6g78SXr4sn5df2cY (source: `vocabulary/app/index.html`). The CSVs in `vocabulary/` are the source of truth for the words; the app's database holds the words plus my study progress.

When I send marked pages:

1. Extract every word highlighted in blue. List them back to me with the page number, flagging any mark that is faint or ambiguous, before treating the list as final.
2. Append one row per new word to `vocabulary/<book-slug>.csv` (for a new book, create the file and add its title and author to `BOOKS` in `export_app_words.py`). If a word is already in the file, add the new page to its `page` column instead of a second row.
   - `word`: the form used in the book (e.g. "jettisoned", not "jettison")
   - `part_of_speech`
   - `meaning_in_context`: the sense used in **this** sentence, not the most common dictionary sense
   - `synonym`: one simpler word, or "(no exact synonym)"
   - `note`: other common meanings, related forms, or easily confused words
   - `sentence`: the shortest quote from the book that shows the meaning, with the word in `**bold**`. Keep quotes short; never store whole passages.
   - `page`
3. Run `python3 vocabulary/export_app_words.py <scratch dir>` and write each new or changed JSON file into the app's `words` collection (doc id = file name without `.json`) with `ArtifactData` `batch` `set` (max 50 per batch; existing docs need `if_version`). Never touch `data/users/...`: that is my study progress.
4. Commit and push the CSV changes.

Don't republish the app page for word changes; only for changes to the app itself. The app reads `word, pos, meaning, synonym, note, sentence, page, book, author, bookSlug, order` from each word document; keep those field names.

`vocabulary/build_anki.py` still builds an Anki deck from the same CSVs if I ever want one; it is not part of the routine.
