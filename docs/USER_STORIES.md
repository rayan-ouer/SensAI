# User stories

## Local and cloud models (B1)

As a student working on confidential material, I want the assistant to run on a
model installed on my computer, so that nothing I write leaves it.

Acceptance criteria:
- With a locally installed model named in the configuration file, the assistant
  answers without any API key.
- Changing the `model` key and restarting changes the model used, with no code
  change.
- A model that exists neither locally nor in the cloud stops the program with
  `<model>: not found neither locally nor in the cloud` and exit code 84.

As a student with a modest laptop, I want to use a model hosted on Ollama Cloud,
so that I get good answers without downloading or running the model myself.

Acceptance criteria:
- With `OLLAMA_API_KEY` set in `.env` and a cloud model in the configuration
  file, the assistant answers although the model is not installed locally.
- When a model exists both locally and in the cloud, the local one is used.
- The API key is never printed, including in error messages.
- An invalid configuration path stops the program with
  `config file not found: <path>` and exit code 84.

## Living project specification (M4, T5)

As a student who works on a project over several days, I want the assistant to
remember what the project is, so that I do not have to explain it again at each
session.

Acceptance criteria:
- After I describe my project, the file set by `spec_path`
  (`workspace/ASSISTANT.md` by default) contains an overview of it.
- After a restart, asking "what is my project?" gives an answer consistent with
  that file.
- If the file does not exist at start, the assistant starts normally and creates
  it after the first exchange.

As a student in a team, I want the specification to be updated after each
exchange, so that I always have a current document to show my teammates.

Acceptance criteria:
- A requirement stated in the conversation appears in the file after the answer,
  under the matching section.
- The file always starts with a Markdown title and never contains internal tags
  or code fences around the whole document.
- A greeting, an off-topic question or a question about the assistant itself
  does not add requirements to the file.
- The note-keeper returns JSON edits that follow a fixed schema and only the
  sections it names are rewritten, the others stay exactly as they were.
- If the update fails or is interrupted, a warning is printed, the previous file
  is kept and the session continues.

## MCP tool integration (T1)

As a developer, I want the agent to use tools exposed by an MCP server, so that I
can reuse existing tools instead of rewriting them for SensAI.

Acceptance criteria:
- Tools declared on a FastMCP server are listed by the MCP adapter with their
  name, description and arguments.
- Once registered, the agent can call them like any local tool.
- The web search tool is delivered this way, through the `sensai-search`
  server.

As a developer, I want to add a tool by writing a single documented function, so
that giving the agent a new ability takes minutes.

Acceptance criteria:
- A function decorated with `@mcp.tool` becomes available to the agent at the
  next start, with its docstring as description.
- A call to an unknown tool returns an error result to the agent instead of
  stopping the program.
- An exception raised inside a tool is returned to the agent as an error result.

## Code sandbox (T2)

As a student learning to program, I want the assistant to run my code in an
isolated container, so that a mistake cannot damage my files.

Acceptance criteria:
- When I ask to run or test a script, the agent calls the `execute_command`
  tool and answers from its real output.
- The command runs in a Docker container, in `/work`, separate from the project
  directory on the host.
- The result given to the agent contains `stdout`, `stderr`, `exit_code` and
  `timed_out`.
- A command running longer than 20 seconds is stopped and reported as timed out.

As a student working on an exercise in several steps, I want files created in
one command to be there for the next, so that the assistant can build and then
test my program.

Acceptance criteria:
- A file created by one command is visible to the next command of the same
  conversation.
- Each conversation has its own sandbox volume.
- A failing command is reported to the agent with its exit code and error
  output, so it can fix the script and try again.

## Tool-using agent and web search (T3, A1)

As a student, I want the assistant to look up the web when a question needs
recent information, so that its answer is not limited to what the model learnt.

Acceptance criteria:
- For a question about a recent event, the agent calls the `search_web` tool
  before answering.
- The tool returns a numbered list of results with title, URL and snippet,
  limited to 10 results.
- For a question it can answer on its own, such as a greeting, the agent answers
  without calling a tool.

As a student, I want the session to survive a failed search or a tool loop, so
that one bad request does not make me lose my conversation.

Acceptance criteria:
- When the search fails (no network), the agent receives the error as the tool
  result and still gives an answer.
- When the agent chains tool calls beyond the limit (`max_loops`, 10 by
  default), an error is printed and the turn is removed from the history.
- After either failure, the prompt comes back and the next message is answered
  normally.

## Workspace files (T4)

As a student, I want the assistant to read the files of my project, so that its
advice is based on my real code.

Acceptance criteria:
- At the first file operation, I confirm the working directory or choose
  another one.
- `list` and `read_file` work on the paths allowed by `configs/file_access.yaml`.
- A path outside the working directory or without a rule is refused with an
  error the agent can explain.

## Document knowledge base (R1)

As a student, I want to give my course documents to the assistant, so that its
answers rely on my teacher's material rather than on general knowledge.

Acceptance criteria:
- PDF, Markdown, CSV and plain text files can be loaded.
- A loaded document is split into chunks and each chunk is embedded.
- An unsupported file type gives a clear error and does not stop the session.

As a student revising for an exam, I want the assistant to retrieve the passages
related to my question, so that I do not have to search a long document myself.

Acceptance criteria:
- A question returns the stored chunks closest to it.
- The number of chunks returned is limited to a configurable maximum.
- The answer is built from the retrieved passages.

## Approval before changing a file (A3)

