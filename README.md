# Trabajo Final - Complejidad Algorítmica
## Estaciones de carga de Tesla

Esta aplicación permite a los usuarios encontrar las estaciones de carga de vehículos Tesla más cercanos a ellos utilizando el algoritmo BFS. Además haciendo uso de A*, permite seleccionar una ubicación de inicio y una ubicación de destino en un mapa para planificar una ruta optimizada considerando la capacidad de batería y el consumo por kilómetro. 


## Funcionalidades

- Selección de puntos de inicio y destino mediante clics en el mapa.
- Planificación de rutas considerando el consumo de batería y la distancia entre estaciones.
- Visualización de estaciones de carga cercanas en el trayecto.
- Interfaz interactiva con Google Maps y marcadores personalizables.

## Tecnologías Utilizadas

- **Frontend:** JavaScript, Google Maps API
- **Backend:** Flask (Python)
- **Algoritmos de Rutas:**
- - BFS para hacer búsqueda en profundidad
- - (A estrella) para optimizar la ruta con condiciones de batería y distancia.

## Instalación

Instala Flask utilizando el comando ``pip install flask``	

## Funcionamiento

Ejecuta la aplicación con el comando ``python app.py``	

Accede a la URL mostrada en la terminal dentro de tu navegador para utilizar la aplicación.