from flask import Flask
from flask_cors import CORS

def create_app(config_name="default"): # Tek değiştirdiğimiz yer burası
    app = Flask(__name__)

    CORS(app)

    # ... geri kalan kodların ...
    return app
