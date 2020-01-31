from typing import Optional

from .tyd_collection import TydCollection
from .tyd_node import TydNode


class TydTable(TydCollection):
    def __getitem__(self, key: str) -> Optional[TydNode]:
        for node in self:
            if node.name == key:
                return node
        return None

    def __str__(self):
        return f'<TydTable name="{self.name}" parent=<{self.parent.name if self.parent else "NullName"}>>'
