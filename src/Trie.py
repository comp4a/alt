class TrieNode(object):
    """
    Nodo interno de un Trie

    Attributes
    ----------
    indice : int
        Identificador del nodo (en orden)

    char : char
        Letra que guarda el nodo

    children : TrieNode[] <- lista
        Numero de nodos del trie

    father : TrieNode
        Padre del nodo

    word_finished : bool
        Indica si el TrieNode completa una palabra

    word : str
        Palabra guardada por el TrieNode

    counter: int
        Numero de palabras que pasan por el TrieNode

    """
    def __init__(self, char):
        self.indice = 0
        self.char = char
        self.children = []
        self.father = None
        self.word_finished = False
        self.word= None
        self.counter = 1
        self.depth = 0

    
    def toString(self):
        word2 = ""
        res = ""
        if(self.word_finished):
            word2 = str(self.word)
        if self.indice != 0 :
            res =  str(self.indice)+"\t" + str(self.father.indice)+"\t" +self.char + "\t" + str(self.counter) + "\t"+str(self.word_finished)+"\t" + word2 + "\n"
        else: 
            res =  str(self.indice)+"\tN\t" +self.char + "\t" + str(self.counter) + "\t"+str(self.word_finished)+"\t" + word2 + "\n"

        for node in self.children:
            res = res + node.toString()
        return res  
        


class Trie(object):
    """
    Estructura de datos Trie

    Attributes
    ----------
    size : int
        Numero de nodos del trie
    node : TrieNode
        Nodo raiz del Trie
    dictionary : dictionary[int:TrieNode]
        diccionario que vincula el indice con el nodo para accesos mas rápidos
    """
    def __init__(self):
        self.size = 0
        self.node = TrieNode('')
        self.dictionary = {0 : self.node}
        
    def add(self, word):
        """
        Añade una palabra al Trie

        Parameters
        ----------
        word : str
            palabra a añadir
    
        """
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
                new_node.depth = node.depth+1
                node = new_node
                self.size += 1
                node.indice = self.size
#                 Inserta elemento en tabla hash
                self.dictionary[node.indice] = node
                
        node.word_finished = True
        node.word = word

    def toString(self):
        """
        Devuelve un string que describe el Trie

        Returns
        -------
        str
    
        """
        node = self.node
        return node.toString()

    def pull(self,ind):
        """
        Dado un indice devuelve el TrieNode asociado

        Parameters
        ----------
        ind : int
            indice del nodo a devolver

        Returns
        -------
        TrieNode
    
        """
        return self.dictionary[ind]

                    
# trie = Trie()
# trie.add("caro")
# trie.add("cara")
# trie.add("codo")
# trie.add("caros")

# print(trie.toString())
# print("=====")
# for i in range(0,10):
#     print(trie.pull(i).indice)

help(Trie)
