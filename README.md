# SensAI

![SensAI logo](assets/Logo_SensAI_Wu.svg)

An AI assistant built on [Ollama](https://ollama.com), in the terminal or in the browser. It mentors you on your project as Wu, can switch to specialized tutors and keeps a living specification of your project.

By *Armand Lecomte* (armand.lecomte@epitech.eu), *Rayan Ouerdane* (rayan.ouerdane@epitech.eu) and *Sacha Lemée* (sacha.lemee@epitech.eu).

## Features

- **Agent profiles**: switch during a session between Wu (mentor), Euclid (math tutor), Sensei (Japanese teacher), Ada (code reviewer), Mira (product coach) or add your own in `configs/profiles/`.
- **Living specification**: after each answer, `workspace/ASSISTANT.md` is updated with what you said about your project and it is reloaded at the next start. The note-keeper returns only the sections that change, as JSON edits that the code applies.
- **Local or cloud models**: use a model installed on your machine or a larger one on Ollama Cloud.
- **Web search**: the agent searches the web when it needs recent information (MCP tool).
- **Multi-agent**: with `-m`, a coordinator hands parts of the task to specialized agents (research, code, files, review) described in a YAML file.
- **Conversation history**: the assistant remembers the previous messages of the conversation.
- **Clarification questions**: when a missing choice blocks the request, the agent asks a closed question with options, numbered in the terminal and as buttons in the browser (human in the loop).
- **Workspace files**: the agent can list, read, create and edit files of the directory you run it from, within the permissions you set.
- **Code sandbox**: the agent runs commands in an isolated Docker container to test your code.
- **Web interface**: streamed replies, model reasoning, specification panel, profile switch and model choice in the browser.
- **HTTP API**: conversations, streamed replies, profiles and specification for other interfaces.
- **Logging & monitoring**: local interaction traces and dashboards for call volume, latency, errors, token use and response-size drift.
- **Prompt versions and automated eval**: `wu-compare` runs two versions of the prompts on the same messages and a judge agent scores every reply.

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
wu -c configs/cloud_config.yaml -m agents/agent.yaml   # multi-agent, path relative to configs/
```

```
Starting Wu with prompts v2
> I want to build a todo list app in Python
Answer:
A fine project. Start small: what should a task contain?
> /profiles
-> wu              Wu
   math_tutor      Euclid
   sensei          Sensei
   code_reviewer   Ada
   product_coach   Mira
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

Open **Monitoring** in the chat header for the live dashboard. The API stores prompts, model requests and replies, tool
arguments/results, errors, latency and available token counts in `workspace/monitoring.sqlite3`. Set
`MONITOR_DB_PATH` to choose another SQLite file. The database is local and unencrypted; traces can contain sensitive
prompt and tool data.

For the Jupyter dashboard, install its optional dependencies and open `notebooks/monitoring_dashboard.ipynb` from the
repository root:

```sh
pip install -e '.[monitoring]'
jupyter lab notebooks/monitoring_dashboard.ipynb
```

Both dashboards read the same database. The displayed drift metric tracks changes in average completion-token count;
it is an operational response-size signal, not semantic model-quality drift.

## Agents

SensAI always starts with **Wu**, the default agent: a mentor for any subject who guides you towards the answer and
keeps the specification of your project. It is set by `default_profile: "wu"` in the config files. You can switch at any
time with `/profile <name>` in the terminal or the buttons of the header in the browser, the conversation is kept.

| Profile | Agent | Use it for |
|---|---|---|
| `wu` (default) | Wu | any subject, mentoring on your project |
| `math_tutor` | Euclid | mathematics only, high-school level |
| `sensei` | Sensei | Japanese for beginners, explained in your language |
| `code_reviewer` | Ada | reviewing and testing Python code, with the file tools and the sandbox |
| `product_coach` | Mira | defining a project: users, features, priorities, with clarification questions |

Every agent replies in the language of your last message. To add one, drop a YAML file in `configs/profiles/`, see
[configs/README.md](configs/README.md).

## Try it

Start with `wu -c configs/cloud_config.yaml` (or `local_config.yaml`), then:

| Feature | Agent | Type | You should see |
|---|---|---|---|
| Living specification | Wu | `I want to build a todo list app in Python for students` | `workspace/ASSISTANT.md` (or the Specification panel) lists the project |
| Profiles | any | `/profile math_tutor` then `What is the capital of France?` | Euclid declines in one sentence |
| Web search | Wu | `What is the latest version of Python?` | the agent calls `search_web` before answering |
| Clarification questions | Mira | `Help me define my app, I do not know who it is for` | a question with options, numbered or as buttons |
| Workspace files | Ada | `Read README.md and summarise it` | the agent asks to confirm the folder, then reads the file |
| Code sandbox | Ada | `Write a fizzbuzz in Python and run it` | the real output of the script, Docker must be running |
| Prompt versions | - | set `prompt_version: "v1"` in the config and restart | `Starting Wu with prompts v1` |
| Prompt comparison | - | `wu-compare` | `docs/PROMPT_COMPARISON.md` compares v1 and v2 |
| Multi-agent | coordinator | `-m agents/agent.yaml` then `What is the latest version of Python? Check it in the sandbox` | the coordinator hands the search and the check to its agents |
| Automated eval | - | `wu-compare` | each reply has relevance, coherence and faithfulness scores and its flagged claims |

The full scenario with the expected answers is in [docs/SCENARIO.md](docs/SCENARIO.md).

## Documentation

| Topic | File |
|---|---|
| Configuration files, profiles, prompts and permissions | [configs/README.md](configs/README.md) |
| HTTP API and the message stream | [src/interfaces/api/README.md](src/interfaces/api/README.md) |
| Web interface | [src/app/frontend/README.md](src/app/frontend/README.md) |
| Workspace files | [src/tools/file_access/README.md](src/tools/file_access/README.md) |
| Multi-agent files | [configs/README.md](configs/README.md#agents-files) |
| Clarification questions | [src/tools/human_in_the_loop/README.md](src/tools/human_in_the_loop/README.md) |
| Code sandbox | [src/tools/sandbox/README.md](src/tools/sandbox/README.md) |
| MCP tools | [src/tools/mcp/README.MD](src/tools/mcp/README.MD) |
| User stories | [docs/USER_STORIES.md](docs/USER_STORIES.md) |
| Usage scenario with prompts and expected answers | [docs/SCENARIO.md](docs/SCENARIO.md) |
| Where each requirement and feature is implemented | [docs/TRACEABILITY.md](docs/TRACEABILITY.md) |
| Comparison of the prompt versions | [docs/PROMPT_COMPARISON.md](docs/PROMPT_COMPARISON.md) |

## Limits

- **Small local models follow the rules less well**: a 7B model sometimes keeps the previous persona after `/profile`, ignores the brevity rule or answers in another language.
- **Small local models may not call tools**: `qwen2.5-coder:7b` writes the tool call as text instead of running it, use `qwen2.5:7b` or a cloud model for the tools.
- **The specification can drift**: the note-keeper may record suggestions of the assistant that the user never accepted, especially without a low temperature.
- **Answers can be wrong**: the model may invent facts when it does not search the web.
- **Cloud models reason at length**: the thinking part can be much longer than the answer.
- **Conversations are kept in memory**: they are lost when the CLI or the API stops, only the specification persists.
- **One shared specification**: every conversation and the CLI write to the same `ASSISTANT.md`.
- **The CLI needs Docker to start**: the sandbox connects to Docker at start, even if you never run a command.
- **One model server for every agent**: with `-m`, each agent's model must exist where the main model was found, local or cloud.

## License

This project is licensed under the **MIT License**, see [LICENSE.md](LICENSE.md). It belongs in equal shares to its
three [authors](AUTHORS.md). To contribute, read [CONTRIBUTING.md](CONTRIBUTING.md) and the
[code of conduct](CODE_OF_CONDUCT.md). To report a vulnerability, see [SECURITY.md](SECURITY.md).

![SensAI MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
