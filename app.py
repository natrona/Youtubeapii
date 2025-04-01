from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Pega a URL do vídeo enviada pelo seu bot
        video_url = request.json.get('url')
        
        # Usa a API do Piped (alternativa ao YouTube)
        response = requests.get(
            f"https://pipedapi.kavin.rocks/streams/{video_url.split('v=')[1].split('&')[0]}"
        )
        
        audio_url = response.json()['audioStreams'][0]['url']
        
        return jsonify({
            "audioUrl": audio_url,  # ← Seu bot já espera esse formato!
            "quality": "128kbps"    # Opcional
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
