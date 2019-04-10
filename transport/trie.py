from __future__ import annotations
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    children: Dict[str, Node] = field(default_factory=dict)
    value: Any = None


class Trie:

    def __init__(self):
        self.root = Node()

    def insert(self, key: str, value: Any) -> None:
        current = self.root
        for char in key.lower():
            if char not in current.children:
                current.children[char] = Node()
            current = current.children[char]
        current.value = value

    def search(self, key_prefix: str) -> List:
        current = self.root
        for char in key_prefix.lower():
            if char in current.children:
                current = current.children[char]
            else:
                return []
        return self._get_all_child_values(current)

    def _get_all_child_values(self, node: Node) -> List:
        values = []
        for _, child in node.children.items():
            values.extend(self._get_all_child_values(child))
        if node.value:
            values.append(node.value)
        return values
