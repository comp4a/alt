#%%
import numpy as np

#%%
def levenshtein_distance2(x, y):
    current_row = np.zeros((1+len(x)))
    previous_row = np.zeros((1+len(x)))
    
    current_row[0] = 0
    for i in range(1, len(x)+1):
        current_row[i] = current_row[i-1] + 1
    for j in range(1, len(y)+1):
        previous_row, current_row = current_row, previous_row
        current_row[0] = previous_row[0] + 1
        for i in range(1, len(x)+1):
            current_row[i] = min(current_row[i-1] + 1,
            previous_row[i] + 1,
            previous_row[i-1] + (x[i-1] != y[j-1]))
    return current_row[len(x)]

#%%
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

#%%
trie = Trie()
trie.add("caros")
trie.add("cara")
trie.add("caro")
trie.add("codo")
trie.add("xaro")
palabra = "cara"
print(trie.toString())
print(levenshtein_distance2('bazs','baz'))

#%%
def lvrp(maxima_distancia):
    
    # { palabra : distancia } para comprobar si se logra una distancia mejor
    resultados = {} 
    
    # Inicializar CLOSED vacio
    # (pos_palabra,id_trie) usamos un set para que la comprobación sea mas rapida
    cerrados = set()   
    
    # Inicializar abiertos con el nodo raiz
    # (distancia,pos_palabra,id_trie)
    abiertos = np.ndarray((0,3),np.intc)
    abiertos = np.append(abiertos,[[0,0,0]],0)
    
    while abiertos.size != 0:
        
        # sacamos de la lista open
        nodo = abiertos[0]
        abiertos = abiertos[1:]
        
        distancia = nodo[0]
        pos_palabra = nodo[1]
        pos_trie = nodo[2]
        
        # guardamos en la lista cerrados 
        cerrados.add((pos_palabra,pos_trie))
        
        # comprobamos si es solucion
        palabra_completa_trie = trie.dictionary[pos_trie].word_finished
        palabra_completa = fin_palabra = pos_palabra == len(palabra)
        distancia_adecuada = distancia <= maxima_distancia

        if palabra_completa_trie and palabra_completa and distancia_adecuada:
            solucion = trie.dictionary[pos_trie].word
            # comprobar que no hay una mejor solucion
            if (solucion in resultados and resultados[solucion] >= distancia) or solucion not in resultados:
                #si es solución añadimos al diccionario de resultados
                resultados[solucion] = distancia
        
        #sacamos los hijos y calculamos sus distancias
        hijos = []
        
        fin_palabra = pos_palabra == len(palabra)
        fin_trie = pos_trie == len(trie.dictionary)
        
        for pos_hijo_trie in trie.pull(pos_trie).children:
            # SUSTITUCIÓN
            if fin_trie == False and fin_palabra == False:
                char_palabra = palabra[pos_palabra]
                char_trie = trie.pull(pos_hijo_trie.indice).char
                if(palabra[pos_palabra] == trie.pull(pos_hijo_trie.indice).char):
                    hijos.append((distancia,pos_palabra+1,pos_hijo_trie.indice))
                else:
                    hijos.append((distancia+1,pos_palabra+1,pos_hijo_trie.indice))

            # INSERCIÓN
            if fin_trie == False:
                hijos.append((distancia+1,pos_palabra,pos_hijo_trie.indice))
                
        # BORRADO
        if fin_palabra == False:
            hijos.append((distancia+1,pos_palabra+1,pos_trie))
        
        # para cada hijo
        for hijo in hijos:                    
            # si no esta en CLOSED
            if hijo[1:] not in cerrados:
                # si no esta en OPEN, o esta en OPEN pero tiene una distancia mejor
                #TODO: aclarar esto
                aux = np.where((abiertos[:,1:]==hijo[1:]).all(axis=1))[0]
                pertenece_y_mejor = aux.size > 0 and hijo[0] < abiertos[aux[0]][0]
                no_pertenece = all((abiertos[:,1:]!=hijo[1:]).any(1))
                if no_pertenece or pertenece_y_mejor:
                    # insertamos en OPEN y ordena
                    abiertos = np.append(abiertos,[[hijo[0],hijo[1],hijo[2]]],0)
                    abiertos_watch = abiertos.tolist()

    return resultados

print(lvrp(2))


# %%
