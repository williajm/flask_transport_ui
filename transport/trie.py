"""
trie.py provides trie search tree (AKA a prefix tree).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any


class Trie:
    """
    Trie implementation:
    A nodes position within the tree defines the key with which it is associated.
    All child nodes of a given node share a common prefix.
    """

    def __init__(self):
        self._root = _Node()

    def insert(self, key: str, value: Any) -> None:
        """
        Insert a key value pair into the Trie.
        :param key: determines node position and will be searchable by prefix.
        :param value: value to be stored.
        """
        current = self._root
        for char in key.lower():
            if char not in current.children:
                current.children[char] = _Node()
            current = current.children[char]
        current.value = value

    def search(self, key_prefix: str) -> List:
        """
        Search the Trie for all nodes with a common prefix.
        :param key_prefix: search parameter
        :return: A lit of values which share a common prefix
        e.g. with a key_prefix for 'Ba' the trie could possibly return ['Ban', 'Ball', 'Barbecue']
        """
        current = self._root
        for char in key_prefix.lower():
            if char in current.children:
                current = current.children[char]
            else:
                return []
        return self._get_all_child_values(current)

    def _get_all_child_values(self, node: _Node) -> List:
        values = []
        for _, child in node.children.items():
            values.extend(self._get_all_child_values(child))
        if node.value:
            values.append(node.value)
        return values


@dataclass(eq=False)
class _Node:
    children: Dict[str, _Node] = field(default_factory=dict)
    value: Any = None
