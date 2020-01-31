from __future__ import annotations
from typing import Union

from .tyd_table import TydTable
from .tyd_list import TydList


class TydDocument(TydTable):
    def __init__(self, nodes: Union[TydDocument, TydList, TydTable] = None):
        super().__init__(None, None)
        if nodes is None:
            return

        for node in nodes:
            self.add(node)
