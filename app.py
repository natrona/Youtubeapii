import os
import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Cria a pasta se não existir

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL não fornecida"}), 400

    try:
        # Configuração do yt-dlp para baixar o áudio em MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        return jsonify({"message": "Download concluído!", "file": filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)