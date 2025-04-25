<body>
  <h1>🔥 FURIA Chatbot</h1>
  <p>Chatbot para fãs da FURIA com integração de notícias, próximos jogos, elenco e live score, tudo com scraping e IA.</p>

  <h2>⚙️ Tecnologias Utilizadas</h2>
  <ul>
    <li>Python (Flask)</li>
    <li>HTML, CSS, JavaScript (Vanilla)</li>
    <li>BeautifulSoup (Web Scraping)</li>
    <li>Chart.js (Analytics)</li>
    <li>OpenAI/GPT4Free (IA)</li>
    <li>Twitch API</li>
  </ul>

  <h2>📦 Instalação</h2>
  <ol>
    <li>Clone o repositório: <code>git clone https://github.com/leoouu/furia-chatbot</code></li>
    <li>Instale os pacotes: <code>pip install -r requirements.txt</code></li>
    <li>Crie um arquivo <code>.env</code> com:
      <pre>
TWITCH_CLIENT_ID=seu_id
TWITCH_CLIENT_SECRET=sua_secret
      </pre>
    </li>
    <li>Rode com: <code>python app.py</code></li>
    <li>Acesse <a href="http://localhost:5000">localhost:5000</a></li>
  </ol>

  <h2>💬 Funcionalidades</h2>
  <ul>
    <li>Consulta ao próximo jogo da FURIA via HLTV e Liquipedia</li>
    <li>Scraping de elenco atualizado</li>
    <li>Notícias recentes do Google News</li>
    <li>Live Score ao vivo com notificações</li>
    <li>Detecta se FURIA está em live na Twitch</li>
    <li>Dashboard com gráficos de uso em <code>/admin/analytics</code></li>
  </ul>

  <h2>👨‍💻 Autor</h2>
  <p>Desenvolvido por Leonardo Gonçalves para o desafio técnico da FURIA Tech.</p>
</body>
</html>
