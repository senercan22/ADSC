"""
Modül C — Yapay zekâ servisi
Projedeki TÜM yapay zekâ çağrıları yalnızca bu dosyadadır.
Bu dosya Flask, HTTP rotaları veya veritabanı hakkında hiçbir şey bilmez.
"""
import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisine özel hata sınıfı."""
    pass


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _sistem_talimati(self):
        """Asistanın kişiliğini config'teki BUSINESS_CONTEXT'ten okur."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Mesajı (ve varsa önceki konuşmayı) Groq'a gönderip yanıt metnini döndürür."""
        if gecmis is None:
            gecmis = []

        # Anahtar yoksa çökmek yerine demo yanıtı ver
        if not self.api_key:
            return "Demo modu: Groq API anahtarı ayarlanmadığı için bu otomatik bir yanıttır."

        # Sıra önemli: sistem talimatı → geçmiş mesajlar → yeni kullanıcı mesajı
        messages = [{"role": "system", "content": self._sistem_talimati()}]
        messages.extend(gecmis)
        messages.append({"role": "user", "content": mesaj})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": messages, "temperature": 0.7}

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=20)
        except requests.RequestException as e:
            raise AIServiceError(f"Groq'a bağlanılamadı: {e}")

        if response.status_code != 200:
            raise AIServiceError(f"Groq API hatası: {response.status_code} - {response.text[:200]}")

        try:
            return response.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError):
            raise AIServiceError("Groq'tan beklenmeyen biçimde yanıt geldi.")


# Uygulama boyunca kullanılacak tek örnek
ai_service = AIService()
