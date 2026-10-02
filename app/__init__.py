"""
Modül E — Uygulama fabrikası
Ayarlar → CORS → veritabanı → blueprint'ler sırasıyla birleştirilir.
"""
from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import close_connection, init_db


def create_app(config_name="default"):
    app = Flask(__name__)

    # 1) Ayarları yükle
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # 2) CORS: Wix sitesinin /api adreslerine istek atabilmesi için
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # 3) Veritabanı tablosunu hazırla, her istek sonunda bağlantıyı kapat
    init_db(app)
    app.teardown_appcontext(close_connection)

    # 4) Blueprint'leri kaydet
    from app.routes import api_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Sunucu canlılık kontrolü (Render ve Wix "uyandırma" için)
    @app.route("/health")
    def health():
        return jsonify({"basari": True, "durum": "aktif"}), 200

    # Bilinmeyen adres veya beklenmeyen hata durumunda da JSON dön
    @app.errorhandler(404)
    def bulunamadi(e):
        return jsonify({"basari": False, "hata": "Adres bulunamadı."}), 404

    @app.errorhandler(500)
    def sunucu_hatasi(e):
        return jsonify({"basari": False, "hata": "Sunucu hatası."}), 500

    return app
