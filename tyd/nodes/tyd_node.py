from __future__ import annotations

from abc import ABCMeta
from typing import Optional


class TydNode(metaclass=ABCMeta):
    def __init__(
        self,
        name: Optional[str] = None,
        parent: Optional[TydNode] = None,
        docline: int = -1,
    ):
        self._name = name
        self._parent = parent

        self.docline = docline
        self.docindexend = -1

    @property
    def parent(self) -> Optional[TydNode]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional[TydNode]) -> None:
        self._parent = value

    @property
    def name(self) -> Optional[str]:
        return self._name
