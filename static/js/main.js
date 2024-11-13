import { initMapBfs } from './encontrar_estaciones_cercanas.js';
import { initMapAStar } from './planificar_ruta.js';
import { cargarTeslas } from './teslas.js';

window.onload = function() {
  cargarTeslas()
  initMapBfs();
  initMapAStar();
};

document.addEventListener("DOMContentLoaded", function () {
  const sliderContainer = document.getElementById("slider-container");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  let indice = 0;

  function updateSlider() {
      sliderContainer.style.transform = `translateX(-${indice * 100}%)`;
  }

  nextBtn.addEventListener("click", function () {
      if (indice < 1) {  // Número total de secciones - 1
        indice++;
          updateSlider();
      }
  });

  prevBtn.addEventListener("click", function () {
      if (indice > 0) {
        indice--;
          updateSlider();
      }
  });
});