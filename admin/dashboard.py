import json
from flask import Blueprint, render_template
from collections import Counter

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    try:
        with open("logs/mensagens.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = []

    perguntas = [msg['pergunta'] for msg in dados]
    respostas = [msg['resposta'] for msg in dados]

    contagem = Counter(perguntas).most_common(5)

    return render_template("dashboard.html", total=len(dados), mais_comuns=contagem)
