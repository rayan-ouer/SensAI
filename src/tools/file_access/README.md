# File access tools

The CLI captures its launch directory in a `WorkspaceSession`, includes that
directory and its initial listing in the system context, and keeps the session
state in memory for the conversation. Before the first file tool runs, the CLI
asks the user to confirm the detected directory. If it is not correct, the user
can provide another directory.

The file tools are exposed through the existing FastMCP client and adapter:

- `list(path=".")` lists the workspace root (or a directory beneath it).
- `read_file(path)` reads a file.
- `create_file(path, content)` creates a new file and never overwrites one.
- `write_in_file(path, content)` writes the complete content to a file, replacing
  its previous content if it exists. It creates the file if it does not exist.

Access is restricted to the confirmed workspace and the permissions file
referenced by the CLI config (`file_access_config`, relative to the config
directory). Permission paths are relative to the workspace root by default;
the most specific matching path takes precedence.

```yaml
permissions:
  ".": read
  "src": read_write
  "private": read
```

Supported values are `read` and `read_write`. Any path without an applicable
rule is denied. Both `create_file` and `write_in_file` require `read_write`;
`create_file` refuses to replace existing files, while `write_in_file`
intentionally replaces their full contents. The default `configs/file_access.yaml`
grants read access to the launch directory and read/write access to `src`; adjust
it to your project. The agent receives only registered tools and must not run
shell commands or arbitrary functions.
