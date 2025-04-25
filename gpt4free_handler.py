import re
from bs4 import BeautifulSoup
from g4f import ChatCompletion

def limpar_resposta(resposta):
    if isinstance(resposta, dict) and "choices" in resposta:
        resposta = resposta["choices"][0]["message"]["content"]
    soup = BeautifulSoup(resposta, "html.parser")
    texto = soup.get_text(separator="\n")
    texto = re.sub(r'[\uE000-\uF8FF\uFFF0-\uFFFF]', '', texto)
    texto = re.sub(r'[*_`>#-]+', '', texto)
    texto = re.sub(r'\n{2,}', '\n', texto).strip()
    texto = re.sub(r'([.!?])\s*', r'\1\n', texto)
    return texto

def perguntar_furia(historico):
    if not any(m["role"]=="system" for m in historico):
        historico.insert(0,{
            "role":"system",
            "content":(
                "Você é o assistente oficial da torcida FURIA.gg. "
                "Use gírias de torcedor, emojis de torcida e informações atualizadas, sem HTML ou markdown."
            )
        })
    try:
        res = ChatCompletion.create(model="gpt-4", messages=historico)
        return limpar_resposta(res)
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
