"""
Yönetim paneli girişi.
Kimlik doğrulama mantığı burada; routes.py yalnızca bu fonksiyonları çağırır.
Şifre doğruysa süreli ve imzalı bir token verilir; /api/leads bu token olmadan veri vermez.
"""
import hmac
from functools import wraps

from flask import current_app, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

TOKEN_SURESI = 8 * 60 * 60  # saniye (8 saat)


def _serializer():
    # Token, config'teki SECRET_KEY ile imzalanır; anahtarı bilmeyen sahte token üretemez
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="admin-giris")


def bilgiler_dogru_mu(kullanici, sifre):
    """Kullanıcı adı ve şifreyi config'teki değerlerle karşılaştırır."""
    # compare_digest: karşılaştırma süresinden şifre tahmin edilmesini engeller
    return (
        hmac.compare_digest(kullanici, current_app.config["ADMIN_USERNAME"])
        and hmac.compare_digest(sifre, current_app.config["ADMIN_PASSWORD"])
    )


def token_uret():
    return _serializer().dumps({"admin": True})


def giris_gerekli(view):
    """'Authorization: Bearer <token>' başlığı geçerli değilse 401 döndürür."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        baslik = request.headers.get("Authorization", "")
        token = baslik[7:] if baslik.startswith("Bearer ") else ""
        try:
            _serializer().loads(token, max_age=TOKEN_SURESI)
        except (BadSignature, SignatureExpired):
            return jsonify({"basari": False, "hata": "Bu veriyi görmek için giriş yapmalısınız."}), 401
        return view(*args, **kwargs)
    return wrapper
