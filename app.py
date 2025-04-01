from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        video_url = request.json.get('url')
        if not video_url:
            return jsonify({"error": "URL não fornecida"}), 400

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            for fmt in info['formats']:
                if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                    return jsonify({
                        "audioUrl": fmt['url'],
                        "filename": f"{info['title']}.mp3"
                    })

        return jsonify({"error": "Nenhum formato de áudio encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
