import heapq

def a_star_ruta(grafo, nodo_inicio_id, nodo_destino_id, capacidad_bateria, consumo_por_km):
    try:
        nodo_inicio = grafo.nodos[nodo_inicio_id]
        nodo_destino = grafo.nodos[nodo_destino_id]
    except KeyError:
        print(f"Error: No se encontró el nodo con id {nodo_inicio_id} o {nodo_destino_id}")
        return []

    # Verificar si los nodos son válidos
    if nodo_inicio is None or nodo_destino is None:
        return []

    open_set = []
    heapq.heappush(open_set, (0, nodo_inicio))  # (costo, nodo)
    came_from = {}
    g_score = {nodo.id: float('inf') for nodo in grafo.nodos.values()}
    g_score[nodo_inicio.id] = 0

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current.id == nodo_destino.id:
            return reconstruir_ruta(came_from, current)

        # Iterar sobre las conexiones del nodo actual
        for vecino, distancia in current.conexiones.items():
            # Calcular el costo de ir al vecino
            new_g_score = g_score[current.id] + distancia
            
            # Calcular el consumo de batería
            consumo_bateria = distancia * consumo_por_km

            # Solo consideramos el vecino si tenemos suficiente batería
            if capacidad_bateria - consumo_bateria >= 0:
                if new_g_score < g_score[vecino.id]:
                    g_score[vecino.id] = new_g_score
                    came_from[vecino.id] = current
                    # Agregar el vecino al conjunto abierto
                    f_score = new_g_score + heuristica(grafo.nodos[vecino.id], nodo_destino)
                    heapq.heappush(open_set, (f_score, grafo.nodos[vecino.id]))

    return []  # No hay ruta encontrada

def heuristica(nodo_a, nodo_b):
    """Calcula una heurística simple (distancia euclidiana) entre dos nodos."""
    lat1, lon1 = nodo_a.datos['GPS']
    lat2, lon2 = nodo_b.datos['GPS']
    return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

def reconstruir_ruta(came_from, nodo_actual):
    """Reconstruye la ruta desde el nodo de destino hasta el inicio."""
    total_path = [nodo_actual]
    while nodo_actual.id in came_from:
        nodo_actual = came_from[nodo_actual.id]
        total_path.append(nodo_actual)
    return total_path[::-1]  # Retornar la ruta en orden desde inicio a destino
