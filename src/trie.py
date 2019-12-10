from dataclasses import dataclass, field
from typing import Mapping, Any


@dataclass
class TrieNode:
    """
    Intern nodes of a Trie

    Attributes
    ----------
    char : str
        The character stored in the node

    children : dict -> { str: TrieNode }
        Children of the TrieNode:
            - key: character of the child
            - value: the child

    father : TrieNode
        Parent of the TrieNode

    end_state : bool
        Determines whether the node is an end state

    depth: int
        Depth of the TrieNode inside de Trie

    node_id: int
        Node ID
    """
    char: str = ""
    children: Mapping[int, Any] = field(default_factory=dict)
    father: Any = None
    end_state: bool = False
    depth: int = 0
    node_id: int = 0

    # To change the to_string redefine magic method __repr__
    def __repr__(self):
        return "ID: " + str(self.node_id) + "\n\tDepth: " + str(self.depth) + "\n\tChar: " + self.char + "\n\tChildren: "\
              + str(list(self.children.keys())) + "\n\tIt is an End State: " + str(self.end_state)


@dataclass
class Trie(object):
    """
    Data structure

    Attributes
    ----------
    root : TrieNode
        Root node of the Trie

    size : int
        Amount of nodes of the trie
    """
    root: TrieNode = field(default=TrieNode())
    size: int = 0

    def add(self, word: str):
        """
        Adds a word to the trie

        Parameters
        ----------
        word : str
            Word to be added
        """
        current_node = self.root
        for c in word:
            children = current_node.children
            next_node = children.get(c, None)
            if not next_node:
                self.size += 1
                next_node = TrieNode(c, {}, current_node, False, current_node.depth + 1, self.size)
                current_node.children[c] = next_node
            current_node = next_node
        current_node.end_state = True

    def __add__(self, word: str):
        self.add(word)

    def __repr__(self):
        res = "TrieNode\nSize: " + str(self.size)
        res += "\nAllNodes:\n========\n" + str(self.root)
        opened = list(self.root.children.values())
        while opened:
            node = opened[0]
            for child in node.children.values():
                opened.append(child)
            res += "\n\n" + str(node)
            opened.remove(node)
        return res
