##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## display
##


class ChunkDisplay:
    def __init__(self) -> None:
        self._last_kind = None

    def __call__(self, kind: str, text: str) -> None:
        if kind not in ("thinking", "content"):
            return
        if kind != self._last_kind:
            if kind == "thinking":
                print("Thinking:")
            else:
                if self._last_kind == "thinking":
                    print("\n")
                print("Answer:")
            self._last_kind = kind
        print(text, end="", flush=True)

    def reset(self) -> None:
        self._last_kind = None
