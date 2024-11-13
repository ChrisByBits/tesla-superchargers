import { teslas } from './teslas.js';

let mapAStar;
let markerAStar;
let directionsServiceAStar;
let directionsRendererAStar;
let ubicacion_inicio = null;
let ubicacion_destino = null;
let contador_clicks = 0;

export function initMapAStar() {

  mapAStar = new google.maps.Map(document.getElementById("map-a-star"), {
    center: { lat: 34.61456, lng: -120.188387 },
    zoom: 7,
  });

  directionsServiceAStar = new google.maps.DirectionsService();
  directionsRendererAStar = new google.maps.DirectionsRenderer();
  directionsRendererAStar.setMap(mapAStar);

  mapAStar.addListener("click", function (e) {
    const ubicacion_usuario = e.latLng;

    if (contador_clicks === 0) {
      ubicacion_inicio = ubicacion_usuario;
      contador_clicks++;
      markerAStar = new google.maps.Marker({
        position: ubicacion_inicio,
        map: mapAStar,
        title: "Ubicación de Inicio",
      });
      document.getElementById("mensaje-a-star").innerText = "Selecciona la ubicación de fin...";
    } else if (contador_clicks === 1) {
      // Segundo clic: ubicación de fin
      ubicacion_destino = ubicacion_usuario;
      contador_clicks++;

      if (markerAStar) {
        markerAStar.setMap(null); // Eliminar el marcador anterior
      }

      markerAStar = new google.maps.Marker({
        position: ubicacion_destino,
        map: mapAStar,
        title: "Ubicación de Fin",
      });

      const selectTesla = document.getElementById("tesla-select");
      const teslaSeleccionado = selectTesla.value;
      const tesla = teslas[teslaSeleccionado];

      document.getElementById("mensaje-a-star").innerText = "Buscando estaciones cercanas...";
      planificar_ruta(ubicacion_inicio, ubicacion_destino, tesla.modelo, tesla.capacidad, tesla.consumoPorKm);
    }
  });
}

function planificar_ruta(ubicacion_inicio, ubicacion_destino, modelo, capacidadBateria, consumoPorKm) {
 
  const latInicio = ubicacion_inicio.lat();
  const lngInicio = ubicacion_inicio.lng();
  const latDestino = ubicacion_destino.lat();
  const lngDestino = ubicacion_destino.lng();

  fetch('/planificar_ruta', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      latInicio: latInicio,
      lngInicio: lngInicio,
      latDestino: latDestino,
      lngDestino: lngDestino,
      modelo: modelo,
      capacidadBateria: capacidadBateria,
      consumoPorKm: consumoPorKm,
    }),
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    if (data.ruta && data.ruta.length > 0) {
      
      const puntosRuta = data.ruta.map(nodo => {
        return {
          lat: nodo['GPS'][0],
          lng: nodo['GPS'][1],
        };
      });

      const request = {
        origin: ubicacion_inicio,
        destination: ubicacion_destino,
        waypoints: puntosRuta.map(p => ({ location: new google.maps.LatLng(p.lat, p.lng) })),
        travelMode: google.maps.TravelMode.DRIVING,
      };

      console.log(puntosRuta)

      directionsServiceAStar.route(request, (response, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          directionsRendererAStar.setDirections(response);
        } else {
          console.error('Error al calcular la ruta: ' + status);
        }
      });
      document.getElementById("mensaje-a-star").innerText = "Tu ruta ha sido planificada. ¡Que tengas un excelente viaje!";

    } else {
      document.getElementById("mensaje-a-star").innerText = "No se encontró una ruta.";
    }
  })
  .catch(error => {
    console.error('Error al hacer la petición:', error);
    document.getElementById("mensaje").innerText = "Error al buscar estaciones cercanas.";
  });
}

window.onload = initMapAStar;