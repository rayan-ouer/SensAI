# HTTP API

Start it from the root of the repository with `wu-api`: it listens on <http://127.0.0.1:8084> and the generated
documentation is on <http://127.0.0.1:8084/docs>. It loads the config set by `CONFIG_PATH` in `.env`.

```
interfaces/api/
  app.py          application, startup and routers
  setup.py        profiles, LLM client and tools loaded once at startup
  chat.py         agent creation and the turn run in a thread
  dependencies.py the conversation service injected in the routes
  routes/         one file per resource, endpoints only
  schemas/input/  request bodies
  schemas/output/ response bodies and stream events
  utils/          helpers used by the routes
```

## Endpoints

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/api/conversations/` | `{"user_id": "..."}` | `{"id": "..."}` |
| `POST` | `/api/conversations/{id}/messages` | `{"content": "...", "profile": "math_tutor", "model": "..."}` | stream of events, see below |
| `GET` | `/api/conversations/{id}/messages` | | `{"messages": [{"role": "user", "content": "..."}, ...]}` |
| `GET` | `/api/profiles` | | `{"profiles": [{"key", "name", "role"}, ...], "default": "wu"}` |
| `GET` | `/api/models` | | `{"models": ["..."], "default": "..."}` |
| `GET` | `/api/spec` | | `{"content": "# Project specification..."}` |
| `GET` | `/api/monitoring/summary` | | Interaction metrics, 14-day series and latest 100 trace events |
| `GET` | `/health` | | `{"status": "ok"}` |
| `GET` | `/version` | | `{"version": "...", "prompt_version": "v2"}` |

`profile` and `model` are optional, the default profile and the `model` of the config answer without them. `model`
must be one of the `models` of the config and the specification update always uses `model`. An unknown conversation
returns 404, an unknown profile or model returns 400.

## The message stream

`POST /api/conversations/{id}/messages` answers with one JSON object per line (`application/x-ndjson`):

```
{"type":"thinking","text":"The user asks..."}
{"type":"content","text":"Pleasure"}
{"type":"content","text":" to meet you."}
{"type":"done"}
{"type":"spec","text":"# Project specification\n..."}
```

| Event | Meaning |
|---|---|
| `thinking` | a piece of the model reasoning, only with models that reason |
| `content` | a piece of the reply |
| `question` | a clarification question with its `options`, the client shows them and sends the choice as the next message |
| `done` | the reply is complete and saved in the conversation, the client can send the next message |
| `spec` | the specification updated from this exchange, the last event of the stream |
| `error` | the turn failed (model, tool loop or unexpected error), the message is not saved, the last event of the stream |

The agent runs in a thread and pushes its chunks in a queue that the response reads. The exchange is saved only when
the agent succeeds, so a failed request leaves the conversation unchanged.

## Logging and monitoring

The API records each chat turn, each model request (including the prompt context sent), and each executed tool call in a
local SQLite database. Events include available prompt/completion token counts, elapsed time, success/error state, model,
profile, and tool arguments/results. The database defaults to `workspace/monitoring.sqlite3`; configure another path with
`MONITOR_DB_PATH`. `/api/monitoring/summary` returns aggregate interaction metrics and the latest 100 events for the
web and Jupyter dashboards. Stored prompt and tool content is plaintext and may contain sensitive data.

## Limits

- Conversations are kept in memory: they are lost when the API restarts. The web interface then starts a new one.
- The agent of the API has the web search and the clarification questions: the file tools ask for approval in the
  terminal and the sandbox is not connected yet.
- A question card disappears when the page is reloaded: the history route does not return the tool calls.
- The specification is a single file shared by every conversation and by the CLI.
