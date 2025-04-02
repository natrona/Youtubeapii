from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Rota para conversão de vídeo do YouTube em áudio
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    try:
        # Captura a URL do vídeo do YouTube
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'url' not in data:
                return jsonify({"error": "Nenhuma URL enviada"}), 400
            video_url = data['url']
        else:  # Método GET (para testar no navegador)
            video_url = request.args.get('url')
            if not video_url:
                return jsonify({"error": "Nenhuma URL fornecida"}), 400
        
        # Verifica se a URL do YouTube é válida
        if "youtube.com/watch?v=" not in video_url and "youtu.be/" not in video_url:
            return jsonify({"error": "URL inválida, insira um link válido do YouTube"}), 400

        # Extrai o ID do vídeo
        video_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]

        # Faz requisição para a API do Piped
        piped_api_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
        response = requests.get(piped_api_url)

        if response.status_code != 200:
            return jsonify({"error": "Falha ao obter dados do vídeo"}), 500

        # Obtém o primeiro link de áudio disponível
        data = response.json()
        if "audioStreams" not in data or not data["audioStreams"]:
            return jsonify({"error": "Nenhum áudio disponível para este vídeo"}), 404
        
        audio_url = data["audioStreams"][0]["url"]

        return jsonify({
            "audioUrl": audio_url,
            "quality": data["audioStreams"][0].get("bitrate", "128kbps")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
