
# estructura para crear un trie
class TrieNode(object):
    indice = 0
    def __init__(self, char):
        self.char = char 
        self.children = []
        self.word_finished = False
        self.word=""
        self.counter = 1

    def add(self, word):

        node = self
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
                node = new_node
                TrieNode.indice += 1
                node.indice =TrieNode.indice
                
        
        node.word_finished = True
        node.word = word

    def toString(self):
        word = ""
        if(self.word_finished):
            word= str(self.word)
        print(str(self.indice)+" " +self.char + "  " + str(self.counter) + "  "+str(self.word_finished)+"   " + word)
        
        for node in self.children:
            node.toString()