As a student, I want to approve every change to my files, so that the
assistant never overwrites my work without my consent.

Acceptance criteria:
- Every `write_in_file` call asks me `[y/N]` before writing and a refusal
  leaves the file unchanged.
- `create_file` needs a `read_write` permission and never replaces an existing
  file.

## Prompt versioning (A4)

As a developer tuning the assistant, I want each version of the global prompts
kept with its date and changes, so that I can go back to a previous one when a
change makes the answers worse.

Acceptance criteria:
- Each folder of `configs/prompt/versions/` holds `system.txt`, `spec.txt`,
  `question.txt` and a `version.yaml` with its date and what changed.
- `prompt_version` in the configuration file selects the folder and writing
  the previous version there rolls back, with no code change.
- An unknown version stops the program with `prompt version not found: <path>`
  and exit code 84.
- The CLI start message and `GET /version` show the version in use.
- `wu-compare` sends the messages of `configs/prompt_comparison.yaml` with each
  version and writes `docs/PROMPT_COMPARISON.md`: mean latency, prompt and reply
  tokens and the replies side by side.

## Agent profiles (A5)

As a student working on several subjects, I want to switch the assistant to a
specialized tutor without restarting, so that I keep my conversation while
getting answers in the right domain.

Acceptance criteria:
- `/profiles` lists the available profiles and marks the active one with `->`.
- `/profile math_tutor` prints `Switched to 'math_tutor' profile.` and the next
  answer is given under the name Euclid.
- A question outside the active profile's scope is declined in one sentence.
- `/profile unknown` prints `Unknown profile: 'unknown'. Type /profiles to see
  available ones.` and the active profile does not change.
- Every profile replies in the language of my last message and says "tu" in
  French, never "vous".
- Asked what it is, the assistant answers with its profile name and role and
  never names the underlying model.

As a teacher, I want to describe a new tutor in a YAML file, so that I can adapt
the assistant to my class without asking a developer.

Acceptance criteria:
- A file added to `configs/profiles/` with `name`, `role`, `tone` and `scope`
  appears in `/profiles` at the next start.
- The profile named by `default_profile` in the configuration file is the one
  active at start and the start message shows its name.
- An optional `prompt` key points to a text file whose instructions are added to
  the tutor's behavior.
- An optional `order` key sets the position of the tutor in `/profiles` and in
  the web interface, lowest first.
- A profile file with a missing key stops the program with exit code 84 and an
  error naming the missing key and the file.

## Web interface (X1)

As a student who prefers a browser to a terminal, I want to chat with SensAI in
a web page, so that I can follow the answer and the specification side by side.

Acceptance criteria:
- The reply is displayed while it is generated and the model reasoning can be
  unfolded above it.
- A side panel shows the specification and refreshes after each reply, while I
  can already type the next message.
- I can switch between the profiles (Wu, Euclid, Sensei, Ada, Mira) from the
  header and the next reply comes from the chosen profile.
- After a page reload, the conversation is displayed again and "New
  conversation" starts an empty one.
- If the API is not running, a readable error is shown instead of a blank page.

## Clarification questions (X4)

As a student describing a project, I want the assistant to ask me when a choice
is missing instead of guessing, so that it builds what I actually want.

Acceptance criteria:
- When a missing choice blocks the request, the agent calls `human_in_the_loop`
  and a numbered menu of options is shown.
- The menu always ends with an "Other free-form answer" choice.
- An invalid number is asked again and the selected answer is sent back to the
  agent.
- The agent does not ask about details already given in the conversation or in
  the specification.

As a student, I want my answers to these questions to be kept in the
specification, so that I do not have to give them again later.

Acceptance criteria:
- After the turn, the specification contains the choice I selected.
- A question asked with fewer than two options is refused as a tool error and
  the session continues.

As a student using the browser, I want to answer the assistant's questions with
one click, so that I do not have to type an answer it already proposed.

Acceptance criteria:
- The question is shown under the reply as a card with one button per option.
- A click sends the option as my next message and the agent continues from it.
- I can still type another answer in the message field instead.
- The buttons are disabled once I have answered or while the agent replies.

## Automated eval and hallucination detection (EV1)

As a developer changing a prompt, I want each reply scored by a judge model, so
that I know whether a new version is better without reading every reply.

Acceptance criteria:
- `wu-compare` sends every reply with its question to the `evaluator` agent of
  `configs/agents/automated_eval.yaml`, set by `judge` and `judge_agent`.
- The judge answers in JSON with relevance, coherence, faithfulness and overall
  scores from 0 to 1.
- `docs/PROMPT_COMPARISON.md` shows the mean of each score per version and the
  overall score of each reply.
- Claims the judge cannot verify or finds contradicted are listed with their
  version and question under "Flagged claims".
- A judge model that does not exist stops the program with exit code 84 and a
  judge answer without flagged claims counts as none.

## HTTP API

As a developer, I want to use SensAI through an HTTP API, so that I can build
other interfaces on the same agent.

Acceptance criteria:
- `POST /api/conversations/` returns a conversation id.
- `POST /api/conversations/{id}/messages` streams one JSON event per line:
  `thinking` and `content` chunks, a `question` with its `options` when the
  agent asks one, then `done`, then `spec` (or `error`).
- `GET /api/conversations/{id}/messages`, `GET /api/spec` and `GET /api/profiles`
  return the history, the specification and the profiles.
- An unknown conversation returns 404 and an unknown profile returns 400.
