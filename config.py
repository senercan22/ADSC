"""
Modül A — Yapılandırma
Tüm ayarlar ve gizli anahtarlar burada toplanır; değerler .env dosyasından okunur.
"""
import os
from dotenv import load_dotenv

# .env dosyasını ortam değişkenlerine yükle (bu satır olmazsa .env okunmaz)
load_dotenv()


class Config:
    # Flask oturum/token imzalama anahtarı
    SECRET_KEY = os.environ.get("SECRET_KEY", "gelistirme-icin-gizli-anahtar")

    # SQLite veritabanı dosyasının yolu
    DATABASE_URL = os.environ.get("DATABASE_URL", "smartlead.db")

    # Yapay zekâ ayarları
    # strip(): kopyala-yapıştırda gelen boşluk / tırnak karakterlerini temizler
    GROQ_API_KEY = (os.environ.get("GROQ_API_KEY") or "").strip().strip("\"'").strip()
    # Groq bir modeli kaldırırsa koda dokunmadan Render'dan değiştirilebilir
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    # Hangi sitelerin API'ye istek atabileceği (Wix sitesi dahil)
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # Yönetim paneli girişi (canlıda Render ortam değişkenlerinden değiştirin)
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "1234")

    # Yapay zekânın kişiliği — projeyi kendi işimize uyarladığımız TEK yer
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        "Sen ADSC Creative reklam ajansının dijital temsilcisisin. "
        "Ajansın hizmetleri: yaratıcı reklam kampanyaları, marka kimliği tasarımı, "
        "web geliştirme ve dijital pazarlama. Kısa, samimi ve profesyonel Türkçe yanıtlar ver. "
        "Bilmediğin konularda uydurma; ziyaretçiyi sayfadaki formdan ad soyad, e-posta "
        "ve mesajını bırakmaya yönlendir, ekibin kendisine dönüş yapacağını söyle."
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# create_app() bu sözlükten ortamı seçer
config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
}
