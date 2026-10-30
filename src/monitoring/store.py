from __future__ import annotations

import json
import sqlite3
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

from core.messages import AIMessage, IMessage
from core.tools import ITool, ToolCall, ToolExecution
from llm.client import ILLMClient


class InteractionMonitor:
    def __init__(self, store: MonitoringStore) -> None:
        self.store = store
        self._context = threading.local()

    @contextmanager
    def bind(self, conversation_id: str, profile: str, model: str) -> Iterator[None]:
        previous = getattr(self._context, "interaction", None)
        self._context.interaction = {
            "conversation_id": conversation_id,
            "profile": profile,
            "model": model,
        }
        try:
            yield
        finally:
            self._context.interaction = previous

    def record(self, event_type: str, **fields: Any) -> None:
        event = dict(getattr(self._context, "interaction", {}))
        event.update(fields)
        self.store.record_event(event_type, **event)

    def record_tool(self, call: ToolCall, execution: ToolExecution, latency_ms: float) -> None:
        self.record(
            "tool_call",
            tool_name=call.name,
            tool_arguments=call.arguments,
            tool_result=execution.result,
            latency_ms=latency_ms,
            success=execution.status.value == "success",
            error=None if execution.status.value == "success" else str(execution.result),
        )


class MonitoredLLMClient(ILLMClient):
    def __init__(self, client: ILLMClient, monitor: InteractionMonitor) -> None:
        self.client = client
        self.monitor = monitor

    def chat(
        self,
        model: str,
        messages: list[IMessage],
        tools: list[ITool],
        response_format: dict | None,
        *,
        think: bool | None = None,
        include_thinking: bool = False,
        extract_thinking_tags: bool = False,
        on_chunk: Callable[[str, str], None] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
    ) -> AIMessage:
        started = time.perf_counter()
        prompt = json.dumps(
            {
                "messages": [
                    {"role": message.role.value, "content": message.content}
                    for message in messages
                ],
                "tools": [
                    {"name": tool.name, "description": tool.description, "parameters": tool.args}
                    for tool in tools
                ],
                "response_format": response_format,
            },
            ensure_ascii=False, default=str,
        )
        try:
            response = self.client.chat(
                model, messages, tools, response_format, think=think,
                include_thinking=include_thinking,
                extract_thinking_tags=extract_thinking_tags,
                on_chunk=on_chunk, is_cancelled=is_cancelled,
            )
        except Exception as error:
            self.monitor.record(
                "llm_call", model=model, prompt=prompt,
                latency_ms=(time.perf_counter() - started) * 1000,
                success=False, error=str(error),
            )
            raise

        self.monitor.record(
            "llm_call", model=model, prompt=prompt, response=response.content,
            latency_ms=(time.perf_counter() - started) * 1000,
            prompt_tokens=response.prompt_eval_count,
            completion_tokens=response.eval_count,
            success=True,
        )
        return response

    def embed(self, embed_model: str | None, text: str) -> list[float]:
        return self.client.embed(embed_model, text)


class MonitoringStore:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    occurred_at TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    conversation_id TEXT,
                    model TEXT,
                    profile TEXT,
                    prompt TEXT,
                    response TEXT,
                    tool_name TEXT,
                    tool_arguments TEXT,
                    tool_result TEXT,
                    latency_ms REAL,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    success INTEGER NOT NULL,
                    error TEXT
                )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS events_occurred_at ON events(occurred_at)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS events_type ON events(event_type)"
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def _json(value: Any) -> str | None:
        return json.dumps(value, ensure_ascii=False, default=str) if value is not None else None

    def record_event(
        self,
        event_type: str,
        *,
        conversation_id: str | None = None,
        model: str | None = None,
        profile: str | None = None,
        prompt: str | None = None,
        response: str | None = None,
        tool_name: str | None = None,
        tool_arguments: Any = None,
        tool_result: Any = None,
        latency_ms: float | None = None,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        success: bool = True,
        error: str | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(uuid4()), datetime.now(UTC).isoformat(), event_type,
                    conversation_id, model, profile, prompt, response, tool_name,
                    self._json(tool_arguments), self._json(tool_result), latency_ms,
                    prompt_tokens, completion_tokens, int(success), error,
                ),
            )

    def get_summary(self) -> dict[str, Any]:
        today = datetime.now(UTC).date()
        first_day = today - timedelta(days=13)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM events WHERE event_type = 'interaction' ORDER BY occurred_at"
            ).fetchall()
            llm_rows = connection.execute(
                "SELECT * FROM events WHERE event_type = 'llm_call' ORDER BY occurred_at"
            ).fetchall()
            event_rows = connection.execute(
                "SELECT * FROM events ORDER BY occurred_at DESC LIMIT 100"
            ).fetchall()

        rows = [
            row for row in rows
            if datetime.fromisoformat(row["occurred_at"]).date() >= first_day
        ]
        llm_rows = [
            row for row in llm_rows
            if datetime.fromisoformat(row["occurred_at"]).date() >= first_day
        ]
        daily: dict[date, list[sqlite3.Row]] = {
            first_day + timedelta(days=offset): [] for offset in range(14)
        }
        for row in rows:
            event_day = datetime.fromisoformat(row["occurred_at"]).date()
            if event_day in daily:
                daily[event_day].append(row)

        interactions = len(rows)
        errors = sum(not row["success"] for row in rows)
        latencies = [row["latency_ms"] for row in rows if row["latency_ms"] is not None]
        baseline_rows = [
            row for row in rows
            if first_day <= datetime.fromisoformat(row["occurred_at"]).date() < today - timedelta(days=6)
        ]
        recent_rows = [row for row in rows if datetime.fromisoformat(row["occurred_at"]).date() >= today - timedelta(days=6)]
        baseline = self._average_response_tokens(baseline_rows)
        recent = self._average_response_tokens(recent_rows)

        return {
            "metrics": {
                "interaction_count": interactions,
                "average_latency_ms": self._average(latencies),
                "error_rate": errors / interactions if interactions else 0,
                "prompt_tokens": sum(row["prompt_tokens"] or 0 for row in llm_rows),
                "completion_tokens": sum(row["completion_tokens"] or 0 for row in llm_rows),
                "response_size_drift_percent": (
                    ((recent - baseline) / baseline * 100) if baseline else None
                ),
                "drift_baseline_response_tokens": baseline,
                "drift_recent_response_tokens": recent,
            },
            "series": [
                {
                    "date": day.isoformat(),
                    "call_volume": len(day_rows),
                    "average_latency_ms": self._average(
                        [row["latency_ms"] for row in day_rows if row["latency_ms"] is not None]
                    ),
                    "error_rate": (
                        sum(not row["success"] for row in day_rows) / len(day_rows)
                        if day_rows else 0
                    ),
                    "average_response_tokens": self._average_response_tokens(day_rows),
                }
                for day, day_rows in daily.items()
            ],
            "events": [self._serialize(row) for row in event_rows],
        }

    @staticmethod
    def _average(values: list[float | int]) -> float | None:
        return round(sum(values) / len(values), 2) if values else None

    @classmethod
    def _average_response_tokens(cls, rows: list[sqlite3.Row]) -> float | None:
        values = [row["completion_tokens"] for row in rows if row["completion_tokens"] is not None]
        return cls._average(values)

    @staticmethod
    def _serialize(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        result["success"] = bool(result["success"])
        for field in ("tool_arguments", "tool_result"):
            result[field] = json.loads(result[field]) if result[field] else None
        return result
