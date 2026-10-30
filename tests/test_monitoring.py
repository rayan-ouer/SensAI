import json
import tempfile
import unittest
from pathlib import Path

from core.messages import AIMessage, HumanMessage
from monitoring.store import InteractionMonitor, MonitoredLLMClient, MonitoringStore


class StubLLM:
    def chat(self, model, messages, tools, response_format, **kwargs):
        return AIMessage(content="answer", prompt_eval_count=3, eval_count=2)

    def embed(self, embed_model, text):
        return []


class MonitoringTests(unittest.TestCase):
    def test_records_interaction_and_llm_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MonitoringStore(str(Path(directory) / "monitor.sqlite3"))
            monitor = InteractionMonitor(store)
            llm = MonitoredLLMClient(StubLLM(), monitor)

            with monitor.bind("conversation-1", "Wu", "model-1"):
                reply = llm.chat(
                    "model-1", [HumanMessage(content="question")], [], None
                )
                store.record_event(
                    "interaction", conversation_id="conversation-1", model="model-1",
                    profile="Wu", prompt="question", response=reply.content,
                    latency_ms=125, prompt_tokens=3, completion_tokens=2,
                )

            summary = store.get_summary()
            self.assertEqual(summary["metrics"]["interaction_count"], 1)
            self.assertEqual(summary["metrics"]["prompt_tokens"], 3)
            self.assertEqual(summary["metrics"]["completion_tokens"], 2)
            self.assertEqual(summary["series"][-1]["call_volume"], 1)
            llm_event = next(event for event in summary["events"] if event["event_type"] == "llm_call")
            self.assertEqual(
                json.loads(llm_event["prompt"])["messages"][0]["content"], "question"
            )
            self.assertEqual(llm_event["response"], "answer")
            self.assertEqual(llm_event["conversation_id"], "conversation-1")


if __name__ == "__main__":
    unittest.main()
