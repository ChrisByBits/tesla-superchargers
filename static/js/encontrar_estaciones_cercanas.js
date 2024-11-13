let map;
let marker;
let stations = [];
let directionsService;
let directionsRenderer;
let dropdownEstaciones = document.getElementById("dropdown-estaciones");

export function initMapBfs() {
  map = new google.maps.Map(document.getElementById("map-bfs"), {
    center: { lat: 34.61456, lng: -120.188387 },
    zoom: 7,
  });

  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  map.addListener("click", function (e) {
    const ubicacion_usuario = e.latLng;

    if (marker) {
      marker.setMap(null);
    }

    marker = new google.maps.Marker({
      position: ubicacion_usuario,
      map: map,
      title: "Tu ubicación",
    });

    document.getElementById("mensaje-bfs").innerText = "Buscando estaciones cercanas...";

    // Ocultar el dropdown antes de buscar las estaciones
    dropdownEstaciones.style.display = "none";
    
    encontrar_estaciones_cercanas(ubicacion_usuario);
  });
}

function encontrar_estaciones_cercanas(ubicacion_usuario) {
  const lat = ubicacion_usuario.lat();
  const lng = ubicacion_usuario.lng();
  const quantity = parseInt(document.getElementById("cantidadEstaciones").value, 10);
  const kmLimit = parseFloat(document.getElementById("limiteKilometros").value);

  fetch('/encontrar_estaciones_cercanas', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ lat, lng, quantity, kmLimit }),
  })
    .then(response => response.json())
    .then(data => {
      const estaciones = data.estaciones_cercanas;
      if (estaciones.length === 0) {
        alert("No se encontraron estaciones cercanas.");
        return;
      }

      if (stations.length > 0) {
        stations.forEach(station => station.setMap(null));
        stations = [];
      }

      dropdownEstaciones.innerHTML = '<option value="" disabled selected>Selecciona una estación cercana</option>';
      
      estaciones.forEach((estacion, index) => {
        const position = { lat: estacion.GPS[0], lng: estacion.GPS[1] };
        
        const stationMarker = new google.maps.Marker({
          position: position,
          map: map,
          title: estacion.Supercharger,
        });
        
        stations.push(stationMarker);

        const option = document.createElement("option");
        option.value = index;
        option.text = estacion.Supercharger;
        dropdownEstaciones.appendChild(option);
      });

      dropdownEstaciones.style.display = "block";

      dropdownEstaciones.addEventListener("change", () => {
        const selectedIndex = dropdownEstaciones.value;
        const selectedStation = estaciones[selectedIndex];
        const selectedPosition = { lat: selectedStation.GPS[0], lng: selectedStation.GPS[1] };

        const request = {
          origin: ubicacion_usuario,
          destination: selectedPosition,
          travelMode: 'DRIVING',
        };

        directionsService.route(request, (result, status) => {
          if (status === 'OK') {
            directionsRenderer.setDirections(result);
          } else {
            console.error('Error al calcular la ruta:', status);
          }
        });
      });
    })
    .then(() => {
      document.getElementById("mensaje-bfs").innerText = "Estaciones cercanas encontradas. Selecciona una para ver la ruta.";
    })
    .catch(error => {
      console.error('Error al buscar estaciones cercanas:', error);
    });
}
