import pandas as pd
from collections import deque


data = pd.read_csv("ComplejidadAlgoritmicaDF.csv")

class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_arista(self, nodo1, nodo2):
        if nodo1 not in self.grafo:
            self.grafo[nodo1] = []
        if nodo2 not in self.grafo:
            self.grafo[nodo2] = []

        if nodo2 not in self.grafo[nodo1]:
            self.grafo[nodo1].append(nodo2)
        if nodo1 not in self.grafo[nodo2]:
            self.grafo[nodo2].append(nodo1)

    def obtener_vecinos(self, nodo):

        return self.grafo.get(nodo, [])

grafo = Grafo()
for _, row in data.iterrows():
    nodo = str(row['ID'])
    amigos = eval(row['Amigos'])
    for amigo in amigos:
        grafo.agregar_arista(nodo, amigo)

def bfs_busqueda(grafo, inicio, destino):
    visitados = set()
    cola = deque([(inicio, [inicio])])
    while cola:
        nodo_actual, camino = cola.popleft()
        if nodo_actual == destino:
            return camino
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for vecino in grafo.obtener_vecinos(nodo_actual):
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))

    return None

def amigos_en_comun(grafo, usuario1, usuario2):
    amigos1 = set(grafo.obtener_vecinos(usuario1))
    amigos2 = set(grafo.obtener_vecinos(usuario2))
    return len(amigos1.intersection(amigos2))

def buscar_por_nombre_o_apellido(nombre_o_apellido):
    resultados = data[(data['Nombre'].str.contains(nombre_o_apellido, case=False)) | 
                      (data['Apellido'].str.contains(nombre_o_apellido, case=False))]
    return resultados

def encontrar_mejor_coincidencia(usuario_id, posibles_ids):
    mejor_coincidencia = None
    max_amigos_comun = -1
    mejor_camino = None
    for posible_id in posibles_ids:
        camino = bfs_busqueda(grafo, usuario_id, posible_id)
        if camino:
            num_amigos_comun = amigos_en_comun(grafo, usuario_id, posible_id)
            if num_amigos_comun > max_amigos_comun:
                max_amigos_comun = num_amigos_comun
                mejor_coincidencia = posible_id
                mejor_camino = camino
    return mejor_coincidencia, max_amigos_comun, mejor_camino
