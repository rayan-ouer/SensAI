##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import json
import os
import sys
import time
from dataclasses import dataclass, replace

from agent.definition import AgentDefinition
from agent.load import AgentsLoader
from core.messages import HumanMessage, SystemMessage
from interfaces.compare.report import Result, render_report
from llm.errors import LLMError
from llm.ollama.ollama import OllamaClient
from tools.agent.profiles import build_profile_prompt, init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.errors import AppError
from tools.chat.load_config import ConfigLoader, read_prompt, read_yaml
from tools.chat.settings import Settings
from tools.spec.spec import build_system_prompt

COMPARISON_PATH = "configs/prompt_comparison.yaml"


@dataclass(frozen=True)
class Judge:
    client: OllamaClient
    agent: AgentDefinition
    message: str


def version_role(config: ConfigData, raw: dict, version: str, profile: str) -> SystemMessage:
    folder = os.path.join(config.config_dir, config.prompt_version_dir, version)
    system = read_prompt(folder, raw["system_prompt"])
    profile_prompt = build_profile_prompt(init_profiles(config)[profile])
    return SystemMessage(content=build_system_prompt(system, profile_prompt, ""))


def ask(client: OllamaClient, config: ConfigData, role: SystemMessage, message: str) -> tuple:
    start = time.perf_counter()
    reply = client.chat(config.model, [role, HumanMessage(content=message)], [], None, think=config.think)
    return reply, time.perf_counter() - start


def compare_version(
    client: OllamaClient,
    config: ConfigData,
    raw: dict,
    comparison: dict,
    version: str,
    judge: Judge
) -> list[Result]:
    role = version_role(config, raw, version, comparison["profile"])
    results = []
    for message in comparison["messages"]:
        results.append(measure(client, config, role, judge, version, message))
        print(f"{version} | {results[-1].latency:.1f} s | {results[-1].overall:.2f} | {message}")
    return results


def create_client(config: ConfigData, model: str) -> OllamaClient:
    key = Settings().ollama_api_key
    api_key = key.get_secret_value() if key else None
    return OllamaClient(model, api_key, options=config.llm_settings, provider=config.ollama_provider)


def score(judge: Judge, question: str, reply: str) -> dict:
    text = judge.message.format(question=question, reply=reply)
    answer = judge.client.chat(
        model=judge.agent.model,
        messages=[SystemMessage(content=judge.agent.role), HumanMessage(content=text)],
        tools=[],
        response_format=judge.agent.response_format,
        think=False
    )
    return json.loads(answer.content)


def load_judge(comparison: dict, config: ConfigData) -> Judge:
    path = os.path.join(os.path.dirname(COMPARISON_PATH), comparison["judge"])
    agent = AgentsLoader.load(path).by_name()[comparison["judge_agent"]]
    agent = replace(agent, model=comparison.get("judge_model", agent.model))
    return Judge(create_client(config, agent.model), agent, comparison["judge_message"])


def measure(
    client: OllamaClient,
    config: ConfigData,
    role: SystemMessage,
    judge: Judge,
    version: str,
    message: str
) -> Result:
    reply, latency = ask(client, config, role, message)
    scores = score(judge, message, reply.content)
    flagged = [f"{c['claim']} ({c['issue']})" for c in scores.get("flagged_claims", [])]
    return Result(
        version, message, reply.content, latency, reply.prompt_eval_count or 0, reply.eval_count or 0,
        scores["relevance"], scores["coherence"], scores["faithfulness"], scores["overall"], flagged
    )


def run(comparison: dict) -> str:
    config_path = os.path.join(os.path.dirname(COMPARISON_PATH), comparison["config"])
    config = ConfigLoader(config_path).get_configs()
    client = create_client(config, config.model)
    judge = load_judge(comparison, config)
    results = []
    for version in comparison["versions"]:
        results += compare_version(client, config, read_yaml(config_path), comparison, version, judge)
    return render_report(config.model, comparison["profile"], comparison["versions"], results)


def main() -> None:
    try:
        comparison = read_yaml(COMPARISON_PATH)
        report = run(comparison)
    except (AppError, LLMError, KeyError, json.JSONDecodeError) as e:
        print(f"wu-compare: {e}", file=sys.stderr)
        sys.exit(84)
    with open(comparison["report_path"], "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print(f"Report written to {comparison['report_path']}")
