import json
from .nodo import Nodo
from .grafo import Grafo
from .estacion_de_carga import EstacionDeCarga
from math import radians, cos, sin, sqrt, atan2

class ControlEstaciones:
    def __init__(self, archivo_json):
        self.grafo = Grafo()  # El grafo contendrá todas las estaciones
        self.nodo_inicio = None  # Inicialmente, no hay nodo de inicio
        self.nodo_destino = None  # Inicialmente, no hay nodo de fin
        self.cargar_estaciones(archivo_json)  # Cargar estaciones al iniciar

    def cargar_estaciones(self, archivo_json):
        """Carga las estaciones desde un archivo JSON y las agrega al grafo."""
        with open(archivo_json, 'r') as archivo:
            data = json.load(archivo)

        for estacion in data:
            nueva_estacion = EstacionDeCarga(estacion)
            nombre = nueva_estacion.nombre
            # Agregar la estación al grafo usando su nombre o id como clave
            self.grafo.agregar_nodo(nombre, nueva_estacion)

        # Conectar estaciones cercanas después de cargarlas
        self.conectar_estaciones_cercanas()

    def calcular_distancia(self, coord1, coord2):
        """Calcula la distancia entre dos coordenadas geográficas."""
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        R = 6371.0  # Radio de la Tierra en kilómetros
        distancia = R * c
        return distancia

    def conectar_estaciones_cercanas(self):
        """Conecta las estaciones cercanas en el grafo."""
        for estacion in self.grafo.nodos.values():  # Iterar sobre los nodos del grafo
            distancias = []
            for otra_estacion in self.grafo.nodos.values():
                if estacion.id != otra_estacion.id:
                    distancia = self.calcular_distancia(estacion.gps, otra_estacion.gps)
                    distancias.append((otra_estacion, distancia))
            distancias.sort(key=lambda x: x[1])
            estaciones_cercanas = distancias[:10]
            for estacion_cercana, distancia in estaciones_cercanas:
                # Conectar usando los nodos directamente
                self.grafo.conectar_nodos(estacion.id, estacion_cercana.id, distancia)

    def conectar_inicio_y_destino(self, coord_inicio, coord_destino = None):
        """Conecta un nodo de inicio y destino (si existe) a las estaciones más cercanas."""

        if self.nodo_inicio != None:
            self.grafo.eliminar_nodo(self.nodo_inicio.nombre)

        if self.nodo_destino != None:
            self.grafo.eliminar_nodo(self.nodo_destino.nombre)

        # Crear un nuevo nodo de usuario como estación de carga
        nodo_inicio = EstacionDeCarga({
            'Supercharger': 'inicio',
            'GPS': coord_inicio,
            'Address': 'Inicio',
            'City': '',
            'State': '',
            'Zip': '',
            'Country': '',
            'Stalls': 0,
            'kW': 0,
            'Elev': 0,
            'Date': ''
        })

        self.nodo_inicio = nodo_inicio

        # Agregar el nodo inicio al grafo
        self.grafo.agregar_nodo('inicio', nodo_inicio)

        if coord_destino:
            nodo_destino = EstacionDeCarga({
                'Supercharger': 'destino',
                'GPS': coord_destino,
                'Address': 'Destino',
                'City': '',
                'State': '',
                'Zip': '',
                'Country': '',
                'Stalls': 0,
                'kW': 0,
                'Elev': 0,
                'Date': ''
            })

            self.nodo_destino = nodo_destino
            self.grafo.agregar_nodo('destino', nodo_destino)

        # Conectar a las estaciones más cercanas
        self.conectar_estaciones_cercanas()

        return self.nodo_inicio, self.nodo_destino