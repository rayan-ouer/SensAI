# User stories

## Agent profiles

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

As a teacher, I want to describe a new tutor in a YAML file, so that I can adapt
the assistant to my class without asking a developer.

Acceptance criteria:
- A file added to `configs/profiles/` with `name`, `role`, `tone` and `scope`
  appears in `/profiles` at the next start.
- The profile named by `default_profile` in the configuration file is the one
  active at start and the start message shows its name.
- An optional `prompt` key points to a text file whose instructions are added to
  the tutor's behavior.
- A profile file with a missing key stops the program with exit code 84 and an
  error naming the missing key and the file.

## Living project specification

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
- A greeting or an off-topic question does not add requirements to the file.
- If the update fails or is interrupted, a warning is printed, the previous file
  is kept and the session continues.

## Local and cloud models

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

## Tool-using agent and web search

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

## MCP tool integration

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

## Code sandbox

As a student learning to program, I want the assistant to run commands in an
isolated container, so that a mistake cannot damage my files.

Acceptance criteria:
- A command runs in a Docker container, in `/work`, separate from the project
  directory on the host.
- The result contains `stdout`, `stderr`, `exit_code` and `timed_out`.
- A command running longer than the timeout (20 seconds by default) is stopped
  and reported as timed out.

As a student working on an exercise in several steps, I want files created in
one command to be there for the next, so that the assistant can build and then
test my program.

Acceptance criteria:
- A file created by one command is visible to the next command of the same
  session.
- Putting the session to sleep removes the container but keeps the files.
- Destroying the session removes the container and its files.

## Document knowledge base (RAG)

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
