class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, id_nodo, nodo):
        if id_nodo in self.nodos:
            raise ValueError("El nodo ya existe en el grafo.")
        self.nodos[id_nodo] = nodo

    def conectar_nodos(self, id_nodo1, id_nodo2, peso):
        if id_nodo1 in self.nodos and id_nodo2 in self.nodos:
            self.nodos[id_nodo1].agregar_conexion(self.nodos[id_nodo2], peso)
            self.nodos[id_nodo2].agregar_conexion(self.nodos[id_nodo1], peso)
        else:
            raise ValueError("Uno de los nodos no está en el grafo.")

    def eliminar_nodo(self, id_nodo):
        if id_nodo in self.nodos:
            for vecino in list(self.nodos[id_nodo].conexiones.keys()):
                if vecino in self.nodos:
                    self.nodos[vecino].conexiones.pop(id_nodo, None)
            del self.nodos[id_nodo]
        else:
            raise ValueError("El nodo no existe en el grafo.")

    def __repr__(self):
        return f"Grafo(nodos={list(self.nodos.keys())})"
