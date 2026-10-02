"""
Modül B — Veritabanı
Projedeki TÜM SQL kodu yalnızca bu dosyadadır.
"""
import sqlite3
from flask import current_app, g


def get_db():
    """İstek boyunca tek bir bağlantı açar; satırlara sütun adıyla erişim sağlar."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_URL"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_connection(exception=None):
    """İstek bittiğinde bağlantıyı kapatır (create_app içinde teardown olarak kayıtlı)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """'leads' tablosunu yoksa oluşturur."""
    with app.app_context():
        db = get_db()
        # Kişiselleştirme: yönergedeki 'telefon' yerine 'email' kullanıyoruz,
        # 'mesaj' ise ziyaretçinin geri bildirimi (feedback).
        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                isim   TEXT NOT NULL,
                email  TEXT NOT NULL,
                mesaj  TEXT,
                tarih  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()


def lead_ekle(isim, email, mesaj=""):
    """Yeni kayıt ekler. Değerler '?' yer tutucusuyla verilir (SQL Injection koruması)."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO leads (isim, email, mesaj) VALUES (?, ?, ?)",
        (isim, email, mesaj),
    )
    db.commit()
    return cursor.lastrowid


def tum_leadler():
    """Tüm kayıtları en yeniden eskiye doğru sözlük listesi olarak döndürür."""
    db = get_db()
    rows = db.execute(
        "SELECT id, isim, email, mesaj, tarih FROM leads ORDER BY id DESC"
    ).fetchall()
    return [dict(row) for row in rows]
