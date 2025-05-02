# FURIA Chatbot - Desafio FURIA Tech

### Projeto funcional desenvolvido para o desafio técnico da FURIA

---

## 🔖 Visão Geral

O **FURIA Chatbot** é uma aplicação web interativa, criada para proporcionar uma experiência real de torcedor com a FURIA, focando especialmente no time de CS2. Desenvolvido em **Python (Flask)** com frontend responsivo em **HTML, CSS e JS**, o bot permite acompanhar notícias, próximos jogos, escalação, live scores e transmissões ao vivo. O sistema também conta com um painel administrativo com logs e métricas em tempo real.

---

## 📊 Funcionalidades

### 📞 Chatbot interativo

* Envia mensagens simulando conversa com torcedor
* Integração com GPT (via gpt4free)

### 🌟 Consulta de Dados em Tempo Real

* 🎮 Próximos jogos da FURIA (via HLTV/Liquipedia)
* 🎥 Live score ao vivo com notificação push
* 🎙️ Streaming ao vivo via Twitch API
* 📰 Notícias recentes via Google News
* 👥 Elenco atual com scraping do Liquipedia

### 📊 Dashboard Administrativo

* Logs de conversa completos em `/admin`
* Métricas e gráficos em `/admin/analytics`

  * Volume de uso por rota (chat, noticias, live-score...)
  * Horários de pico de uso
  * Registros de erro (por exemplo, scraping falhou)

---

## ⚙️ Como Rodar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/leoouu/furia-chatbot
cd furia-chatbot
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure seu `.env` com credenciais da Twitch:

```env
TWITCH_CLIENT_ID=seu_id\TWITCH_CLIENT_SECRET=sua_secret
```

4. Inicie o servidor Flask:

```bash
python app.py
```

5. Acesse:

```
http://localhost:5000
```

---

## 💻 Tecnologias Utilizadas

* **Backend:** Python 3.11, Flask, Flask-CORS
* **Frontend:** HTML5, CSS3, JavaScript
* **Scraping/API:** BeautifulSoup, requests, Twitch API, Google News scraping
* **Dashboard:** Chart.js
* **Infraestrutura:** Deploy via Render.com

---

## 👤 Desenvolvido por Leonardo Gonçalves

Desafio FURIA Tech 2025

[LinkedIn](https://www.linkedin.com/in/leonardogonc) | [GitHub](https://github.com/leoouu) 
