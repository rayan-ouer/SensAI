# Traceability

Each requirement of the subject and each feature, with its ID in the features catalog of [USER_STORIES.md](USER_STORIES.md) mapped to the code that implements it and to the way to check it. The scenario steps refer to [SCENARIO.md](SCENARIO.md).

## Base loop (subject, catalog B1)

| Requirement                      | Implementation                                                                       | How to check                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Streaming responses              | `src/llm/ollama/ollama_stream.py`, `src/interfaces/cli/display.py`                   | the answer is printed while it is generated                      |
| In-session history               | `src/interfaces/cli/chat.py`                                                         | "My name is Eon" then "What is my name?"                         |
| Clean error handling             | `src/tools/chat/errors.py`, `src/tools/chat/module.py`, `src/interfaces/cli/chat.py` | missing config file, unknown model, network cut during a session |
| Model chosen without code change | `configs/*.yaml`, `src/tools/chat/load_config.py`                                    | change `model` in the config file                                |

## Features

| Catalog | Feature                         | Implementation                                                                                                                                       | How to check                                                                            |
| ------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| A5      | Agent profiles (persona)        | `configs/profiles/`, `configs/prompt/`, `src/tools/agent/profiles.py`, `src/tools/chat/commands.py`                                                  | scenario steps 3 and 4, a reply in English to an English message                        |
| M4      | Living specification            | `configs/prompt/spec.txt`, `src/tools/spec/spec.py`, `src/tools/chat/chat_loop.py`                                                                   | scenario steps 1, 2 and 6                                                               |
| T5      | Structured output               | `EDIT_SCHEMA` in `src/tools/spec/spec.py`, `response_format` in the config                                                                           | the note-keeper returns JSON edits, only the changed sections are rewritten             |
| A1      | Tool-using agent (ReAct loop)   | `src/agent/agent.py`                                                                                                                                 | scenario step 5                                                                         |
| T1, T3  | Web search through MCP          | `src/tools/search/web.py`, `src/tools/mcp/`                                                                                                          | scenario step 5                                                                         |
| T2      | Code sandbox                    | `src/tools/sandbox/sandbox.py` (tool `execute_command`)                                                                                              | ask to run a script, Docker must be running (CLI only)                                  |
| X4      | Clarification questions         | `src/tools/human_in_the_loop/`, `src/interfaces/api/chat.py`, `configs/prompt/question.txt`, `src/app/frontend/src/components/chat/QuestionCard.tsx` | ask Mira to help define a project without a target user, in the terminal or the browser |
| T4      | Workspace files                 | `src/tools/file_access/`, `configs/file_access.yaml`                                                                                                 | ask to read a file of the project (CLI only)                                            |
| A3      | Approval before changing a file | `write_in_file` in `src/tools/file_access/file_access.py`                                                                                            | ask Ada to edit a file and answer `N`, the file is unchanged (CLI only)                 |
|         | HTTP API                        | `src/interfaces/api/`                                                                                                                                | the requests listed in `src/interfaces/api/README.md`                                   |
| X1      | Web interface                   | `src/app/frontend/`                                                                                                                                  | chat, reasoning, specification panel, profile switch, question card, page reload        |
| R1      | Document knowledge base (RAG)   | `src/tools/loader/`, `src/tools/rag/`                                                                                                                | loading, chunking and embedding only, retrieval not implemented yet                     |
