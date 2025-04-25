const chatForm    = document.getElementById("chat-form");
const userInput   = document.getElementById("user-input");
const sendBtn     = document.getElementById("send-btn");
const chatBox     = document.getElementById("chat-box");
const toggleMenu  = document.getElementById("mensagens-toggle");
const fastMenu    = document.getElementById("mensagens-menu");

let historico = [], liveScoreInterval = null, lastLiveScore = "";

// Append + scroll com placeholder inteligente
function appendMessage(remetente, texto) {
  const msg = document.createElement("div");
  msg.classList.add("mensagem", remetente === "Você" ? "usuario" : "bot");

  if (remetente === "Você") {
    msg.textContent = `${remetente}: ${texto}`;
  } else {
    if (texto.trim() === "⌛ Pensando...") {
      msg.innerHTML = `<strong>${remetente}:</strong><br><span class="typing">${texto}</span>`;
    } else {
      msg.innerHTML = `<strong>${remetente}:</strong><br>${texto}`;
    }
  }

  chatBox.appendChild(msg);
  scrollSuave();
}

function scrollSuave() {
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

// Digitação animada para respostas HTML
function digitarMensagem(textoHTML, cb) {
  const ultima = chatBox.querySelector(".mensagem.bot:last-child");
  if (!ultima) return;
  ultima.innerHTML = `<strong>FURIA:</strong><br>`;
  const container = document.createElement("div");
  container.innerHTML = textoHTML;
  const nodes = Array.from(container.childNodes);
  let i = 0;
  (function next() {
    if (i >= nodes.length) {
      if (cb) cb();
      return;
    }
    ultima.appendChild(nodes[i++].cloneNode(true));
    scrollSuave();
    setTimeout(next, 20);
  })();
}

// Envio genérico de chat
chatForm.addEventListener("submit", async e => {
  e.preventDefault();
  const m = userInput.value.trim();
  if (!m) return;

  sendBtn.classList.add("animando");
  sendBtn.addEventListener("animationend", () => sendBtn.classList.remove("animando"), { once: true });

  appendMessage("Você", m);
  historico.push({ role: "user", content: m });
  userInput.value = "";
  userInput.disabled = true;
  appendMessage("FURIA", "⌛ Pensando...");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ historico })
    });
    const data = await res.json();
    digitarMensagem(data.resposta, () => {
      historico.push({ role: "assistant", content: data.resposta });
    });
  } catch (err) {
    const last = chatBox.querySelector(".mensagem.bot:last-child");
    if (last) last.innerHTML = `<strong>FURIA:</strong><br>Erro ao conectar com o bot.`;
    console.error(err);
  }

  userInput.disabled = false;
  fastMenu.classList.remove("show");
});

// Toggle do menu rápido
toggleMenu.addEventListener("click", () => {
  fastMenu.classList.toggle("show");
  toggleMenu.setAttribute(
    "aria-expanded",
    fastMenu.classList.contains("show")
  );
});

// Menu rápido: Próximo jogo (com fallback)
function enviarProximoJogo() {
  const p = "Quando é o próximo jogo da FURIA?";
  appendMessage("Você", p);
  historico.push({ role: "user", content: p });
  appendMessage("FURIA", "⌛ Pensando...");

  fetch("/api/proximo-jogo")
    .then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(d => {
      digitarMensagem(d.resposta, () => {
        historico.push({ role: "assistant", content: d.resposta });
      });
    })
    .catch(err => {
      const msg =
        `🚫 Falha ao acessar HLTV (erro ${err.message}).\nAbrindo Liquipedia...`;
      appendMessage("FURIA", msg);
      window.open("https://liquipedia.net/counterstrike/FURIA", "_blank");
    })
    .finally(() => fastMenu.classList.remove("show"));
}

// Menu rápido: Escalação
function enviarElenco() {
  const p = "Qual é o elenco atual da FURIA?";
  appendMessage("Você", p);
  historico.push({ role: "user", content: p });
  appendMessage("FURIA", "⌛ Pensando...");
  fetch("/api/elenco")
    .then(r => r.json())
    .then(d => digitarMensagem(d.resposta, () => {
      historico.push({ role: "assistant", content: d.resposta });
    }))
    .catch(() => digitarMensagem("Erro ao buscar o elenco da FURIA."))
    .finally(() => fastMenu.classList.remove("show"));
}

// Menu rápido: Notícias
function enviarNoticia() {
  const p = "Quais são as últimas notícias da FURIA?";
  appendMessage("Você", p);
  historico.push({ role: "user", content: p });
  appendMessage("FURIA", "⌛ Pensando...");
  fetch("/api/noticias")
    .then(r => r.json())
    .then(d => digitarMensagem(d.resposta, () => {
      historico.push({ role: "assistant", content: d.resposta });
    }))
    .catch(() => digitarMensagem("Erro ao buscar notícias."))
    .finally(() => fastMenu.classList.remove("show"));
}

// Menu rápido: Redes sociais
function enviarRedesSociais() {
  const p = "Redes sociais da FURIA.gg";
  appendMessage("Você", p);
  historico.push({ role: "user", content: p });
  appendMessage("FURIA", "⌛ Pensando...");
  fetch("/api/redes-sociais")
    .then(r => r.json())
    .then(d => digitarMensagem(d.resposta, () => {
      historico.push({ role: "assistant", content: d.resposta });
    }))
    .catch(() => digitarMensagem("Erro ao carregar redes sociais."))
    .finally(() => fastMenu.classList.remove("show"));
}

// Live Score em tempo real + push
function startLiveScore() {
  fetch("/api/live-score")
    .then(r => r.json())
    .then(d => {
      const score = d.resposta;
      if (score !== lastLiveScore) {
        appendMessage("FURIA", score);
        if (lastLiveScore) new Notification("Live Score FURIA", { body: score });
        lastLiveScore = score;
      }
    })
    .catch(() => {});
}

function enviarLiveScore() {
  if (liveScoreInterval) {
    clearInterval(liveScoreInterval);
    liveScoreInterval = null;
    appendMessage("FURIA", "🔴 Live Score DESATIVADO");
  } else {
    appendMessage("FURIA", "🔴 Live Score ATIVADO");
    startLiveScore();
    liveScoreInterval = setInterval(startLiveScore, 30000);
  }
  fastMenu.classList.remove("show");
}

// Streaming ao vivo (Twitch/YouTube)
function enviarStreaming() {
  appendMessage("Você", "Streaming?");
  appendMessage("FURIA", "⌛ Verificando…");
  fetch("/api/streaming")
    .then(r => r.json())
    .then(d => digitarMensagem(d.resposta))
    .finally(() => fastMenu.classList.remove("show"));
}
