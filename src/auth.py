from flask import request, jsonify
from dotenv import load_dotenv
from pathlib import Path
from functools import wraps
import os
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH,override=True)


def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        client_key = request.headers.get("x-api-key")
        server_key = os.getenv("SECRET_KEY_API")

        if not server_key:
            return jsonify({"error": "Server API key not configured"}), 500

        if not client_key:
            return jsonify({"error": "API key missing"}), 401

        if client_key != server_key:
            return jsonify({"error": "Invalid API key"}), 403

        return fn(*args, **kwargs)
    return wrapper
