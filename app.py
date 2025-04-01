import os
import yt_dlp
from flask import Flask, request, jsonify
from urllib.parse import unquote

app = Flask(__name__)

# Configurações do yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',  # Remove a pasta downloads/
    'quiet': True,
}

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL não fornecida"}), 400

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)  # Não baixa ainda
            filename = f"{info['title']}.mp3"
            
            # Pega a URL direta do áudio
            audio_url = None
            for format in info['formats']:
                if format.get('acodec') != 'none' and format.get('vcodec') == 'none':
                    audio_url = format['url']
                    break

            if not audio_url:
                return jsonify({"error": "Não foi possível extrair o áudio"}), 500

            return jsonify({
                "message": "Sucesso",
                "audioUrl": audio_url,  # Agora compatível com seu bot
                "filename": filename
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
