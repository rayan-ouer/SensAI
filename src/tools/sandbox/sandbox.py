import json
import re
import uuid

import docker
from docker.types import Mount
from fastmcp import FastMCP

from core.tools import ITool, ToolDependencies, ToolHandler
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

client = docker.from_env()
IMAGE = "python:3.12-slim"
MAX_OUTPUT = 10000
MAX_LIFETIME = 60 * 60
SANDBOX_VERSION = "2"
SESSION_ID_PATTERN = re.compile(r"[a-f0-9]{12}")


class Sandbox:
    def __init__(self, session_id: str | None = None):
        if session_id is None:
            self.session_id = str(uuid.uuid4())
        else:
            self.session_id = session_id
        self.name = f"sbox-{self.session_id}"
        self.volume = f"sbx-vol-{self.session_id}"

    def _container(self):
        try:
            c = client.containers.get(self.name)
            c.reload()
            if c.labels.get("sensai.sandbox.version") != SANDBOX_VERSION:
                raise RuntimeError(
                    f"La session {self.session_id} a été créée avec une ancienne configuration. "
                    "Utilisez un nouvel identifiant de session."
                )
            if c.status != "running":
                raise RuntimeError(
                    f"La session {self.session_id} est expirée ou arrêtée. "
                    "Relancez sans identifiant pour créer une nouvelle session."
                )
            return c
        except docker.errors.NotFound:
            pass

        client.containers.run(
            IMAGE,
            ["chmod", "777", "/work"],
            remove=True,
            network_mode="none",
            mounts=[Mount(target="/work", source=self.volume, no_copy=True)],
            working_dir="/work",
            read_only=True,
            cap_drop=["ALL"],
        )
        c = client.containers.run(
            IMAGE,
            ["sleep", str(MAX_LIFETIME)],
            name=self.name,
            detach=True,
            mounts=[Mount(target="/work", source=self.volume, no_copy=True)],
            working_dir="/work",
            network_mode="none",
            mem_limit="512m",
            memswap_limit="512m",
            nano_cpus=1_000_000_000,
            pids_limit=128,
            user="nobody",
            cap_drop=["ALL"],
            labels={"sensai.sandbox.version": SANDBOX_VERSION},
            read_only=True,
            tmpfs={
                "/tmp": "rw,nosuid,nodev,size=64m,mode=1777",
                "/var/tmp": "rw,nosuid,nodev,size=16m,mode=1777",
            },
        )
        c.reload()
        if c.status != "running":
            state = c.attrs["State"]
            raise RuntimeError(
                f"Conteneur arrêté : status={c.status} exit={state['ExitCode']} "
                f"error={state['Error']!r} logs={c.logs().decode(errors='replace')!r}"
            )
        return c

    def _exec(self, argv: list[str], timeout: int) -> dict:
        r = self._container().exec_run(
            ["timeout", "-s", "KILL", str(timeout), *argv],
            demux=True,
            workdir="/work",
            user="nobody",
            environment={"HOME": "/work"},
        )
        out, err = r.output
        return {
            "stdout": (out or b"").decode(errors="replace")[:MAX_OUTPUT],
            "stderr": (err or b"").decode(errors="replace")[:MAX_OUTPUT],
            "exit_code": r.exit_code,
            "timed_out": r.exit_code == 137,
        }

    def run_command(self, command: str, timeout: int = 20) -> dict:
        return self._exec(["bash", "-c", command], timeout)

    def sleep(self):
        try:
            client.containers.get(self.name).remove(force=True)
        except docker.errors.NotFound:
            pass

    def destroy(self):
        self.sleep()
        try:
            client.volumes.get(self.volume).remove()
        except docker.errors.NotFound:
            pass


def create_sandbox_server(session_id: str | None = None) -> FastMCP:
    mcp = FastMCP("sensai-sandbox")
    sandbox = Sandbox(session_id)

    @mcp.tool
    def execute_command(command: str) -> str:
        """Execute a command in a sandbox"""
        return json.dumps(sandbox.run_command(command))

    return mcp


def create_sandbox_tools(dependencies: ToolDependencies) -> list[ITool]:
    server = create_sandbox_server(dependencies.conversation_id)
    return MCPAdapter(MCPClient(server)).list_tools()


def register_sandbox_tools(manager: ToolHandler, context: ToolDependencies):
    manager.register_many(create_sandbox_tools(context))
