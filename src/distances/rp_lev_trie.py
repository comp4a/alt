#%%
import numpy as np
from trie import Trie
import bisect 
#%%
def lvrp(trie,palabra,maxima_distancia = float('inf')):
    trie_dic = { 0 :(trie.root,'') }

    # { palabra : distancia } para comprobar si se logra una distancia mejor
    resultados = {} 
    
    # Inicializar CLOSED vacio
    # (pos_palabra,pos_trie) usamos un set para que la comprobación sea mas rapida
    cerrados = set()   
    
    # Inicializar abiertos con el nodo raiz
    # {pos_trie, pos_palabra : distancia}
    abiertos = {}
    abiertos[(0,0)] = 0

    # [(distancia,(pos_trie,pos_palabra))]lista para la extraccion ordenada
    orden = [(0,(0,0))]

    while len(abiertos) != 0:
        
        # sacamos de la lista open
        nodo = orden.pop(0)[1]
        pos_trie = nodo[0]
        pos_palabra = nodo[1]
        distancia = abiertos[nodo]
        del abiertos[nodo]

        
        # guardamos en la lista cerrados 
        cerrados.add((pos_palabra,pos_trie))
        
        # comprobamos si es solucion
        palabra_completa_trie = trie_dic[pos_trie][0].end_state
        palabra_completa = pos_palabra == len(palabra)
        distancia_adecuada = distancia <= maxima_distancia

        if palabra_completa_trie and palabra_completa and distancia_adecuada:
            solucion = trie_dic[pos_trie][1]
            # comprobar que no hay una mejor solucion
            if (solucion in resultados and resultados[solucion] >= distancia) or solucion not in resultados:
                #si es solución añadimos al diccionario de resultados
                resultados[solucion] = distancia
        
        #sacamos los hijos y calculamos sus distancias
        hijos = []
        
        fin_palabra = pos_palabra == len(palabra)
        fin_trie = pos_trie == trie.size
        
        for child in trie_dic[pos_trie][0].children.values():
            trie_dic[child.node_id] = (child,trie_dic[pos_trie][1] + child.char)

            # SUSTITUCIÓN
            if fin_trie == False and fin_palabra == False:
                if palabra[pos_palabra] == child.char:
                    hijos.append((distancia,pos_palabra+1,child.node_id))
                else:
                    hijos.append((distancia+1,pos_palabra+1,child.node_id))

            # INSERCIÓN
            if fin_trie == False:
                hijos.append((distancia+1,pos_palabra,child.node_id))
                
        # BORRADO
        if fin_palabra == False:
            hijos.append((distancia+1,pos_palabra+1,pos_trie))
        
        # para cada hijo
        for hijo in hijos:                    
            # si no esta en CLOSED
            if hijo[1:] not in cerrados:
                # si no esta en OPEN, o esta en OPEN pero tiene una distancia mejor
                pertenece_y_mejor = (hijo[2],hijo[1]) in abiertos and hijo[0] < abiertos[(hijo[2],hijo[1])]
                no_pertenece = (hijo[2],hijo[1]) not in abiertos
                if no_pertenece or pertenece_y_mejor:
                    # insertamos en OPEN y ordena
                    abiertos[(hijo[2],hijo[1])] = hijo[0]
                    bisect.insort(orden, (hijo[0],(hijo[2],hijo[1]))) 

    return resultados
