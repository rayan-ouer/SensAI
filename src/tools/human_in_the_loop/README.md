# Human-in-the-loop tool

`human_in_the_loop` lets the agent ask the user a closed question when an
important project specification detail is missing. The tool displays the
proposed options as a numbered list and always adds an **Other free-form
answer** option.

## MCP tool

The tool is exposed through the project's FastMCP client and adapter:

```json
{
  "question": "Which platform should the app target?",
  "options": ["Web", "Mobile", "Desktop"]
}
```

The terminal displays the question and options. The user selects an option by
number, or selects **Other** and types a non-empty answer. The selected answer
is returned to the agent.

Questions must be non-empty. Provide at least two distinct, non-empty options;
the free-form option is added automatically.

## Registration

`register_human_in_the_loop_tools(manager, answers)` creates the local MCP
server, adapts its tools, and registers them with the `ToolHandler`. The
`answers` list receives each question and its answer. The CLI passes those
answers to the specification updater for the current turn.

The system prompt instructs the agent to use this tool for important missing
project details, ask one concise question at a time, and avoid guessing the
user's answer or asking unnecessary questions.
