
function getQueryParams() {
    const params = {};
    window.location.search.substring(1).split('&').forEach(pair => {
      if(pair) {
        const [key, value] = pair.split('=');
        params[decodeURIComponent(key)] = decodeURIComponent(value || '');
      }
    });
    return params;
  }

  const params = getQueryParams();

  if(params.nombre && params.fecha) {
    document.getElementById('mensaje').textContent =
      `Gracias ${params.nombre}, tu agenda está reservada para el día ${params.fecha}. Por favor revisa Google Calendar.`;
  }