import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/db")
def db():
    host = os.environ.get("DB_HOST", "localhost")
    port = int(os.environ.get("DB_PORT", 5432))
    try:
        socket.create_connection((host, port), timeout=2).close()
        return jsonify(db="reachable", host=host, port=port)
    except OSError as e:
        app.logger.error("Connexion a %s:%s impossible : %s", host, port, e)
        return jsonify(db="unreachable", host=host, port=port, error=str(e)), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
