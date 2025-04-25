import os
import json
import requests
from collections import Counter
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from gpt4free_handler import perguntar_furia
from hltv_scraper import (
    buscar_proximo_jogo_furia,
    buscar_elenco_furia_cs2,
    buscar_live_score_furia
)

# ─── Carrega variáveis de ambiente ───────────────────────────────
load_dotenv()
TWITCH_CLIENT_ID     = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

app = Flask(__name__)
CORS(app)

def grava_analytics(tipo: str):
    """Adiciona um evento de analytics no logs/analytics.json."""
    os.makedirs("logs", exist_ok=True)
    try:
        ana = json.load(open("logs/analytics.json", encoding="utf-8"))
    except:
        ana = []
    ana.append({"tipo": tipo, "timestamp": datetime.utcnow().isoformat() + "Z"})
    json.dump(ana,
              open("logs/analytics.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

# ─── scraping das notícias via Google News ────────────────────────
def buscar_noticias_furia():
    grava_analytics("noticias")
    url = ("https://news.google.com/search?"
           "q=furia%20esports&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        artigos = soup.select('article h3 a') or soup.select('article a')
        noticias = []
        for a in artigos:
            titulo = a.get_text(strip=True)
            href   = a.get('href','')
            if not titulo: continue
            link = href
            if href.startswith('./'):
                link = "https://news.google.com" + href[1:]
            noticias.append((titulo, link))
            if len(noticias) >= 5:
                break
        if not noticias:
            return "<p>🗞️ Ainda não encontrei notícias da FURIA. Tente mais tarde!</p>"
        itens = "".join(
            f'<li><a href="{link}" target="_blank">{titulo}</a></li>'
            for titulo, link in noticias
        )
        return f'🗞️ <strong>Últimas notícias da FURIA</strong>:<ul>{itens}</ul>'
    except Exception:
        grava_analytics("noticias-error")
        return "<p>🗞️ Erro ao buscar notícias. Tente novamente mais tarde.</p>"

# ─── rotas principais ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data      = request.get_json()
    historico = data.get('historico', [])
    resposta  = perguntar_furia(historico)

    # grava log de mensagens
    os.makedirs("logs", exist_ok=True)
    try:
        logs = json.load(open("logs/mensagens.json", encoding="utf-8"))
    except:
        logs = []
    logs.append({"pergunta": historico[-1]["content"], "resposta": resposta})
    json.dump(logs,
              open("logs/mensagens.json","w",encoding="utf-8"),
              ensure_ascii=False, indent=2)

    return jsonify({"resposta": resposta})

@app.route('/api/proximo-jogo')
def proximo_jogo():
    try:
        resp = buscar_proximo_jogo_furia()
        grava_analytics("proximo-jogo")
        return jsonify({"resposta": resp})
    except Exception:
        grava_analytics("proximo-jogo-error")
        return jsonify({"resposta":
            "😢 Não consegui encontrar o próximo jogo da FURIA no momento. "
            "Tente novamente mais tarde!"})

@app.route('/api/elenco')
def elenco():
    try:
        resp = buscar_elenco_furia_cs2()
        grava_analytics("elenco")
        return jsonify({"resposta": resp})
    except Exception:
        grava_analytics("elenco-error")
        return jsonify({"resposta":
            "🤷‍♂️ Erro ao buscar o elenco da FURIA. Tente novamente mais tarde."})

@app.route('/api/redes-sociais')
def redes_sociais():
    grava_analytics("redes-sociais")
    html = """
<ul>
  <li><a href="https://twitter.com/FURIA"        target="_blank">Twitter</a></li>
  <li><a href="https://www.instagram.com/furiagg/"target="_blank">Instagram</a></li>
  <li><a href="https://www.facebook.com/furiagg"  target="_blank">Facebook</a></li>
  <li><a href="https://www.youtube.com/furiagg"   target="_blank">YouTube</a></li>
  <li><a href="https://www.tiktok.com/@furia"     target="_blank">TikTok</a></li>
</ul>
"""
    return jsonify({"resposta": html})

@app.route('/api/noticias')
def noticias():
    return jsonify({"resposta": buscar_noticias_furia()})

@app.route('/api/live-score')
def live_score():
    try:
        resp = buscar_live_score_furia()
        grava_analytics("live-score")
        return jsonify({"resposta": resp})
    except Exception:
        grava_analytics("live-score-error")
        return jsonify({"resposta":
            "🎮 Nenhum jogo ao vivo no momento ou erro ao buscar live score."})

# ─── rota de streaming via Twitch ───────────────────────────────────
@app.route('/api/streaming')
def streaming():
    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        return jsonify({"resposta":
            "❌ Configuração Twitch ausente. Defina TWITCH_CLIENT_ID e "
            "TWITCH_CLIENT_SECRET no .env"}), 500

    # obtém token OAuth
    token_url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id":     TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type":    "client_credentials"
    }
    try:
        tk = requests.post(token_url, params=params, timeout=10)
        tk.raise_for_status()
        access_token = tk.json().get("access_token")
    except Exception as e:
        grava_analytics("streaming-error")
        return jsonify({"resposta":
            f"❌ Erro ao obter token Twitch: {e}"}), 400

    headers = {
        "Client-ID":     TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    try:
        r = requests.get(
            "https://api.twitch.tv/helix/streams",
            headers=headers,
            params={"user_login": "furia"},
            timeout=10
        )
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            grava_analytics("streaming-off")
            return jsonify({"resposta":
                "🚫 FURIA não está ao vivo no momento."})
        s = data[0]
        title   = s.get("title")
        viewers = s.get("viewer_count")
        html = (
            f"🔴 FURIA AO VIVO!\n"
            f"🎙️ {title}\n"
            f"👥 {viewers} espectadores\n"
            f"<a href='https://www.twitch.tv/furiatv' target='_blank'>"
            "Ver na Twitch</a>"
        )
        grava_analytics("streaming-on")
        return jsonify({"resposta": html})
    except Exception as e:
        grava_analytics("streaming-error")
        return jsonify({"resposta":
            f"❌ Erro ao buscar streaming: {e}"}), 400

# ─── analytics de frontend (POST via fetch /api/analytics) ──────────
@app.route('/api/analytics', methods=['POST'])
def analytics():
    data = request.get_json()
    grava_analytics(data.get("tipo", "unknown"))
    return jsonify({"status": "ok"})

@app.route('/api/analytics/data')
def analytics_data():
    try:
        ana = json.load(open("logs/analytics.json", encoding="utf-8"))
    except:
        ana = []
    counts = Counter(e.get("tipo") for e in ana if "tipo" in e)
    hours  = [0]*24
    for e in ana:
        ts = e.get("timestamp","")
        try:
            dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
            hours[dt.hour] += 1
        except:
            pass
    return jsonify({"counts": counts, "hourly": hours})

# ─── painel de logs de mensagens ────────────────────────────────────
@app.route('/admin')
def admin():
    try:
        logs = json.load(open("logs/mensagens.json", encoding="utf-8"))
    except:
        logs = []
    return render_template('admin.html', logs=logs)

# ─── painel de analytics ─────────────────────────────────────────────
@app.route('/admin/analytics')
def admin_analytics():
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
