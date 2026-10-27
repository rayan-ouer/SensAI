from collections.abc import Callable


def visit(
    graph: dict[str, list[str]],
    visited: set[str],
    in_path: set[str],
    path: list[str],
    order: list[str],
    node: str,
    on_back_edge: Callable[[list[str]], None],
) -> None:
    visited.add(node)
    in_path.add(node)
    path.append(node)

    for neighbor in graph[node]:
        if neighbor in in_path:
            start = path.index(neighbor)
            on_back_edge(path[start:] + [neighbor])
        elif neighbor not in visited:
            visit(graph, visited, in_path, path, order, neighbor, on_back_edge)
    path.pop()
    in_path.remove(node)
    order.append(node)

def dfs(
    graph: dict[str, list[str]],
    on_back_edge: Callable[[list[str]], None],
) -> list[str]:
    visited: set[str] = set()
    in_path: set[str] = set()
    path: list[str] = []
    order: list[str] = []

    for node in graph:
        if node not in visited:
            visit(graph, visited, in_path, path, order, node, on_back_edge)
    return order
