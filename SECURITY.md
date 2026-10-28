# Security

## Reporting a vulnerability

Do not open a public issue. Send a private email to the authors listed in [AUTHORS.md](AUTHORS.md) with the steps to
reproduce the problem. You will get an answer within a week.

## How SensAI protects you

- The Ollama Cloud API key stays in `.env`, which is ignored by git, and is never printed.
- Commands run by the agent execute in a Docker container, separate from your files.
- The file tools only reach the paths allowed by `configs/file_access.yaml` and every edit asks for your approval.

## Known limits

- The HTTP API has no authentication and allows every origin: run it on your own machine only.
- Answers come from a language model and can be wrong. Check them before running generated code outside the sandbox.
