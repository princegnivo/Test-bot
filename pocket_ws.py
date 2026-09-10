import json
import logging
import threading
import time
import websocket
import pandas as pd

try:
    from ssid_fetcher import fetch_ssid
    SSID_FETCHER_AVAILABLE = True
except ImportError:
    SSID_FETCHER_AVAILABLE = False

logger = logging.getLogger(__name__)

# Liste des endpoints à essayer, dans l'ordre, en cas de coupure.
# Je n'ai pas de liste fiable d'URLs régionales alternatives pour Pocket Option -
# ajoute ici toute autre URL que tu identifierais via devtools (onglet Network/WS)
# si tu observes des connexions vers d'autres domaines/serveurs.
WS_ENDPOINTS = [
    "wss://api-fin.po.trade/socket.io/?EIO=4&transport=websocket",
]


class PocketOptionWS:
    def __init__(self, ssid: str, endpoints: list[str] | None = None):
        self.ssid = ssid
        self.endpoints = endpoints or WS_ENDPOINTS
        self.ws = None
        self.data_store = {}
        self.is_connected = False

        self.auth_status = None
        self._auth_event = threading.Event()

        self._should_run = False
        self._reconnect_delay = 2
        self._max_reconnect_delay = 60
        self._current_endpoint_index = 0

    def connect(self):
        self._should_run = True
        self._connect_once()

    def _connect_once(self):
        url = self.endpoints[self._current_endpoint_index % len(self.endpoints)]

        def on_message(ws, message):
            # Ping Engine.IO du serveur ("2") -> on répond pong ("3") pour garder la connexion active
            if message == "2":
                try:
                    ws.send("3")
                except Exception:
                    pass
                return

            if message.startswith("42"):
                try:
                    data = json.loads(message[2:])
                    event_name = data[0]

                    if event_name == "updateStream":
                        asset = data[1]["asset"]
                        candles = data[1]["data"]
                        self.data_store[asset] = pd.DataFrame(candles)

                    elif event_name in ("successauth", "successupdateBalance", "profile"):
                        if self.auth_status is None:
                            self.auth_status = True
                            self._auth_event.set()

                except Exception as e:
                    logger.error(f"Erreur de traitement message WS: {e}")

        def on_open(ws):
            logger.info(f"Connexion WebSocket établie sur {url}. Authentification...")
            self._reconnect_delay = 2  # reset du backoff après un succès
            auth_payload = f'42["auth", {{"session": "{self.ssid}", "isDemo": 1}}]'
            ws.send(auth_payload)
            self.is_connected = True
            self._start_keepalive(ws)

        def on_close(ws, close_status_code, close_msg):
            logger.warning(f"Connexion WebSocket fermée ({close_status_code}): {close_msg}")
            self.is_connected = False
            if self.auth_status is None:
                self.auth_status = False
                self._auth_event.set()
            self._schedule_reconnect()

        def on_error(ws, error):
            logger.error(f"Erreur WebSocket: {error}")
            if self.auth_status is None:
                self.auth_status = False
                self._auth_event.set()

        self.ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error
        )

        wsthread = threading.Thread(target=self.ws.run_forever, kwargs={"ping_interval": 0})
        wsthread.daemon = True
        wsthread.start()

    def _start_keepalive(self, ws):
        """Envoie un ping applicatif toutes les 25s pour éviter les coupures pour inactivité."""
        def keepalive_loop():
            while self.is_connected and self._should_run:
                time.sleep(25)
                if not self.is_connected:
                    break
                try:
                    ws.send("2")
                except Exception as e:
                    logger.warning(f"Échec du ping de maintien de connexion: {e}")
                    break

        t = threading.Thread(target=keepalive_loop)
        t.daemon = True
        t.start()

    def _schedule_reconnect(self):
        if not self._should_run:
            return
        # Bascule sur l'endpoint suivant de la liste (repli multirégional)
        self._current_endpoint_index += 1
        delay = self._reconnect_delay
        next_url = self.endpoints[self._current_endpoint_index % len(self.endpoints)]
        logger.info(f"Reconnexion dans {delay}s (prochain essai sur {next_url})...")
        threading.Timer(delay, self._connect_once).start()
        self._reconnect_delay = min(self._reconnect_delay * 2, self._max_reconnect_delay)

    def disconnect(self):
        self._should_run = False
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass

    def check_ssid_valid(self, timeout: int = 10) -> bool:
        self.auth_status = None
        self._auth_event.clear()

        if not self.is_connected:
            self.connect()
        else:
            try:
                self.ws.close()
            except Exception:
                pass
            self._connect_once()

        confirmed = self._auth_event.wait(timeout)
        if not confirmed:
            return False
        return bool(self.auth_status)

    def try_refresh_ssid(self, email: str, password: str) -> bool:
        if not SSID_FETCHER_AVAILABLE:
            logger.error(
                "Rafraîchissement auto indisponible : le module ssid_fetcher "
                "(ou playwright) n'est pas installé dans cet environnement."
            )
            return False

        logger.info("Tentative de rafraîchissement automatique du SSID...")
        new_ssid = fetch_ssid(email, password)
        if not new_ssid:
            logger.error("Échec de la récupération automatique du SSID.")
            return False
        self.ssid = new_ssid
        return self.check_ssid_valid(timeout=10)

    def get_candles(self, asset: str) -> pd.DataFrame:
        return self.data_store.get(asset, pd.DataFrame())
                                        
