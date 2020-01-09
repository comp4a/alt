from dataclasses import dataclass, field
from typing import Mapping, Any
from bisect import bisect_left
from random import randint

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
    children: Mapping[str, Any] = field(default_factory=dict)
    father: Any = None
    end_state: bool = False
    depth: int = 0
    node_id: int = 0

    def __repr__(self):
        return "'" + self.char + "' " + "| id: " + str(self.node_id) + " | f: " \
        + (str(self.father.node_id) if self.father else "[]") + " | end: " + str(self.end_state) + " | d: " + str(self.depth)


@dataclass
class Trie():
    """
    Data structure
    Attributes
    ----------
    desc: str
        Description of the uses of the trie
    root : TrieNode
        Root node of the Trie
    size : int
        Amount of nodes of the trie
    depth : int
        Length of the largest word included
    """
    desc: str = ""
    root: TrieNode = field(default=TrieNode)
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

    def to_list(self):
        """
        Returns a list containing all the words of the trie
        Parameters
        ----------
        ordered : bool
            Whether the list must be ordered or not
        """
        prefixes = {self.root.node_id:''}
        opened = list(self.root.children.values())
        res = []
        while opened:
            node = opened[0]
            my_id = node.node_id
            is_end_state = node.end_state
            for child in node.children.values():
                opened.append(child)
            my_prefix = prefixes[node.father.node_id] + node.char
            prefixes[my_id] = my_prefix
            if is_end_state:
                my_word = prefixes[my_id]
                res.append(my_word)
            opened.remove(node)
        return res

    def __repr__(self):
        res = "Trie: " + self.desc + "\nSize:\t" + str(self.size) + " Depth: " + str(self.depth)
        res += "\nAllNodes:\n========\n" + str(self.root)
        opened = list(self.root.children.values())
        while opened:
            node = opened[0]
            for child in node.children.values():
                opened.append(child)
            res += "\n" + str(node)
            opened.remove(node)
        return res

@dataclass
class TrieNodeWithContent(TrieNode):
    content: Any = None

    def __repr__(self):
        return "'" + self.char + "' " + "| id: " + str(self.node_id) + " | f: " \
               + (str(self.father.node_id) if self.father else "[]") + " | end: " + str(
            self.end_state) + " | d: " + str(self.depth) + " c= " + str(self.content)

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
                next_node = TrieNodeWithContent(c, {}, current_node, False, current_node.depth + 1, self.size)
                current_node.children[c] = next_node
                if current_node.depth > self.depth:
                    self.depth = current_node.depth
            current_node = next_node
        current_node.content = value
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
                    next_node = TrieNodeWithContent(c, {}, current_node, False, current_node.depth + 1, self.size, None)
                    if new_node_depth > self.depth:
                        self.depth = new_node_depth
                else:
                    return None
            current_node = next_node
        if not current_node.end_state:
            if force:
                current_node.end_state = True
            else:
                return None
        return current_node

    def get(self, key: str):
        """
        Returns the content associated with the key if it does not exist
        it returns None
        ----------
        word : str
            Word associated with the content
        """
        node = self.reach_node(key)
        if node:
            return node.content
        else:
            return None

    def __repr__(self):
        res = "TrieDict: " + self.desc + "\nSize:\t" + str(self.size) + " Depth: " + str(self.depth)
        res += "\nAllNodes:\n========\n" + str(self.root)
        opened = list(self.root.children.values())
        while opened:
            node = opened[0]
            for child in node.children.values():
                opened.append(child)
            res += "\n" + str(node)
            opened.remove(node)
        return res
