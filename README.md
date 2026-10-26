# SensAI

![SensAI logo](assets/Logo_SensAI_Wu.svg)

An AI assistant for the command line, built on [Ollama](https://ollama.com). It mentors you on your project as Wu, can switch to specialized tutors and keeps a living specification of your project.

By *Armand Lecomte* (armand.lecomte@epitech.eu), *Rayan Ouerdane* (rayan.ouerdane@epitech.eu) and *Sacha Lemée* (sacha.lemee@epitech.eu).

## Features

- **Agent profiles**: switch between Wu (mentor) and Euclid (math tutor) during a session or add your own in `configs/profiles/`.
- **Living specification**: after each answer, `workspace/ASSISTANT.md` is updated with what you said about your project and it is reloaded at the next start.
- **Local or cloud models**: use a model installed on your machine or a larger one on Ollama Cloud.
- **Web search**: the agent searches the web when it needs recent information (MCP tool).
- **Conversation history**: the assistant remembers the previous messages of the session.
- **Clarification questions**: when a missing choice blocks the request, the agent asks a closed question with numbered options (human in the loop).
- **Workspace files**: the agent can list, read, create and edit files of the directory you run it from, within the permissions you set.

In progress: RAG on your documents, code sandbox, HTTP API, web frontend.

- [USER_STORIES.md](USER_STORIES.md): the use cases of each feature
- [SCENARIO.md](SCENARIO.md): a full usage scenario with prompts and expected answers
- [TRACEABILITY.md](TRACEABILITY.md): where each requirement and feature is implemented

## Installation

Requires Python 3.12+ and Ollama.

```sh
# Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# SensAI
git clone git@github.com:EpitechPGE3-2026/G-AIA-500-PAR-5-1-sensai-1.git
cd G-AIA-500-PAR-5-1-sensai-1
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

Then pick a model:

- **Local**: `ollama pull qwen2.5-coder:7b`
- **Cloud**: nothing to download. Create an API key on [ollama.com](https://ollama.com/settings/keys), then `cp .env.example .env` and set `OLLAMA_API_KEY`.

## Usage

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

Every key of the configuration files is described in [configs/config.yaml.example](configs/config.yaml.example).

## File access

At the first file operation, the agent asks you to confirm the working directory. Every write asks for your approval.
Permissions are set in `configs/file_access.yaml`, the most specific path wins and a path without a rule is denied:

```yaml
permissions:
  ".": read
  "src": read_write
```

See [src/tools/file_access/README.md](src/tools/file_access/README.md) for the details.

## Limits

- **Small local models follow the rules less well**: a 7B model sometimes keeps the previous persona after `/profile` and ignores the brevity rule.
- **The specification can drift**: the note-keeper may record suggestions of the assistant that the user never accepted, especially without a low temperature.
- **Answers can be wrong**: the model may invent facts when it does not search the web.
- **Cloud models reason at length**: the thinking part can be much longer than the answer.
- **One conversation at a time**: the history is kept in memory and lost when the session ends, only the specification persists.

## License

This project is licensed under the **MIT License**.

![SensAI MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
