class Nodo:
    def __init__(self, id, datos):
        self.id = id
        self.datos = datos
        self.conexiones = {}

    def agregar_conexion(self, nodo, peso):
        self.conexiones[nodo] = peso

    def __repr__(self):
        return f"Nodo(id={self.id}, datos={self.datos}, conexiones={list(self.conexiones.keys())})"