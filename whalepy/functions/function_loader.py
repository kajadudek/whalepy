from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FunctionLoader:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).parent / "functions_info"

    def list_functions(self) -> list[str]:
        return sorted(path.stem for path in self.base_path.glob("*.json"))

    def load_metadata(self, name: str) -> dict[str, Any]:
        file_path = self.base_path / f"{name}.json"
        with file_path.open("r", encoding="ascii") as handle:
            return json.load(handle)

    def load_callable(self, name: str):
        # TODO: return real benchmark implementations.
        raise NotImplementedError(
            f"Callable benchmark loading is not implemented for '{name}'."
        )
