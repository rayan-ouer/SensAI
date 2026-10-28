##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## report
##

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    version: str
    message: str
    reply: str
    latency: float
    prompt_tokens: int
    reply_tokens: int
    relevance: float
    coherence: float
    faithfulness: float
    overall: float
    flagged: list[str]


def one_line(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def mean(results: list[Result], name: str) -> float:
    return sum(getattr(r, name) for r in results) / len(results)


def summary_row(version: str, results: list[Result]) -> str:
    rows = [r for r in results if r.version == version]
    latency = sum(r.latency for r in rows) / len(rows)
    prompt_tokens = sum(r.prompt_tokens for r in rows)
    reply_tokens = sum(r.reply_tokens for r in rows)
    scores = " | ".join(f"{mean(rows, name):.2f}" for name in ("relevance", "coherence", "faithfulness"))
    flagged = sum(len(r.flagged) for r in rows)
    return f"| {version} | {latency:.1f} s | {prompt_tokens} | {reply_tokens} | {scores} | {flagged} |"


def summary(versions: list[str], results: list[Result]) -> list[str]:
    header = ["| Version | Mean latency | Prompt tokens | Reply tokens | Relevance | Coherence | Faithfulness | Flagged claims |", "|---|---|---|---|---|---|---|---|"]
    return header + [summary_row(version, results) for version in versions]


def message_section(message: str, results: list[Result]) -> list[str]:
    lines = [f"### {message}", "", "| Version | Latency | Tokens | Score | Flagged | Reply |", "|---|---|---|---|---|---|"]
    for r in results:
        if r.message == message:
            lines.append(f"| {r.version} | {r.latency:.1f} s | {r.reply_tokens} | {r.overall:.2f} | {len(r.flagged)} | {one_line(r.reply)} |")
    return lines + [""]


def flagged_section(results: list[Result]) -> list[str]:
    lines = ["## Flagged claims", ""]
    return lines + [f"- {r.version}, {r.message}: {claim}" for r in results for claim in r.flagged]


def render_report(model: str, profile: str, versions: list[str], results: list[Result]) -> str:
    lines = ["# Prompt comparison", "", f"Model `{model}`, profile `{profile}`.", "", "## Summary", ""]
    lines += summary(versions, results) + ["", "## Replies", ""]
    for message in dict.fromkeys(r.message for r in results):
        lines += message_section(message, results)
    lines += flagged_section(results)
    return "\n".join(lines)
