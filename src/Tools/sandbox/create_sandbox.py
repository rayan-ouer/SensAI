import uuid
import docker

client = docker.from_env()
IMAGE = "python:3.12-slim"
MAX_OUTPUT = 10000

class Sandbox:
    def __init__(self, session_id: str | None = None):
        if session_id is None:
            self.session_id = uuid.uuid4().hex[:12]
        else:
            self.session_id = session_id
        self.name = f"sbox-{self.session_id}"
        self.volume = f"sbx-vol-{self.session_id}"

    def _container(self):
        try:
            c = client.containers.get(self.name)
            if c.status != "running":
                c.start()
            return c
        except docker.errors.NotFound:
            pass

        c = client.containers.run(
            IMAGE, ["sleep", "infinity"],
            name=self.name, detach=True,
            volumes={self.volume: {"bind": "/work", "mode": "rw"}},
            working_dir="/work",
            network_disabled=True,
            mem_limit="512m", memswap_limit="512m",
            nano_cpus=1_000_000_000,
            pids_limit=128,
            # Certains runtimes Docker refusent cap_drop avec no-new-privileges.
            cap_drop=["ALL"],
        )
        c.reload()
        if c.status != "running":
            state = c.attrs["State"]
            raise RuntimeError(
                f"Conteneur arrêté : status={c.status} exit={state['ExitCode']} "
                f"error={state['Error']!r} logs={c.logs().decode(errors='replace')!r}"
            )
        c.exec_run(["chmod", "777", "/work"], user="root")
        return c

    def _exec(self, argv: list[str], timeout: int) -> dict:
        r = self._container().exec_run(
            ["timeout", "-s", "KILL", str(timeout), *argv],
            demux=True, workdir="/work", user="nobody",
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
