from dataclasses import dataclass, field
from typing import Mapping, Any
from bisect import bisect_left

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

    def __repr__(self):
        res = "ID: " + str(self.node_id) + "\n\tDepth: " + str(self.depth) +\
               "\n\tChar: " + self.char + "\n\tChildren: ["
        for child in self.children.keys():
            res += " ({}):{}".format(self.children[child].node_id, child)
        res += " ]\n\tIt is an End State: " + str(self.end_state)
        return res


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

    depth : int
        Length of the largest word included
    """
    root: TrieNode = field(default=TrieNode())
    size: int = 0
    depth: int = 0

    def add(self, word: str):
        """
        Adds a word to the trie and returns its end state node

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
                if current_node.depth > self.depth:
                    self.depth = current_node.depth
            current_node = next_node
        current_node.end_state = True
        return current_node

    def to_list(self, ordered: bool = True):
        """
        Returns a list containing all the words of the trie

        Parameters
        ----------
        ordered : bool
            Whether the list must be ordered or not
        """
        prefixes = ["" for i in range(1, self.size+1)]
        opened = list(self.root.children.values())
        res = []
        while opened:
            node = opened[0]
            my_id = node.node_id
            is_end_state = node.end_state
            for child in node.children.values():
                opened.append(child)
            prefixes[my_id] += node.char
            if is_end_state:
                my_word = prefixes[my_id]
                if ordered:
                    index = bisect_left(res, my_word)
                    res.insert(index, res)
                else:
                    res.append(my_word)
            opened.remove(node)
        return res

    def __repr__(self):
        res = "TrieNode\nSize:\t" + str(self.size) + "Depth: " + str(self.depth)
        res += "\nAllNodes:\n========\n" + str(self.root)
        opened = list(self.root.children.values())
        while opened:
            node = opened[0]
            for child in node.children.values():
                opened.append(child)
            res += "\n\n" + str(node)
            opened.remove(node)
        return res

@dataclass
class TrieNodeWithContent(TrieNode):
    content: Any = None

    def __repr__(self):
        res = super()
        if self.end_state:
            res += "n\tContent: " + self.content
        return res

@dataclass
class TrieDict(Trie):
    def add(self, key: str, value):
        """
        Adds a word and his associated value to the trie

        Parameters
        ----------
        key : str
            Word to be added

        value: str
            Value associated to the key
        """
        current_node = self.root
        for c in key:
            children = current_node.children
            next_node = children.get(c, None)
            if not next_node:
                self.size += 1
                next_node = TrieNodeWithContent(c, {}, current_node, False, current_node.depth + 1, self.size, value)
                current_node.children[c] = next_node
                if current_node.depth > self.depth:
                    self.depth = current_node.depth
            current_node = next_node
        current_node.end_state = True

    def reach_node(self, word: str, force: bool = False):
        """
        Searches inside the trie if the word is contained, if it is it returns its
        end state if it is not then returns None; If force flag is activated it
        always reaches the node by creating the missing ones.

        Parameters
        ----------
        word : str
            Word to be searched

        force: bool
            Force mode flag
        """
        current_node = self.root
        for c in word:
            children = current_node.children
            next_node = children.get(c, None)
            if not next_node:
                if force:
                    self.size += 1
                    new_node_depth = current_node.depth + 1
                    next_node = TrieNode(c, {}, current_node, False, new_node_depth, self.size)
                    current_node.children[c] = next_node
                    if new_node_depth > self.depth:
                        self.depth = new_node_depth
                else:
                    return None
            current_node = next_node
        if not current_node.end_state:
            return None
        return current_node

