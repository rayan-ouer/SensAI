# Traceability

Each requirement of the subject and each feature of [USER_STORIES.md](USER_STORIES.md) mapped to the code that implements it and to the way to check it. The scenario steps refer to [SCENARIO.md](SCENARIO.md).

## Base loop (subject)

| Requirement                      | Implementation                                                                       | How to check                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Streaming responses              | `src/llm/ollama/ollama_stream.py`, `src/interfaces/cli/display.py`                   | the answer is printed while it is generated                      |
| In-session history               | `src/interfaces/cli/chat.py`                                                         | "My name is Eon" then "What is my name?"                         |
| Clean error handling             | `src/tools/chat/errors.py`, `src/tools/chat/module.py`, `src/interfaces/cli/chat.py` | missing config file, unknown model, network cut during a session |
| Model chosen without code change | `configs/*.yaml`, `src/tools/chat/load_config.py`                                    | change `model` in the config file                                |

## Features

| Feature                       | Implementation                                                                                  | How to check                                                        |
| ----------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Agent profiles                | `configs/profiles/`, `src/tools/agent/profiles.py`, `src/tools/chat/commands.py`                | scenario steps 3 and 4                                              |
| Living specification          | `configs/prompt/spec.txt`, `src/tools/spec/spec.py`, `src/tools/chat/chat_loop.py`              | scenario steps 1, 2 and 6                                           |
| Local and cloud models        | `src/tools/chat/create_client.py`, `src/tools/chat/model_list.py`, `src/tools/chat/settings.py` | run with `local_config.yaml` then `cloud_config.yaml`               |
| Tool-using agent              | `src/agent/agent.py`                                                                            | scenario step 5                                                     |
| Web search through MCP        | `src/tools/search/web.py`, `src/tools/mcp/`                                                     | scenario step 5                                                     |
| Code sandbox                  | `src/tools/sandbox/sandbox.py` (tool `execute_command`)                                         | ask to run a script, Docker must be running (CLI only)              |
| Clarification questions       | `src/tools/human_in_the_loop/`, `configs/prompt/system.txt`                                     | ask for a project with a missing choice (CLI only)                  |
| Workspace files               | `src/tools/file_access/`, `configs/file_access.yaml`                                            | ask to read a file of the project (CLI only)                        |
| HTTP API                      | `src/interfaces/api/`                                                                           | the requests listed in `src/interfaces/api/README.md`               |
| Web interface                 | `src/app/frontend/`                                                                             | chat, reasoning, specification panel, profile switch, page reload   |
| Document knowledge base (RAG) | `src/tools/loader/`, `src/tools/rag/`                                                           | loading, chunking and embedding only, retrieval not implemented yet |
