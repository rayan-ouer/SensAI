import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from fastmcp import FastMCP

from core.tools import ITool, ToolHandler
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

_SEARCH_URL = "https://lite.duckduckgo.com/lite/"
_USER_AGENT = "Mozilla/5.0 (compatible; SensAI/1.0)"
_TIMEOUT_SECONDS = 20
_MAX_RESULTS = 10


class _LiteResultParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._capture: str = ""
        self._href = ""
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        classes = attributes.get("class", "").split()

        if tag == "a" and "result-link" in classes:
            self._capture = "link"
            self._href = attributes.get("href", "")
            self._chunks = []
        elif tag == "td" and "result-snippet" in classes:
            self._capture = "snippet"
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture == "link":
            title = " ".join("".join(self._chunks).split())
            if title and self._href.startswith("http"):
                self.results.append({"title": title, "url": self._href, "snippet": ""})
            self._capture = ""
        elif tag == "td" and self._capture == "snippet":
            snippet = " ".join("".join(self._chunks).split())
            for result in reversed(self.results):
                if not result["snippet"]:
                    result["snippet"] = snippet
                    break
            self._capture = ""


def _fetch_page(query: str) -> str:
    body = urllib.parse.urlencode({"q": query}).encode()
    request = urllib.request.Request(
        _SEARCH_URL,
        data=body,
        headers={
            "User-Agent": _USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=_TIMEOUT_SECONDS) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as error:
        reason = getattr(error, "reason", error)
        raise RuntimeError(f"Web search failed: {reason}") from error


def _format_results(results: list[dict[str, str]]) -> str:
    blocks = []
    for index, result in enumerate(results, start=1):
        lines = [f"{index}. {result['title']}", result["url"]]
        if result["snippet"]:
            lines.append(result["snippet"])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def run_web_search(query: str, max_results: int = 5) -> str:
    text = (query or "").strip()

    if not text:
        raise ValueError("query is required")
    try:
        limit = int(max_results)
    except (TypeError, ValueError) as error:
        raise ValueError("max_results must be an integer") from error
    limit = max(1, min(limit, _MAX_RESULTS))
    parser: _LiteResultParser = _LiteResultParser()
    parser.feed(_fetch_page(text))
    results = parser.results[:limit]
    if not results:
        return "No results found."
    return _format_results(results)


def create_search_server() -> FastMCP:
    mcp = FastMCP("sensai-search")

    @mcp.tool
    def search_web(query: str, max_results: int = 5) -> str:
        """Search the public web and return titles, URLs and short snippets.

        query: Words or a question to search for.
        max_results: Number of results to return, from 1 to 10.
        """
        return run_web_search(query, max_results)

    return mcp


def create_search_tools() -> list[ITool]:
    return MCPAdapter(MCPClient(create_search_server())).list_tools()


def register_search_tools(manager: ToolHandler) -> None:
    manager.register_many(create_search_tools())
