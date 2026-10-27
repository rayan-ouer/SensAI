# Configuration

Everything SensAI does is set in this folder: the model, the prompts, the agent profiles and the file permissions.
Nothing about Wu or Euclid is written in the code.

```
configs/
  local_config.yaml     main config for a local model
  cloud_config.yaml     main config for an Ollama Cloud model
  config.yaml.example   every key with its type and default value
  file_access.yaml      permissions of the workspace file tools
  profiles/             one YAML file per agent profile
  prompt/               the text prompts referenced by the files above
```

## Main config file

The CLI takes it with `wu -c configs/local_config.yaml`. The API reads the one set by `CONFIG_PATH` in `.env`
(`configs/local_config.yaml` by default).

| Key | Required | Type | Role |
|---|---|---|---|
| `model` | yes | string | model name, local (`ollama list`) or on Ollama Cloud |
| `system_prompt` | yes | path | general rules shared by every profile |
| `spec_prompt` | yes | path | instructions of the note-keeper that updates the specification |
| `spec_path` | yes | path | the living specification, created if missing |
| `profiles_dir` | yes | path | folder of the agent profiles |
| `default_profile` | yes | string | profile active at start, a file name of `profiles_dir` without `.yaml` |
| `spec_think` | no | bool | model reasoning during specification updates, `false` is faster |
| `think` | no | bool | model reasoning for chat replies, by default the model decides |
| `max_loops` | no | int | maximum agent steps (model and tool calls) for one message, 10 by default |
| `llm_settings` | no | dict | options passed to the model, for example `{temperature: 0.2, top_k: 50}` |
| `ollama_provider` | no | string | `auto` (local then cloud), `local` or `cloud`, `auto` by default |
| `file_access_config` | no | path | permissions file of the file tools, `file_access.yaml` by default |
| `response_format` | no | dict | JSON schema the replies must follow, free text by default |

Paths are relative to the config file, except `spec_path` which is relative to the folder you start SensAI from.
A missing required key or an invalid `ollama_provider` stops the program with a clear error and exit code 84.

## Environment variables

Copy `.env.example` to `.env` at the root of the repository.

| Variable | Role |
|---|---|
| `OLLAMA_API_KEY` | key for Ollama Cloud, only needed for cloud models |
| `CONFIG_PATH` | main config file used by the API |
| `OLLAMA_LOCAL_HOST`, `OLLAMA_CLOUD_HOST` | Ollama addresses, the defaults are `http://localhost:11434` and `https://ollama.com` |
| `CONVERSATION_STORAGE` | where the API keeps conversations, `memory` by default |

## Agent profiles

Each file of `profiles/` is a profile, named after the file (`wu.yaml` gives the profile `wu`).
`profile.schema.json` lets editors check the format.

```yaml
name: "Euclid"
role: "a mathematics tutor for high-school students"
tone: "patient, precise, encouraging"
scope: "Only answer questions about mathematics. Politely decline anything else."
prompt: "prompt/math_tutor.txt"
```

`name`, `role`, `tone` and `scope` are required. `prompt` is an optional text file with detailed instructions,
relative to `configs/`. To add a tutor, drop a new YAML file here: it appears in `/profiles` and in the web interface
at the next start.

## Prompts

| File | Used by |
|---|---|
| `prompt/system.txt` | every profile: honesty, brevity, scope, language and the rules of each tool |
| `prompt/spec.txt` | the note-keeper: sections of the specification, what it may record and the JSON edits it returns |
| `prompt/wu.txt`, `prompt/math_tutor.txt`, `prompt/sensei.txt`, `prompt/code_reviewer.txt`, `prompt/product_coach.txt`, `prompt/rayan.txt` | the detailed persona of each profile |

The system prompt sent to the model is built from three layers: `system.txt`, the active profile and the current
specification. In the CLI, the workspace directory and its listing are added at the end.

## File permissions

`file_access.yaml` sets what the file tools may do, relative to the folder SensAI is started from.

```yaml
permissions:
  ".": read
  "src": read_write
```

The most specific path wins and a path without a rule is denied. `read` allows `list` and `read_file`,
`read_write` also allows `create_file`. Every `write_in_file` asks the user for approval.
