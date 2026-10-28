# Sandbox tool for AI agents

This tool gives SensAI a way to run shell commands in an isolated
Docker container. The AI can call `Sandbox.run_command()` as a tool and inspect
the returned output. Commands run in `/work`, a persistent Docker volume that
is separate from the project directory on the host.

## Requirements

- Docker must be installed and running. The Python process must be allowed to
  access the Docker daemon.
- The Docker Python SDK comes with the project dependencies (`pip install -e .` at the root).

## Use from the project

Import `Sandbox` into the AI tool or agent code. A sandbox can execute multiple
commands against the same `/work` directory:

```python
from tools.sandbox.sandbox import Sandbox


def main():
    sbx = Sandbox()
    answer = sbx.run_command("mkdir test;ls")
    print(answer)
    sbx.sleep()
    answer = sbx.run_command("mkdir test1")
    print(answer)
    sbx.sleep()
    answer = sbx.run_command("ls")
    print(answer)
    sbx.destroy()
```

Run this example with `src` on Python's import path. `run_command()` returns a dictionary with
`stdout`, `stderr`, `exit_code`, and `timed_out` fields, which an AI agent can
use to interpret the result and decide what to do next.

In this example, `sleep()` removes the current container but keeps the
session's volume. The next `run_command()` creates a fresh container and
reuses that volume, so the final `ls` still sees `test` and `test1`.
`destroy()` removes both the container and its volume, including files stored
in `/work`. Call `destroy()` when the session is no longer needed; in
production code, use `try/finally` so cleanup also happens if a command fails.

## Session lifetime

Each container stops automatically one hour after it is created. Calling
`sleep()` and then running another command creates a new container with a new
one-hour lifetime; the session's `/work` volume is preserved in between.
Commands have a 20-second timeout by default.

If a container reaches its one-hour limit without being removed with `sleep()`,
the stopped container cannot be restarted by the module. Call `destroy()` to
remove the stopped container and its volume, then create a new `Sandbox`.
Containers created by older versions of this module are not reused with the
current isolation settings.

## Isolation limits

The container has no network access, drops all Linux capabilities, runs
commands as the unprivileged `nobody` user, and has a read-only root filesystem.
Only `/work`, `/tmp`, and `/var/tmp` are writable; the temporary directories
have size limits. The container is limited to 512 MiB of memory, one CPU core,
and 128 processes.
