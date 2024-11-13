from collections import deque
from model.estacion_de_carga import EstacionDeCarga 

def bfs_estaciones_cercanas(grafo, nodo_inicio_id, max_distancia, cantidad_estaciones_cercanas):
    try:
        nodo_inicio = grafo.nodos[nodo_inicio_id]
    except KeyError:
        print(f"Error: No se encontró el nodo con id {nodo_inicio_id}")
        return []

    cola = deque([(nodo_inicio, 0)])  # (nodo_actual, distancia)
    estaciones_cercanas = []

    visited = set()  # Conjunto para rastrear nodos visitados
    visited.add(nodo_inicio_id)

    while cola:
        nodo_actual, distancia_actual = cola.popleft()

        if distancia_actual > max_distancia:
            continue

        if isinstance(nodo_actual, EstacionDeCarga) and nodo_actual.nombre != 'inicio':
            estaciones_cercanas.append((nodo_actual, distancia_actual))

        for vecino, distancia in nodo_actual.conexiones.items():
            if vecino.nombre not in visited:
                visited.add(vecino.nombre)
                cola.append((grafo.nodos[vecino.nombre], distancia_actual + distancia))

    estaciones_cercanas.sort(key=lambda x: x[1])  # Ordenar por distancia

    return [estacion for estacion, _ in estaciones_cercanas[:cantidad_estaciones_cercanas]]
