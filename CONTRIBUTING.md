# Contributing

## Workflow

1. Pick or open an issue on the project board and set it to *In progress*.
2. Create a branch from `main`: `feat/<topic>`, `fix/<topic>` or `docs/<topic>`.
3. Commit with a prefix: `Feat:`, `Fix:`, `Refactor:` or `Docs:`, then a short sentence of what changes.
4. Open a pull request with a short list of the changes and `Closes #<issue>` (or `Related to #<issue>` when it does
   not finish the issue). Set the issue to *In review*.
5. Another author reviews and merges.

## Code rules

- Python 3.12, functions of 10 lines or fewer, typed parameters and return values.
- Nothing hard-coded: models, prompts and paths come from `configs/`.
- No explanatory comments in the code, the names explain it. A file copied from an external source keeps a one-line
  comment with its source.
- Every file starts with the Epitech header.
- Web interface: `npx tsc -b`, `npx oxlint src` and `npm run build` must pass in `src/app/frontend`.

## Secrets

Never commit `.env` or an API key. `OLLAMA_API_KEY` is read from `.env` and must never be printed.

## Code of conduct

By contributing you agree to follow the [code of conduct](CODE_OF_CONDUCT.md).
