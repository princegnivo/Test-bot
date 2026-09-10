// Intercepte les trames WebSocket envoyées par la page pour repérer le
// message d'authentification et en extraire le SSID (session).
(function () {
  const SERVER_URL = "http://127.0.0.1:8765/ssid";
  const OriginalWebSocket = window.WebSocket;

  function patchedSend(originalSend) {
    return function (data) {
      try {
        if (typeof data === "string" && data.startsWith("42") && data.indexOf('"auth"') !== -1) {
          const match = data.match(/"session":"([^"]+)"/);
          if (match && match[1]) {
            const ssid = match[1];
            fetch(SERVER_URL, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ ssid: ssid })
            }).catch(function () {
              // Le bot n'est peut-être pas lancé, on ignore silencieusement
            });
          }
        }
      } catch (e) {
        // on ne casse jamais le fonctionnement normal du site
      }
      return originalSend.apply(this, arguments);
    };
  }

  function WrappedWebSocket(url, protocols) {
    const ws = protocols !== undefined
      ? new OriginalWebSocket(url, protocols)
      : new OriginalWebSocket(url);
    ws.send = patchedSend(ws.send.bind(ws));
    return ws;
  }
  WrappedWebSocket.prototype = OriginalWebSocket.prototype;
  window.WebSocket = WrappedWebSocket;
})();
