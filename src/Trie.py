class TrieNode(object):
    def __init__(self, char):
        self.indice = 0
        self.char = char
        self.children = []
        self.father = None
        self.word_finished = False
        self.word= None
        self.counter = 1

    def pull(self,ind):
        if(self.indice == ind):
            return self
        else:
            for nodeChild in self.children:
                if nodeChild.indice <= ind:
                    return nodeChild.pull(ind)

                
    def toString(self):
        word = ""
        res = ""
        if(self.word_finished):
            word= str(self.word)
        res =  str(self.indice)+" " +self.char + "  " + str(self.counter) + "  "+str(self.word_finished)+"   " + word + "\n"

        for node in self.children:
            res = res + node.toString()
        
        return res  
        
class Trie(object):
    def __init__(self):
        self.size = 0
        self.node = TrieNode('')
        
    def add(self, word):
        node = self.node
        for char in word:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node.counter += 1
                    node = child
                    found_in_child = True
                    break
            
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node.counter += 1
                new_node.father = node
                node = new_node
                self.size += 1
                node.indice = self.size
        node.word_finished = True
        node.word = word

    def toString(self):
        node = self.node
        return node.toString()

    def pull(self,ind):
        node = self.node
        return node.pull(ind)
    


                    
trie = Trie()
trie.add("caro")
trie.add("cara")
trie.add("codo")
trie.add("caros")

print(trie.toString())
trie.pull(9).char