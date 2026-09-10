import logging
import threading
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)


def start_ssid_server(ws_client, port: int = 8765):
    """
    Démarre un petit serveur HTTP local qui reçoit le SSID capturé par
    l'extension Kiwi Browser et met à jour la connexion du bot automatiquement.
    """
    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response):
        # Nécessaire pour que la page pocketoption.com (https) puisse envoyer
        # une requête vers ce serveur local (http://127.0.0.1).
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @app.route("/ssid", methods=["OPTIONS"])
    def ssid_options():
        return "", 204

    @app.route("/ssid", methods=["POST"])
    def receive_ssid():
        data = request.get_json(silent=True) or {}
        ssid = data.get("ssid")
        if not ssid:
            return jsonify({"status": "error", "message": "champ 'ssid' manquant"}), 400

        if ssid == ws_client.ssid and ws_client.is_connected:
            return jsonify({"status": "ok", "changed": False})

        logger.info("Nouveau SSID reçu depuis l'extension Kiwi Browser.")
        ws_client.ssid = ssid
        is_valid = ws_client.check_ssid_valid(timeout=10)
        return jsonify({"status": "ok", "changed": True, "valid": is_valid})

    def run():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    logger.info(f"Serveur de réception SSID démarré sur http://127.0.0.1:{port}/ssid")
