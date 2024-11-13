from .nodo import Nodo

class EstacionDeCarga(Nodo):
    def __init__(self, datos):
        id_estacion = datos['Supercharger']
        super().__init__(id_estacion, datos)
        
        self.nombre = datos['Supercharger']
        self.direccion = datos['Address']
        self.ciudad = datos['City']
        self.estado = datos['State']
        self.zip = datos['Zip']
        self.pais = datos['Country']
        self.estaciones = int(datos['Stalls'])
        self.kW = int(datos['kW'])
        self.gps = datos['GPS']
        self.elevacion = datos['Elev']
        self.fecha = datos['Date']

    def __repr__(self):
        return f"EstacionDeCarga(nombre={self.nombre}, direccion={self.direccion}, ciudad={self.ciudad}, estado={self.estado}, zip={self.zip}, pais={self.pais}, estaciones={self.estaciones}, kW={self.kW}, gps={self.gps}, elevacion={self.elevacion}, fecha={self.fecha})"
    
    def __hash__(self):
        return hash(self.nombre)

    def __eq__(self, other):
        return isinstance(other, EstacionDeCarga) and self.nombre == other.nombre