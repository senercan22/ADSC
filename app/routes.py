"""
Modül D — Rotalar
İstekleri karşılar, doğrular ve doğru katmana yönlendirir.
Burada SQL veya yapay zekâ kodu YOKTUR; sadece içe aktarılan fonksiyonlar çağrılır.
"""
import re

from flask import Blueprint, jsonify, render_template, request

from app.auth import bilgiler_dogru_mu, giris_gerekli, token_uret
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service

main_bp = Blueprint("main", __name__)   # Sayfalar
api_bp = Blueprint("api", __name__)     # JSON API (/api önekiyle kaydedilir)

EMAIL_DESENI = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------- Sayfalar ----------------

@main_bp.route("/", methods=["GET"])
def index():
    """Karşılama sayfası."""
    return render_template("index.html")


@main_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """Yönetim paneli. Veriler sayfaya giriş yapıldıktan sonra /api/leads'ten çekilir."""
    return render_template("dashboard.html")


# ---------------- API ----------------

@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    """Ziyaretçi mesajını yapay zekâ servisine iletir."""
    data = request.get_json(silent=True) or {}
    mesaj = (data.get("mesaj") or "").strip()
    gecmis = data.get("gecmis") or []

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj boş olamaz."}), 400
    if len(mesaj) > 1000:
        return jsonify({"basari": False, "hata": "Mesaj çok uzun."}), 400

    # Geçmişi sadece beklenen biçimdeki son 10 mesajla sınırla
    if not isinstance(gecmis, list):
        gecmis = []
    gecmis = [
        {"role": m["role"], "content": str(m["content"])[:1000]}
        for m in gecmis[-10:]
        if isinstance(m, dict) and m.get("role") in ("user", "assistant") and m.get("content")
    ]

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200
    except AIServiceError:
        return jsonify({"basari": False, "hata": "Asistan şu an yanıt veremiyor, lütfen biraz sonra tekrar deneyin."}), 503


@api_bp.route("/leads", methods=["POST"])
def lead_kaydet():
    """Formdan gelen ad soyad, e-posta ve geri bildirimi kaydeder."""
    data = request.get_json(silent=True) or {}
    isim = (data.get("isim") or "").strip()
    email = (data.get("email") or "").strip()
    mesaj = (data.get("mesaj") or "").strip()

    if not isim or not email:
        return jsonify({"basari": False, "hata": "Ad soyad ve e-posta zorunludur."}), 400
    if not EMAIL_DESENI.match(email):
        return jsonify({"basari": False, "hata": "Geçerli bir e-posta adresi girin."}), 400
    if len(isim) > 100 or len(email) > 200 or len(mesaj) > 2000:
        return jsonify({"basari": False, "hata": "Alanlardan biri çok uzun."}), 400

    try:
        yeni_id = lead_ekle(isim, email, mesaj)
        return jsonify({"basari": True, "id": yeni_id}), 201
    except Exception:
        return jsonify({"basari": False, "hata": "Kayıt sırasında bir hata oluştu."}), 500


@api_bp.route("/leads", methods=["GET"])
@giris_gerekli
def lead_listesi():
    """Tüm kayıtları döndürür. Sadece giriş yapmış yönetici görebilir."""
    try:
        return jsonify({"basari": True, "leads": tum_leadler()}), 200
    except Exception:
        return jsonify({"basari": False, "hata": "Kayıtlar okunamadı."}), 500


@api_bp.route("/login", methods=["POST"])
def giris():
    """Yönetici girişi: bilgiler doğruysa panelin kullanacağı token'ı döndürür."""
    data = request.get_json(silent=True) or {}
    kullanici = data.get("kullanici") or ""
    sifre = data.get("sifre") or ""

    if not bilgiler_dogru_mu(kullanici, sifre):
        return jsonify({"basari": False, "hata": "Kullanıcı adı veya şifre hatalı."}), 401
    return jsonify({"basari": True, "token": token_uret()}), 200
