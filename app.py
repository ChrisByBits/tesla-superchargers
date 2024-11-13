from flask import Flask, jsonify, request, render_template
from model.control_estaciones import ControlEstaciones
from model.tesla import Tesla
from algorithms.bfs import bfs_estaciones_cercanas
from algorithms.a_star import a_star_ruta

class EstacionesApp:
    def __init__(self, config):
        # Configuración inicial
        self.app = Flask(__name__)
        self.config = config
        self.tesla = None
        self.control_estaciones = ControlEstaciones(self.config['data_file'])
        self.GOOGLE_MAPS_API_KEY = config['google_maps_api_key']
        
        # Conectar estaciones cercanas al inicio
        self.control_estaciones.conectar_estaciones_cercanas()

        # Configurar las rutas de la aplicación
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', api_key=self.GOOGLE_MAPS_API_KEY)
        
        @self.app.route('/grafo')
        def grafo():
            return render_template('grafo.html')
        
        @self.app.route('/estaciones', methods=['GET'])
        def estaciones():
            result = []
            for estacion in self.control_estaciones.grafo.nodos.values():
                # Crear un diccionario con la información adicional
                estacion_info = {
                    'id': estacion.id,
                    'nombre': estacion.nombre,
                    'direccion': estacion.direccion,
                    'ciudad': estacion.ciudad,
                    'estado': estacion.estado,
                    'zip': estacion.zip,
                    'pais': estacion.pais,
                    'estaciones': estacion.estaciones,
                    'kW': estacion.kW,
                    'gps': estacion.gps,
                    'elevacion': estacion.elevacion,
                    'fecha': estacion.fecha
                }
                
                # Para cada conexión (vecino, peso), agregamos la información de la estación
                for vecino, peso in estacion.conexiones.items():
                    result.append({
                        'origen': estacion.id,
                        'destino': vecino.id,
                        'peso': peso,
                        'origen_info': estacion_info,  # Información de la estación origen
                        'destino_info': {
                            'id': vecino.id,
                            'nombre': vecino.nombre,
                            'direccion': vecino.direccion,
                            'ciudad': vecino.ciudad,
                            'estado': vecino.estado,
                            'zip': vecino.zip,
                            'pais': vecino.pais,
                            'estaciones': vecino.estaciones,
                            'kW': vecino.kW,
                            'gps': vecino.gps,
                            'elevacion': vecino.elevacion,
                            'fecha': vecino.fecha
                        }
                    })
            
            return jsonify({'conexiones': result})
        
        @self.app.route('/encontrar_estaciones_cercanas', methods=['POST'])
        def encontrar_estaciones_cercanas():
            data = request.json
            lat = data['lat']
            lng = data['lng']
            max_distancia = data['kmLimit']
            cantidad_estaciones = data['quantity']


            ubicacion_inicio = (lat, lng)
            nodo_inicio, nodo_fin = self.control_estaciones.conectar_inicio_y_destino(ubicacion_inicio)

            estaciones_cercanas = bfs_estaciones_cercanas(self.control_estaciones.grafo, nodo_inicio.id, max_distancia, cantidad_estaciones)

            estaciones_respuesta = [estacion.datos for estacion in estaciones_cercanas]
            return jsonify({'estaciones_cercanas': estaciones_respuesta})

        @self.app.route('/planificar_ruta', methods=['POST'])
        def planificar_ruta():
            data = request.json
            punto_inicio = (data['latInicio'], data['lngInicio'])
            punto_destino = (data['latDestino'], data['lngDestino'])
            modelo_tesla = data['modelo']
            capacidad_bateria = data['capacidadBateria']
            consumo_por_km = data['consumoPorKm']
            self.tesla = Tesla(modelo_tesla, capacidad_bateria, consumo_por_km)

            nodo_inicio, nodo_destino = self.control_estaciones.conectar_inicio_y_destino(punto_inicio, punto_destino)
            ruta = a_star_ruta(self.control_estaciones.grafo, nodo_inicio.id, nodo_destino.id, self.tesla.capacidad, self.tesla.perdida_por_km)

            return jsonify({'ruta': [nodo.datos for nodo in ruta]})

    def run(self, debug=True):
        self.app.run(debug=debug)

config = {
    'data_file': 'data/dataset.json',
    'google_maps_api_key': ''
}

if __name__ == '__main__':
    estaciones_app = EstacionesApp(config)
    estaciones_app.run(debug=True)
