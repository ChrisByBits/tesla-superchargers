export const teslas = [
  { modelo: "Model S", capacidad: 75, consumoPorKm: 0.2, imagen: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/2018_Tesla_Model_S_75D.jpg/1200px-2018_Tesla_Model_S_75D.jpg" },
  { modelo: "Model S Plaid", capacidad: 100, consumoPorKm: 0.18, imagen: "https://acnews.blob.core.windows.net/imgnews/medium/NAZ_9033697867ef401d99b1b419faf37ffa.jpg" },
  { modelo: "Model X", capacidad: 75, consumoPorKm: 0.19, imagen: "https://hips.hearstapps.com/hmg-prod/images/2020-tesla-model-x-123-656e3825810bc.jpg?crop=0.345xw:0.413xh;0.324xw,0.303xh&resize=768:*" },
  { modelo: "Model X Plaid", capacidad: 100, consumoPorKm: 0.2, imagen: "https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/inno5xbcnmct5gl4xdgn.jpg" },
  { modelo: "Tesla Model 3", capacidad: 82, consumoPorKm: 0.16, imagen: "https://hips.hearstapps.com/hmg-prod/images/2024-tesla-model-3-long-range-rwd-132-66feb663ecf17.jpg?crop=0.702xw:0.592xh;0.143xw,0.391xh&resize=1200:*" },
  { modelo: "Tesla Model Y", capacidad: 82, consumoPorKm: 0.17, imagen: "https://www.shop4tesla.com/cdn/shop/articles/tesla-model-y-bleibt-meistverkauftes-elektroauto-in-deutschland-2024-874608.jpg?v=1726029361" },
]

export function cargarTeslas() {
  const selectTesla = document.getElementById("tesla-select");

  teslas.forEach((tesla, index) => {
    const option = document.createElement("option");
    option.value = index;
    option.textContent = tesla.modelo;
    selectTesla.appendChild(option);
  });

  selectTesla.addEventListener("change", () => {
    const teslaSeleccionado = selectTesla.value;
    if (teslaSeleccionado !== "") {
      const tesla = teslas[teslaSeleccionado];  

      const imagenDiv = document.getElementById("tesla-imagen");
      imagenDiv.innerHTML = `<img src="${tesla.imagen}" alt="${tesla.modelo}" style="width: 800px; margin-bottom: 10px;">`;
    } else {
      document.getElementById("tesla-imagen").innerHTML = "";
    }
  });
}
