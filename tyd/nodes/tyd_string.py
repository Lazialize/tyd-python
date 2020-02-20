from __future__ import annotations
from typing import Optional

from .tyd_node import TydNode


class TydString(TydNode):
    def __init__(
        self,
        name: Optional[str],
        value: Optional[str],
        parent: Optional[TydNode],
        docline: int = -1,
    ):
        super().__init__(name, parent, docline)

        self._value = value

    @property
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: Optional[str]):
        self._value = str(value)

    def __str__(self) -> str:
        value = "null" if self.value is None else f'"{self.value}"'
        return f"{self.name}={value}"

    def __eq__(self, value: TydString) -> bool:
        return super().__eq__(value) and self.value == value.value
