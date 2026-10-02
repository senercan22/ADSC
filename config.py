
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "varsayilan-gizli-anahtar")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///smartlead.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Modül A Gereksinimleri:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Dashboard girişi (Render'da ortam değişkeni olarak değiştirilebilir)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")

    # Yapay zekanın kişiliğini tanımlayan metin (İşletmenize göre güncelleyebilirsiniz)
    BUSINESS_CONTEXT = os.getenv(
        "BUSINESS_CONTEXT",
        "Sen SmartLead AI sisteminin kurumsal ve yardımsever müşteri asistanısın. "
        "Kullanıcılara hizmetlerimiz hakkında net, profesyonel ve Türkçe yanıtlar verirsin."
    )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig
}
