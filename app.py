from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Lista de servidores Piped alternativos
PIPED_SERVERS = [
    "https://pipedapi.kavin.rocks"
]

def get_audio_url(video_id):
    """Tenta buscar o áudio do vídeo em servidores Piped ativos"""
    for server in PIPED_SERVERS:
        try:
            piped_api_url = f"{server}/streams/{video_id}"
            response = requests.get(piped_api_url, timeout=50)  # Timeout de 5 segundos
            
            if response.status_code == 200:
                data = response.json()
                if "audioStreams" in data and data["audioStreams"]:
                    return data["audioStreams"][0]["url"]  # Retorna o primeiro áudio disponível
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {server}: {e}")
    
    return None  # Retorna None se todos os servidores falharem

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    try:
        # Obtém a URL do vídeo
        video_url = request.args.get('url') if request.method == 'GET' else request.get_json().get('url')

        if not video_url:
            return jsonify({"error": "Nenhuma URL fornecida"}), 400

        # Verifica se a URL pertence ao YouTube
        if "youtube.com/watch?v=" not in video_url and "youtu.be/" not in video_url:
            return jsonify({"error": "URL inválida, insira um link válido do YouTube"}), 400

        # Extrai o ID do vídeo do YouTube
        video_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]

        # Busca o link do áudio
        audio_url = get_audio_url(video_id)

        if not audio_url:
            return jsonify({"error": "Não foi possível obter o áudio do vídeo"}), 500

        return jsonify({
            "audioUrl": audio_url,
            "quality": "128kbps"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
