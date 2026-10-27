# SensAI

![SensAI logo](assets/Logo_SensAI_Wu.svg)

An AI assistant built on [Ollama](https://ollama.com), in the terminal or in the browser. It mentors you on your project as Wu, can switch to specialized tutors and keeps a living specification of your project.

By *Armand Lecomte* (armand.lecomte@epitech.eu), *Rayan Ouerdane* (rayan.ouerdane@epitech.eu) and *Sacha Lemée* (sacha.lemee@epitech.eu).

## Features

- **Agent profiles**: switch during a session between Wu (mentor), Euclid (math tutor), Sensei (Japanese teacher), Ada (code reviewer), Mira (product coach) plus the team profiles Rayan, Sacha and Armand or add your own in `configs/profiles/`.
- **Living specification**: after each answer, `workspace/ASSISTANT.md` is updated with what you said about your project and it is reloaded at the next start. The note-keeper returns only the sections that change, as JSON edits that the code applies.
- **Local or cloud models**: use a model installed on your machine or a larger one on Ollama Cloud.
- **Web search**: the agent searches the web when it needs recent information (MCP tool).
- **Conversation history**: the assistant remembers the previous messages of the conversation.
- **Clarification questions**: when a missing choice blocks the request, the agent asks a closed question with numbered options (human in the loop).
- **Workspace files**: the agent can list, read, create and edit files of the directory you run it from, within the permissions you set.
- **Code sandbox**: the agent runs commands in an isolated Docker container to test your code.
- **Web interface**: streamed replies, model reasoning, specification panel and profile switch in the browser.
- **HTTP API**: conversations, streamed replies, profiles and specification for other interfaces.

In progress: RAG on your documents.

## Installation

Requires Python 3.12+, Ollama, Docker for the sandbox and Node.js 20+ for the web interface.

```sh
# Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# SensAI
git clone git@github.com:EpitechPGE3-2026/G-AIA-500-PAR-5-1-sensai-1.git
cd G-AIA-500-PAR-5-1-sensai-1
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Then pick a model:

- **Local**: `ollama pull qwen2.5:7b`, the model of `configs/local_config.yaml`
- **Cloud**: nothing to download. Create an API key on [ollama.com](https://ollama.com/settings/keys) and set `OLLAMA_API_KEY` in `.env`.

## Usage

### Terminal

```sh
wu -c configs/local_config.yaml   # local model
wu -c configs/cloud_config.yaml   # Ollama Cloud
```

```
Starting Wu
> I want to build a todo list app in Python
Answer:
A fine project. Start small: what should a task contain?
> /profiles
   math_tutor  Euclid
-> wu          Wu
> /profile math_tutor
Switched to 'math_tutor' profile.
> /exit
```

| Command | Effect |
|---|---|
| `/profiles` | list the profiles, `->` marks the active one |
| `/profile <name>` | switch profile |
| `/exit` | quit (or Ctrl+D) |

### Browser

```sh
wu-api                                  # terminal 1, the API on http://127.0.0.1:8084
cd src/app/frontend && npm install      # terminal 2, once
npm run dev                             # then open http://localhost:5173
```

The API uses the config set by `CONFIG_PATH` in `.env`, `configs/local_config.yaml` by default.

## Documentation

| Topic | File |
|---|---|
| Configuration files, profiles, prompts and permissions | [configs/README.md](configs/README.md) |
| HTTP API and the message stream | [src/interfaces/api/README.md](src/interfaces/api/README.md) |
| Web interface | [src/app/frontend/README.md](src/app/frontend/README.md) |
| Workspace files | [src/tools/file_access/README.md](src/tools/file_access/README.md) |
| Clarification questions | [src/tools/human_in_the_loop/README.md](src/tools/human_in_the_loop/README.md) |
| Code sandbox | [src/tools/sandbox/README.md](src/tools/sandbox/README.md) |
| MCP tools | [src/tools/mcp/README.MD](src/tools/mcp/README.MD) |
| User stories | [docs/USER_STORIES.md](docs/USER_STORIES.md) |
| Usage scenario with prompts and expected answers | [docs/SCENARIO.md](docs/SCENARIO.md) |
| Where each requirement and feature is implemented | [docs/TRACEABILITY.md](docs/TRACEABILITY.md) |

## Limits

- **Small local models follow the rules less well**: a 7B model sometimes keeps the previous persona after `/profile`, ignores the brevity rule or answers in another language.
- **Small local models may not call tools**: `qwen2.5-coder:7b` writes the tool call as text instead of running it, use `qwen2.5:7b` or a cloud model for the tools.
- **The specification can drift**: the note-keeper may record suggestions of the assistant that the user never accepted, especially without a low temperature.
- **Answers can be wrong**: the model may invent facts when it does not search the web.
- **Cloud models reason at length**: the thinking part can be much longer than the answer.
- **Conversations are kept in memory**: they are lost when the CLI or the API stops, only the specification persists.
- **One shared specification**: every conversation and the CLI write to the same `ASSISTANT.md`.

## License

This project is licensed under the **MIT License**.

![SensAI MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
