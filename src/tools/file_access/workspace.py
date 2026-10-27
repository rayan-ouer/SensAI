##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## workspace
##

from pathlib import Path
from typing import Any, Callable

import yaml

from tools.chat.errors import ConfigError

_VALID_PERMISSIONS = {"read", "read_write"}
_YES = {"y", "yes"}
_NO = {"n", "no"}


class WorkspaceSession:
    def __init__(
        self,
        root: Path,
        permissions_path: Path,
        input_function: Callable[[str], str] = input,
    ):
        self.root = root.resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError(f"Workspace is not a directory: {self.root}")
        self._input = input_function
        self.permissions_path = permissions_path
        self.permissions = self._load_permissions(permissions_path)
        self._require_permission(self.root)
        self.initial_listing: str = self._read_listing(self.root)
        self.confirmed = False

    @staticmethod
    def _load_permissions(path: Path) -> dict[str, str]:
        try:
            with path.open(encoding="utf-8") as config_file:
                config: Any = yaml.safe_load(config_file)
        except OSError as error:
            raise ConfigError("cannot read file access permissions", path) from error
        except yaml.YAMLError as error:
            raise ConfigError("invalid file access permissions", path) from error

        permissions = config.get("permissions") if isinstance(config, dict) else None
        if not isinstance(permissions, dict) or not permissions:
            raise ConfigError("permissions must be a non-empty mapping", path)
        for location, permission in permissions.items():
            if (
                not isinstance(location, str)
                or not isinstance(permission, str)
                or permission not in _VALID_PERMISSIONS
            ):
                raise ConfigError(
                    "permission entries must map paths to read or read_write", path
                )
        return permissions

    def initial_context(self) -> str:
        return (
            f"Working directory: {self.root}\n"
            f"Initial directory listing:\n{self.initial_listing}"
        )

    @staticmethod
    def _read_listing(directory: Path) -> str:
        entries = sorted(directory.iterdir(), key=lambda item: item.name.lower())
        lines = []
        for entry in entries[:200]:
            kind = "dir" if entry.is_dir() else "file"
            lines.append(f"{kind}\t{entry.name}")
        if len(entries) > 200:
            lines.append(f"... {len(entries) - 200} more entries omitted")
        return "\n".join(lines) if lines else "(empty directory)"

    def _confirm(self) -> None:
        if self.confirmed:
            return

        while True:
            try:
                answer = self._input(
                    f"Detected Workspace: {self.root}. Is it correct ? [Y/n] "
                ).strip().lower()
            except (EOFError, KeyboardInterrupt) as error:
                raise RuntimeError("Workspace confirmation was interrupted") from error
            if answer in _YES or not answer:
                self.confirmed = True
                return
            if answer in _NO:
                break
            print("The answer must be yes or no.")

        try:
            path_text = self._input(
                "Select your workspace path please : "
            ).strip()
        except (EOFError, KeyboardInterrupt) as error:
            raise RuntimeError("Workspace path entry was interrupted") from error
        while path_text:
            candidate = Path(path_text).expanduser()
            if not candidate.is_absolute():
                candidate = self.root / candidate
            try:
                candidate = candidate.resolve(strict=True)
                if candidate.is_dir():
                    previous_root = self.root
                    self.root = candidate
                    try:
                        self._require_permission(self.root)
                        self.initial_listing = self._read_listing(self.root)
                    except OSError as error:
                        self.root = previous_root
                        print(f"Access denied for this folder : {error}")
                    else:
                        self.confirmed = True
                        return
            except OSError:
                pass
            print(f"Invalid path : {path_text}")
            try:
                path_text = self._input(
                    "Select your workspace path please : "
                ).strip()
            except (EOFError, KeyboardInterrupt) as error:
                raise RuntimeError("Workspace path entry was interrupted") from error
        raise ValueError("A valid workspace path was not provided")

    def _resolve_path(self, path: str) -> Path:
        self._confirm()
        candidate = Path(path or ".").expanduser()
        if not candidate.is_absolute():
            candidate = self.root / candidate
        resolved = candidate.resolve()
        if not resolved.is_relative_to(self.root):
            raise PermissionError("Path is outside the confirmed workspace")
        return resolved

    def _permission_for(self, path: Path) -> str | None:
        matching: list[tuple[int, str]] = []
        for location, permission in self.permissions.items():
            rule_path = Path(location).expanduser()
            if not rule_path.is_absolute():
                rule_path = self.root / rule_path
            rule_path = rule_path.resolve()
            if path == rule_path or rule_path in path.parents:
                matching.append((len(rule_path.parts), permission))
        return max(matching, default=(0, None), key=lambda item: item[0])[1]

    def _require_permission(self, path: Path, write: bool = False) -> None:
        permission = self._permission_for(path)
        if permission is None or (write and permission != "read_write"):
            operation = "write" if write else "read"
            raise PermissionError(f"{operation} access is not allowed for {path}")

    def list_directory(self, path: str = ".") -> str:
        directory = self._resolve_path(path)
        self._require_permission(directory)
        if not directory.is_dir():
            raise NotADirectoryError(str(directory))
        return f"{directory}\n{self._read_listing(directory)}"

    def read_file(self, path: str) -> str:
        file_path = self._resolve_path(path)
        self._require_permission(file_path)
        if not file_path.is_file():
            raise IsADirectoryError(str(file_path))
        if file_path.stat().st_size > 1_000_000:
            raise ValueError("File exceeds the 1 MB read limit")
        return file_path.read_text(encoding="utf-8")

    def create_file(self, path: str, content: str) -> str:
        file_path = self._resolve_path(path)
        self._require_permission(file_path, write=True)
        if not file_path.parent.is_dir():
            raise FileNotFoundError(
                f"Parent directory does not exist: {file_path.parent}"
            )
        with file_path.open("x", encoding="utf-8") as created_file:
            created_file.write(content)
        return f"Created {file_path}"

    def _confirm_file_write(self, file_path: Path) -> bool:
        relative_path = file_path.relative_to(self.root)
        while True:
            try:
                answer = self._input(
                    f"Allow the agent to write to {relative_path}? [y/N] "
                ).strip().lower()
            except (EOFError, KeyboardInterrupt) as error:
                raise RuntimeError("File write confirmation was interrupted") from error
            if answer in _YES:
                return True
            if answer in _NO or not answer:
                return False
            print("Please answer yes or no.")

    def write_in_file(self, path: str, content: str) -> str:
        file_path = self._resolve_path(path)
        self._require_permission(file_path)
        if not file_path.parent.is_dir():
            raise FileNotFoundError(
                f"Parent directory does not exist: {file_path.parent}"
            )
        if file_path.is_dir():
            raise IsADirectoryError(str(file_path))
        if not self._confirm_file_write(file_path):
            return f"Write cancelled by user for {file_path.relative_to(self.root)}"
        file_path.write_text(content, encoding="utf-8")
        return f"Wrote {file_path}"
