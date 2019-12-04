from construirTrie import TrieNode


if __name__ == "__main__":
    trie = TrieNode("")
    trie.add("caro")
    trie.add("cara")
    trie.add("codo")
    trie.add("caros")
    trie.toString()