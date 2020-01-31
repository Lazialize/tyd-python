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
    def value(self, value: Optional[str]) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"{self.name if self.name is not None else 'NullName'}=\"{self.value}\""
