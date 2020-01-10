import bisect
from math import inf

from src.trie import Trie, TrieNode

# diccionario para guardar los tries
trie_dic = {}


def lvrp(t, palabra, maxima_distancia=float('inf')):
    trie_dic[0] = (t.root, '')

    # { palabra : distancia } para comprobar si se logra una distancia mejor
    resultados = {}

    def save_sol(sol, dist):
        """
        Guarda la solucion si es mejor que la que habia o no existia una previamente
        """
        # comprobar que no hay una mejor solucion
        if (sol in resultados and resultados[sol] >= dist) or sol not in resultados:
            # si es solución añadimos al diccionario de resultados
            resultados[sol] = dist

    # Inicializar CLOSED vacio
    # (pos_trie, pos_palabra) usamos un set para que la comprobación sea mas rapida
    cerrados = set()

    # Inicializar abiertos con el nodo raiz
    # {pos_trie, pos_palabra : distancia}
    abiertos = {(0, 0): 0}

    # [(distancia, (pos_trie, pos_palabra))] lista para la extraccion ordenada
    orden = [(0, (0, 0))]

    while len(abiertos) != 0:

        # sacamos de la lista open
        nodo = orden.pop(0)[1]
        pos_trie = nodo[0]
        pos_palabra = nodo[1]
        distancia = abiertos[nodo]
        del abiertos[nodo]

        # guardamos en la lista cerrados
        cerrados.add((pos_trie, pos_palabra))

        # comprobamos si es solucion
        fin_palabra = pos_palabra == len(palabra)
        fin_palabra_trie = trie_dic[pos_trie][0].end_state
        distancia_adecuada = distancia <= maxima_distancia

        # obtenemos los hijos
        children = trie_dic[pos_trie][0].children.values()

        # posible solucion
        solucion = trie_dic[pos_trie][1]

        if fin_palabra_trie:
            if fin_palabra and distancia_adecuada:
                solucion = trie_dic[pos_trie][1]

            else:
                # Cota 2: Si fin trie devolver la distancia actual + la longitud restante de la palabra
                distancia += len(palabra) - pos_palabra

            save_sol(solucion, distancia)

        # Cota 3: Si llemgamos a la maxima distancia, no generamos mas hijos
        if distancia == maxima_distancia:
            continue

        # Cota 1: Si fin palabra devolver palabra del trie mas corta que se puede generar desde este nodo
        if fin_palabra:
            current_depth = trie_dic[pos_trie][0].depth
            min_leaf_depth = get_min_leaf_depth(children)

            # la distancia es la palabra mas corta que se puede generar desde el nodo actual
            # menos la profundidad del nodo actual
            distancia = min_leaf_depth - current_depth

            save_sol(solucion, distancia)

        # sacamos los hijos y calculamos sus distancias
        hijos = []

        fin_trie = pos_trie == trie.size

        for child in children:
            trie_dic[child.node_id] = (child, trie_dic[pos_trie][1] + child.char)

            # SUSTITUCIÓN
            if not fin_trie and not fin_palabra:
                if palabra[pos_palabra] == child.char:
                    hijos.append((distancia, child.node_id, pos_palabra + 1))
                else:
                    hijos.append((distancia + 1, child.node_id, pos_palabra + 1))

            # INSERCIÓN
            if not fin_trie:
                hijos.append((distancia + 1, child.node_id, pos_palabra))

            # DAMERAU
            if child.node_id in trie_dic and trie_dic[child.node_id].parent in trie_dic and \
                    trie_dic[trie_dic[child.node_id].parent] in trie_dic:
                peso = inf if palabra[pos_palabra - 1] != trie_dic[child.node_id].parent.char or \
                               palabra[pos_palabra - 2] != child.char else 1

                hijos.append((distancia + peso, child.node_id, pos_palabra + 2))

        # BORRADO
        if not fin_palabra:
            hijos.append((distancia + 1, pos_trie, pos_palabra + 1))

        # para cada hijo
        for hijo in hijos:
            # si no esta en CLOSED
            if hijo[1:] not in cerrados:
                # si no esta en OPEN, o esta en OPEN pero tiene una distancia mejor
                pertenece_y_mejor = (hijo[1], hijo[2]) in abiertos and hijo[0] < abiertos[(hijo[1], hijo[2])]
                no_pertenece = (hijo[1], hijo[2]) not in abiertos

                if no_pertenece or pertenece_y_mejor:
                    # insertamos en OPEN y ordena
                    abiertos[(hijo[1], hijo[2])] = hijo[0]
                    bisect.insort(orden, (hijo[0], (hijo[1], hijo[2])))

    return resultados


def get_min_leaf_depth(children):
    """
    Funcion que devuelve la profundidad mínima de los nodos hoja alcanzables
    """

    opened = list(children)

    while opened:
        node = trie_dic[opened[0].node_id][0]

        if node.end_state:
            return node.depth

        opened.extend(node.get_children())

        opened.remove(node)


trie = Trie(root=TrieNode(node_id=163848))

trie.add("perro")

print(trie)
