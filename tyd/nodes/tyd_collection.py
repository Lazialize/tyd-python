from abc import ABCMeta
from typing import List, Optional

from .tyd_node import TydNode


class TydCollection(TydNode, metaclass=ABCMeta):
    def __init__(
        self, name: Optional[str], parent: Optional[TydNode], docline: int = -1
    ):
        super().__init__(name, parent, docline)
        self._nodes = list()
        self._att_handle = None
        self._att_source = None
        self._att_abstract = False
        self._att_no_inherit = False
        self._i = 0

    @property
    def nodes(self) -> List[TydNode]:
        return self._nodes

    @property
    def attribute_handle(self) -> str:
        return self._att_handle

    @attribute_handle.setter
    def attribute_handle(self, value: str) -> None:
        if not type(value) is str:
            raise TypeError("A handle attribute must be string.")
        self._att_handle = value

    @property
    def attribute_source(self) -> str:
        return self._att_source

    @attribute_source.setter
    def attribute_source(self, value: str) -> None:
        if not type(value) is str:
            raise TypeError("A source attribute must be string.")
        self._att_source = value

    @property
    def attribute_abstract(self) -> bool:
        return self._att_abstract

    @attribute_abstract.setter
    def attribute_abstract(self, value: bool) -> None:
        if not type(value) is bool:
            raise TypeError("A abstract attribute must be bool.")
        self._att_abstract = value

    @property
    def attribute_no_inherit(self) -> bool:
        return self._att_no_inherit

    @attribute_no_inherit.setter
    def attribute_no_inherit(self, value: bool) -> None:
        if type(value) is bool:
            raise TypeError("A noinherit attribute must be bool.")
        self._att_no_inherit = value

    def setup_attributes(
        self,
        handle: Optional[str],
        source: Optional[str],
        abstract: bool,
        no_inherit: bool,
    ):
        """A function to set attributes of the collection.

        Parameters
        ----------
        handle : Optional[str]
            A string representing the handle name used to inheriting from other collection.
        source : Optional[str]
            A string representing the handle name of the collection inheriting.
        abstract : bool
            Whether the collection is abstract.
        no_inherit : bool
            Whether to ignore parent's inheritance.
        """
        self.attribute_handle = handle
        self.attribute_source = source
        self.attribute_abstract = abstract
        self.attribute_no_inherit = no_inherit

    def add(self, node: TydNode):
        """A function to add a node to the collection.

        Parameters
        ----------
        node : TydNode
            A node to add.

        Raises
        ------
        TypeError
            Raise when other than TydNode passed.
        """
        if not isinstance(node, TydNode):
            raise TypeError(
                "Only subclass of the TydNode can be added to the collection."
            )
        self._nodes.append(node)
        node.parent = self

    def insert(self, index: int, node: TydNode):
        """A function to insert a node at the specified index of the collection.

        If the index parameter is bigger than the collection length, the node is added to last.

        Parameters
        ----------
        index : int
            A index of the collection that want to add
        node : TydNode
            A node to add.

        Raises
        ------
        TypeError
            Raise when other than TydNode passed.
        """
        if not isinstance(node, TydNode):
            raise TypeError(
                "Only subclass of the TydNode can be added to the collection."
            )
        self._nodes.insert(index, node)
        node.parent = self

    def __iter__(self):
        return self._nodes.__iter__()

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, key: int) -> TydNode:
        return self._nodes[key]
