from flask import Blueprint, request, jsonify

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADSC Temsilcisi</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .chat-container { width: 100%; max-width: 400px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 500px; }
            .chat-header { background: #000; color: #fff; padding: 15px; font-weight: bold; text-align: center; }
            .chat-log { flex: 1; padding: 15px; overflow-y: auto; background: #fafafa; display: flex; flex-direction: column; gap: 10px; }
            .message { padding: 10px 14px; border-radius: 10px; max-width: 80%; font-size: 14px; line-height: 1.4; }
            .user { background: #007bff; color: #fff; align-self: flex-end; }
            .bot { background: #e9ecef; color: #333; align-self: flex-start; }
            .chat-input-area { display: flex; padding: 10px; background: #fff; border-top: 1px solid #ddd; }
            .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px; outline: none; font-size: 14px; }
            .chat-input-area button { background: #000; color: #fff; border: none; padding: 0 18px; margin-left: 8px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        </style>
    </head>
    <body>
    <div class="chat-container">
        <div class="chat-header">ADSC Temsilcisi</div>
        <div id="chatLog" class="chat-log">
            <div class="message bot">Merhaba! Size nasıl yardımcı olabilirim?</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="userMsg" placeholder="Mesajınızı yazın..." onkeypress="if(event.key==='Enter') sendMsg()" />
            <button onclick="sendMsg()" id="sendBtn">Gönder</button>
        </div>
    </div>
    <script>
        async function sendMsg() {
            const input = document.getElementById("userMsg");
            const log = document.getElementById("chatLog");
            const btn = document.getElementById("sendBtn");
            const text = input.value.trim();
            if (!text) return;
            log.innerHTML += `<div class="message user">${text}</div>`;
            input.value = "";
            log.scrollTop = log.scrollHeight;
            btn.innerText = "...";
            btn.disabled = true;
            try {
                const res = await fetch("https://smartlead-ai-l25b.onrender.com/api/sohbet", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ mesaj: text })
                });
                const data = await res.json();
                if (data.basari) {
                    log.innerHTML += `<div class="message bot">${data.cevap}</div>`;
                } else {
                    log.innerHTML += `<div class="message bot" style="color:red;">Hata: ${data.hata}</div>`;
                }
            } catch (e) {
                log.innerHTML += `<div class="message bot" style="color:red;">Bağlantı hatası!</div>`;
            } finally {
                btn.innerText = "Gönder";
                btn.disabled = false;
                log.scrollTop = log.scrollHeight;
            }
        }
    </script>
    </body>
    </html>
    """

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/chat', methods=['POST', 'OPTIONS'])
def sohbet():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    try:
        data = request.get_json(silent=True) or {}
        # Wix tarafında 'message' gönderdiğimiz için ikisini de yakalayacak şekilde ayarlıyoruz
        kullanici_mesaji = (data.get('message') or data.get('mesaj') or '').lower().strip()

        if not kullanici_mesaji:
            return jsonify({'basari': False, 'hata': 'Mesaj boş olamaz'}), 400

        # ADSC Creative Akıllı Yanıt Mantığı
        if any(kelime in kullanici_mesaji for kelime in ['hizmet', 'ne yapıyorsunuz', 'hizmetleriniz', 'ajans']):
            cevap = "ADSC Creative olarak markanızı dijital dünyada öne taşımak için; yaratıcı reklam kampanyaları, marka kimliği tasarımı, web geliştirme ve dijital pazarlama çözümleri sunuyoruz."
        elif any(kelime in kullanici_mesaji for kelime in ['iletişim', 'ulaş', 'telefon', 'mail', 'adres', 'teklif']):
            cevap = "Bizimle iletişime geçmek ve projeniz için teklif almak adına sitemizin üst kısmındaki 'Share Your Idea' butonunu kullanabilir veya doğrudan iletişim sayfamızdan bize yazabilirsiniz!"
        elif any(kelime in kullanici_mesaji for kelime in ['merhaba', 'selam', 'hey', 'iyi günler']):
            cevap = "Merhaba! Ben ADSC Temsilcisi. Size ajansımız ve hizmetlerimiz hakkında nasıl yardımcı olabilirim?"
        elif any(kelime in kullanici_mesaji for kelime in ['kimsin', 'sen kimsin', 'adsc']):
            cevap = "Ben ADSC Creative'in resmi yapay zeka temsilcisiyim. Markanızın yaratıcı süreçlerinde size rehberlik etmek için buradayım."
        else:
            cevap = f"ADSC Temsilcisi: '{kullanici_mesaji}' ile ilgili detaylı bilgiyi ekibimizle görüşerek öğrenebilirsiniz. Size başka nasıl yardımcı olabilirim?"

        # Wix tarafı doğrudan data.reply beklediği için her iki formatı da destekleyelim
        response = jsonify({'basari': True, 'cevap': cevap, 'reply': cevap})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        response = jsonify({'basari': False, 'hata': str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500
