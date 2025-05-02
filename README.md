<body>
  <h1>🔥 FURIA Chatbot</h1>
  <p>Um chatbot inteligente feito para a torcida da FURIA, com informações em tempo real sobre o time de CS:GO/CS2. Scraping, IA, integrações e visual bonito para manter os fãs atualizados sem sair da página.</p>

  <h2>⚙️ Tecnologias Utilizadas</h2>
  <ul>
    <li>Python + Flask</li>
    <li>JavaScript (Vanilla)</li>
    <li>HTML + CSS responsivo</li>
    <li>BeautifulSoup para scraping</li>
    <li>GPT4Free (IA via gpt4free)</li>
    <li>Twitch API (detecção de lives)</li>
    <li>Chart.js para visualização de dados</li>
  </ul>

  <h2>📆 Funcionalidades</h2>
  <ul>
    <li>🏀 Próximo jogo da FURIA com fallback HLTV/Liquipedia</li>
    <li>📅 Escalação atualizada do time</li>
    <li>📰 Notícias recentes sobre a FURIA via Google News</li>
    <li>⏱️ Live Score ao vivo com atualização automática</li>
    <li>🔴 Verifica se a FURIA está transmitindo na Twitch</li>
    <li>📊 Dashboard de uso em <code>/admin/analytics</code></li>
    <li>🏛️ Painel administrativo com log de conversas em <code>/admin</code></li>
  </ul>

  <h2>⚡ Instalação Local</h2>
  <ol>
    <li>Clone o repositório: <code>git clone https://github.com/leoouu/furia-chatbot</code></li>
    <li>Instale as dependências: <code>pip install -r requirements.txt</code></li>
    <li>Crie um arquivo <code>.env</code> na raiz com:
      <pre>
TWITCH_CLIENT_ID=seu_client_id
tWITCH_CLIENT_SECRET=sua_secret</pre>
    </li>
    <li>Inicie o servidor: <code>python app.py</code></li>
    <li>Acesse: <a href="http://localhost:5000">http://localhost:5000</a></li>
  </ol>

  <h2>🔗 Link Online</h2>
  <p><a href="https://furia-chatbot-jn5w.onrender.com" target="_blank">furia-chatbot-jn5w.onrender.com</a></p>

  <h2>👨‍💻 Autor</h2>
  <p>Desenvolvido com muito carinho por <strong>Leonardo Gonçalves</strong> para o desafio técnico da FURIA Tech.</p>
</body>
