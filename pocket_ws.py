import json
import logging
import websocket
import threading
import time
import pandas as pd

logger = logging.getLogger(__name__)

class PocketOptionWS:
    def __init__(self, ssid: str):
        self.ssid = ssid
        self.ws = None
        self.data_store = {}
        self.is_connected = False

    def connect(self):
        def on_message(ws, message):
            if message.startswith("42"):
                try:
                    data = json.loads(message[2:])
                    # Extraction et stockage du flux de bougies
                    if data[0] == "updateStream":
                        asset = data[1]["asset"]
                        candles = data[1]["data"]
                        self.data_store[asset] = pd.DataFrame(candles)
                except Exception as e:
                    logger.error(f"Erreur de traitement message WS: {e}")

        def on_open(ws):
            logger.info("Connexion WebSocket établie. Authentification...")
            auth_payload = f'42["auth", {{"session": "{self.ssid}", "isDemo": 1}}]'
            ws.send(auth_payload)
            self.is_connected = True

        def on_close(ws, close_status_code, close_msg):
            logger.warning("Connexion WebSocket fermée.")
            self.is_connected = False

        self.ws = websocket.WebSocketApp(
            "wss://api-fin.po.trade/socket.io/?EIO=4&transport=websocket",
            on_message=on_message,
            on_open=on_open,
            on_close=on_close
        )
        
        wsthread = threading.Thread(target=self.ws.run_forever)
        wsthread.daemon = True
        wsthread.start()

    def get_candles(self, asset: str) -> pd.DataFrame:
        return self.data_store.get(asset, pd.DataFrame())
