const palabras = ['estilo', 'belleza', 'cuidado'];
let indice = 0;
const h1 = document.getElementById('titulo');

setInterval(() => {
  indice = (indice + 1) % palabras.length;
  h1.textContent = `Reserva Tu ${palabras[indice]}`;
}, 2500); // Cambia cada 2.5 segundos