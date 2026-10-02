# SmartLead AI — ADSC Creative

Ziyaretçilerle yapay zekâ üzerinden sohbet eden ve iletişim bilgilerini (ad soyad, e-posta, geri bildirim) toplayan sistem. İki arayüzden oluşur: Wix Velo ile yapılmış bir karşılama sayfası ve şifreyle korunan bir yönetim paneli.

**Teknolojiler:** Python, Flask, SQLite, Groq API (llama-3.1-8b-instant), Wix Velo, Render

## Mimari

```
run.py                  Giriş noktası
config.py               Tüm ayarlar (.env'den okunur)
app/__init__.py         create_app(): ayarlar → CORS → veritabanı → blueprint'ler, /health
app/database.py         SQL kodunun TAMAMI (leads tablosu)
app/services/ai_service.py  Yapay zekâ çağrılarının TAMAMI
app/auth.py             Yönetici girişi ve token doğrulama
app/routes.py           Sadece istek karşılama ve yönlendirme (SQL / AI kodu yok)
app/templates/          index.html, dashboard.html
wix/                    Wix Velo sayfa kodları
```

## API

| Metod + Yol | Görevi | Giriş gerekli mi? |
|---|---|---|
| GET `/health` | Sunucu canlılık kontrolü | Hayır |
| POST `/api/sohbet` | `{mesaj, gecmis}` → yapay zekâ yanıtı | Hayır |
| POST `/api/leads` | `{isim, email, mesaj}` kaydeder (201) | Hayır |
| GET `/api/leads` | Tüm kayıtları döndürür | **Evet** (Bearer token) |
| POST `/api/login` | `{kullanici, sifre}` → token | Hayır |

Bütün yanıtlar `basari` alanı içeren JSON'dur. Eksik veri gelirse 400, yapay zekâ hatasında 503, yetkisiz istekte 401 döner.

## Yerelde çalıştırma

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env  → değerleri doldurun
python run.py
```

Tarayıcıda `http://localhost:5000` (karşılama) ve `http://localhost:5000/dashboard` (panel).

## Render'da yayınlama

- Build: `pip install -r requirements.txt`
- Start: `gunicorn run:app`
- Environment: `SECRET_KEY`, `GROQ_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`

## Güvenlik

- SQL sorgularında `?` yer tutucusu kullanılır.
- `.env` GitHub'a yüklenmez (`.gitignore`).
- Kayıt listesi sadece giriş yapan yöneticiye açıktır; şifre Wix kodunda değil, sunucuda kontrol edilir.
