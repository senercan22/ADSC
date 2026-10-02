"""Giriş noktası: yerelde `python run.py`, Render'da `gunicorn run:app`."""
import os

from app import create_app

app = create_app(os.environ.get("FLASK_ENV_NAME", "default"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
