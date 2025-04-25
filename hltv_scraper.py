import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, RequestException

# Primeiro tenta no HLTV, se nao for pula pro Liquipedia, se ainda sim nao for, manda um "tenta mais tarde"
def buscar_proximo_jogo_furia():
    try:
        return buscar_no_hltv()
    except Exception:
        # fallback pro Liquipedia 
        try:
            return buscar_no_liquipedia()
        except Exception:
            # Sem sorte nos dois, manda esse aviso 
            return (
                "😢 Não consegui encontrar o próximo jogo da FURIA no momento. "
                "Tente novamente mais tarde!"
            )

# Scrape do HLTV: pega evento, data, hora e adversário direto do site
def buscar_no_hltv():
    url = "https://www.hltv.org/team/8297/furia"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Achando o card do próximo match
    match_card = soup.find("div", class_="upcomingMatch")
    event = match_card.find("div", class_="matchEventName").text.strip()
    time  = match_card.find("div", class_="matchTime").text.strip()
    date  = match_card.find("div", class_="matchDay").text.strip()
    opp   = match_card.find("div", class_="matchTeam team2").text.strip()

    return (
        "🎮 Próximo jogo da FURIA (via HLTV)\n"
        f"🆚 Adversário: {opp}\n"
        f"🏆 Evento: {event}\n"
        f"🗓️ Data: {date}\n"
        f"⏰ Horário: {time}\n"
        "🔗 https://www.hltv.org/team/8297/furia"
    )

# se HLTV falhar, bate no Liquipedia e tenta pegar o próximo jogo
def buscar_no_liquipedia():
    url = "https://liquipedia.net/counterstrike/FURIA"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    match_table = soup.find("table", class_="infobox_matches_content")
    first_row   = match_table.find("tr", class_="match-row") if match_table else None
    if not first_row:
        return (
            "A FURIA ainda não tem jogos programados nos próximos dias. "
            "Volte em breve para conferir!"
        )
    cells = first_row.find_all("td")
    date     = cells[0].text.strip()
    time     = cells[1].text.strip()
    opponent = cells[2].text.strip()
    event    = cells[3].text.strip()

    return (
        "🎮 Próximo jogo da FURIA (via Liquipedia)\n"
        f"🆚 Adversário: {opponent}\n"
        f"🏆 Evento: {event}\n"
        f"🗓️ Data: {date}\n"
        f"⏰ Horário: {time}\n"
        "🔗 https://liquipedia.net/counterstrike/FURIA"
    )

# pega elenco atual no Liquipedia, ou manda aquele "não achei" se não rolar
def buscar_elenco_furia_cs2():
    url = "https://liquipedia.net/counterstrike/FURIA"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        ativo  = soup.find("span", {"id": "Active"})  # âncora do elenco ativo
        tabela = ativo.find_next("table", class_="wikitable") if ativo else None
        if not tabela:
            return "🤷‍♂️ Não encontrei elenco no Liquipedia."

        jogadores = []
        for tr in tabela.find_all("tr")[1:]:  # pula cabeçalho
            cols = tr.find_all("td")
            if len(cols) >= 2:
                nick = cols[1].text.strip()
                nome = cols[0].text.strip()
                jogadores.append(f"• {nick} ({nome})")

        return "🎯 Elenco atual (Liquipedia):\n" + "\n".join(jogadores)

    except HTTPError as http_err:
        if http_err.response.status_code == 403:
            # 🚫 se der forbiden manda o link
            return (
                "🚫 403 Forbidden ao acessar Liquipedia. "
                "Veja o elenco direto em: https://liquipedia.net/counterstrike/FURIA"
            )
        return f"❌ Erro HTTP ao buscar elenco: {http_err}"
    except RequestException as e:
        return f"❌ Erro de requisição ao buscar elenco: {e}"

# se tiver jogo rolando, mostra score e mapa, senão manda esse aviso
def buscar_live_score_furia():
    url = "https://www.hltv.org/team/8297/furia"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        live = soup.find("div", class_="liveMatch")
        if not live:
            return "🎮 Nenhum jogo ao vivo no momento."

        # Detalhes do live match
        event  = live.find("div", class_="matchEventName").text.strip()
        t1_div = live.find("div", class_="matchTeam team1")
        t2_div = live.find("div", class_="matchTeam team2")
        name1  = t1_div.find("div", class_="matchTeamName").text.strip()
        score1 = t1_div.find("div", class_="matchScore").text.strip()
        name2  = t2_div.find("div", class_="matchTeamName").text.strip()
        score2 = t2_div.find("div", class_="matchScore").text.strip()
        map_el = live.find("div", class_="mapName")
        map_txt = map_el.text.strip() if map_el else ""

        # resposta estilo lista
        result = [
            "🎮 Live Score (via HLTV)",
            f"🏆 {event}",
            f"{name1} {score1} x {score2} {name2}",
        ]
        if map_txt:
            result.append(f"🗺️ {map_txt}")
        return "\n".join(result)

    except HTTPError as http_err:
        if http_err.response.status_code == 403:
            # fallback pra link direto
            return (
                "🚫 403 Forbidden ao acessar HLTV. "
                "Confira o live score direto em: https://www.hltv.org/team/8297/furia"
            )
        return f"❌ Erro HTTP ao buscar live score: {http_err}"
    except RequestException as e:
        return f"❌ Erro de requisição ao buscar live score: {e}"
