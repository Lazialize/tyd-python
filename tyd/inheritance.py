from typing import Dict, List, Set

from .nodes import TydCollection, TydDocument, TydList, TydNode, TydString, TydTable


class Inheritance:
    class InheritanceNode:
        def __init__(self, tyd_node: TydCollection):
            self.tyd_node = tyd_node
            self.resolved = False
            self.heirs = None
            self.source = None

        @property
        def heir_count(self) -> int:
            return len(self.heirs) if self.heirs is not None else 0

        def get_heir(self, index: int):
            return self.heirs[index]

        def add_heir(self, node) -> None:
            if self.heirs is None:
                self.heirs = list()
            self.heirs.append(node)

        def __str__(self) -> str:
            return self.tyd_node.__str__()

    initialized = False
    unresolved_nodes: List[InheritanceNode] = list()
    resolved_nodes: Dict[TydNode, InheritanceNode] = dict()
    nodes_by_handle: Dict[str, InheritanceNode] = dict()

    @classmethod
    def initialize(cls):
        if cls.initialized:
            # TODO: Will add an error message.
            raise Exception()
        cls.initialized = True

    @classmethod
    def register(cls, node: TydCollection):
        if not cls.initialized:
            # TODO: Will add an error message.
            raise Exception()

        node_handle = node.attribute_handle
        node_source = node.attribute_source

        if node_handle is None and node_source is None:
            return

        if node_handle is not None and node_handle in cls.nodes_by_handle.keys():
            # TODO: Will add an error message.
            raise Exception()

        new_node = cls.InheritanceNode(node)
        cls.unresolved_nodes.append(new_node)
        if node_handle is not None:
            cls.nodes_by_handle[node_handle] = new_node

    @classmethod
    def register_all_roots(cls, doc: TydDocument):
        if not cls.initialized:
            raise Exception()

        for tyd_col in doc:
            if tyd_col is not None:
                cls.register(tyd_col)

    @classmethod
    def reset(cls):
        cls.unresolved_nodes.clear()
        cls.resolved_nodes.clear()
        cls.nodes_by_handle.clear()
        cls.initialized = False

    @classmethod
    def resolve_all(cls):
        if not cls.initialized:
            raise Exception()

        try:
            cls._link_all_inheritance_nodes()

        finally:
            cls.reset()

    @classmethod
    def _link_all_inheritance_nodes(cls):
        for node in cls.unresolved_nodes:
            attribute_source = node.tyd_node.attribute_source

            if attribute_source is None:
                continue

            node.source

            if cls.nodes_by_handle.get(attribute_source, None) is None:
                raise Exception()

            if node.source is not None:
                node.source.add_heir(node)

    @classmethod
    def _resolve_all_unresolved_inheritance_nodes(cls):
        roots = [
            node
            for node in cls.unresolved_nodes
            if node.source is None or node.source.resolved
        ]

        for node in roots:
            cls._resolve_inheritance_node_add_heirs(node)

        for node in cls.unresolved_nodes:
            if not node.resolved:
                raise Exception()
            cls.resolved_nodes[node.tyd_node] = node

        cls.unresolved_nodes.clear()

    @classmethod
    def _resolve_inheritance_node_add_heirs(cls, node: InheritanceNode):
        if node.source is None:
            node.resolved = True

        else:
            if not node.source.resolved:
                raise Exception()

    @classmethod
    def _apply_inheritance(cls, source: TydNode, heir: TydNode):
        try:
            if isinstance(source, TydString):
                return

            if isinstance(heir, TydCollection):
                if heir.attribute_no_ingerit:
                    return

            if isinstance(source, TydTable):
                for child in source:
                    heir_matching_child = heir[child.name]

                    if heir_matching_child is not None:
                        cls._apply_inheritance(child, heir_matching_child)
                    else:
                        heir.insert(child, 0)

                return

            if isinstance(source, TydList):
                count = 0
                for s in source:
                    heir.insert(s, count)
                    count += 1
        except Exception:
            raise Exception()

    temp_used_node_names: Set[str] = set()

    @classmethod
    def _check_for_duplicate_nodes(cls, original: TydCollection):
        cls.temp_used_node_names.clear()

        for node in original:
            if node.name is None:
                continue

            if node.name in cls.temp_used_node_names:
                raise Exception()

            else:
                cls.temp_used_node_names.add(node.name)

        cls.temp_used_node_names.clear()
