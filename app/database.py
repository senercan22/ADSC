import sqlite3
from flask import g

DATABASE = "smartlead.db"

def get_db():
    """Veritabanı bağlantısı oluşturur ve satırlara sütun adıyla erişim sağlar."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception=None):
    """İstek bittiğinde veritabanı bağlantısını kapatır."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db(app):
    """'leads' tablosunu otomatik oluşturur (yoksa)."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                email TEXT NOT NULL,
                mesaj TEXT NOT NULL,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

def feedback_ekle(ad, soyad, email, mesaj):
    """Yeni geri bildirim kaydı ekler."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO feedback (ad, soyad, email, mesaj) VALUES (?, ?, ?, ?)",
        (ad, soyad, email, mesaj)
    )
    db.commit()
    return cursor.lastrowid

def tum_feedbackler():
    """Tüm geri bildirimleri en yeniden eskiye listeler."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, ad, soyad, email, mesaj, tarih FROM feedback ORDER BY id DESC")
    return [dict(row) for row in cursor.fetchall()]

def lead_ekle(isim, telefon, mesaj=""):
    """Güvenli SQL yer tutucusu (?) kullanarak yeni kayıt ekler."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    db.commit()
    return cursor.lastrowid

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye doğru listeler."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
