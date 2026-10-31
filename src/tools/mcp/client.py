##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## client
##

import atexit
import asyncio
import threading
from pathlib import Path
from typing import Any

from fastmcp import Client, FastMCP


def _result_text(result: Any) -> str:
    data = getattr(result, "data", None)
    if isinstance(data, str):
        return data
    content = getattr(result, "content", None) or []
    parts = [block.text for block in content if getattr(block, "text", None)]
    if parts:
        return "\n".join(parts)
    if data is None:
        return ""
    return str(data)


_clients: list["MCPClient"] = []


def close_mcp_clients() -> None:
    for client in list(_clients):
        client.close()


class MCPClient:
    def __init__(self, server: FastMCP | str | Path | dict[str, Any]):
        self._client = Client(server)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, name="mcp-client", daemon=True
        )
        self._closed = False
        self._thread.start()
        _clients.append(self)
        try:
            self._run(self._client.__aenter__())
        except Exception:
            self.close()
            raise

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
        self._loop.close()

    def _run(self, coro, timeout: float | None = None):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)

    def list_tools(self):
        return self._run(self._client.list_tools())

    def call_tool(self, name, arguments=None):
        result = self._run(self._client.call_tool(name, arguments or {}))
        return _result_text(result)

    async def _shutdown(self) -> None:
        try:
            await self._client.__aexit__(None, None, None)
        except Exception:
            pass
        current = asyncio.current_task()
        pending = [
            task
            for task in asyncio.all_tasks()
            if task is not current and not task.done()
        ]
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self in _clients:
            _clients.remove(self)
        try:
            if self._loop.is_running():
                self._run(self._shutdown(), timeout=5)
        except Exception:
            pass
        finally:
            if self._loop.is_running():
                self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5)


atexit.register(close_mcp_clients)
