import re
import uuid

import docker
from docker.types import Mount

client = docker.from_env()
IMAGE = "python:3.12-slim"
MAX_OUTPUT = 10000
MAX_LIFETIME = 60 * 60
SANDBOX_VERSION = "2"
SESSION_ID_PATTERN = re.compile(r"[a-f0-9]{12}")


class Sandbox:
    def __init__(self, session_id: str | None = None):
        if session_id is None:
            self.session_id = uuid.uuid4().hex[:12]
        else:
            self.session_id = session_id
        if not self._is_session_ide_valid():
            raise ValueError(
                "L'identifiant de session doit contenir 12 caractères hexadécimaux."
            )
        self.name = f"sbox-{self.session_id}"
        self.volume = f"sbx-vol-{self.session_id}"

    def _is_session_ide_valid(self) -> bool:
        if SESSION_ID_PATTERN.fullmatch(self.session_id):
            return True
        return False

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
