# collectors/ranking_fifa.py
# Coleta o ranking FIFA atual via scraping do site oficial
# Fonte: https://www.fifa.com/fifa-world-ranking/men

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from datetime import datetime

DATA_RAW = "data/raw"


def coletar_ranking_fifa() -> pd.DataFrame:
    """
    Coleta o ranking FIFA masculino atual.
    Retorna DataFrame com colunas: posicao, selecao, pontos, variacao
    """
    print("[FIFA Ranking] Iniciando coleta...")

    url = "https://www.fifa.com/fifa-world-ranking/men"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[FIFA Ranking] ERRO na requisição: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    # O ranking FIFA carrega via JavaScript — precisamos do endpoint de dados
    # Alternativa: endpoint de dados embutido na página
    data = _extrair_dados_json(soup)

    if not data:
        print("[FIFA Ranking] Dados não encontrados via JSON. Tentando scraping direto...")
        data = _scraping_direto(soup)

    if not data:
        print("[FIFA Ranking] FALHA: não foi possível coletar o ranking.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["coletado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Salva raw
    os.makedirs(DATA_RAW, exist_ok=True)
    caminho = f"{DATA_RAW}/ranking_fifa_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(caminho, index=False)
    print(f"[FIFA Ranking] Salvo em: {caminho} ({len(df)} seleções)")

    return df


def _extrair_dados_json(soup: BeautifulSoup) -> list:
    """Tenta extrair dados do JSON embutido na página."""
    scripts = soup.find_all("script", type="application/json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            # Navega pela estrutura do JSON da FIFA
            rankings = _navegar_json_fifa(data)
            if rankings:
                return rankings
        except (json.JSONDecodeError, TypeError):
            continue
    return []


def _navegar_json_fifa(data: dict) -> list:
    """Navega pela estrutura do JSON retornado pela FIFA."""
    resultado = []
    try:
        # Estrutura típica do site FIFA
        rankings_raw = (
            data.get("props", {})
            .get("pageProps", {})
            .get("pageData", {})
            .get("ranking", [])
        )
        for item in rankings_raw:
            resultado.append({
                "posicao": item.get("rankingPosition", ""),
                "selecao": item.get("teamName", {}).get("en", ""),
                "pais_codigo": item.get("countryCode", ""),
                "pontos": item.get("totalPoints", 0),
                "variacao": item.get("previousRankingPosition", 0),
            })
    except (AttributeError, KeyError):
        pass
    return resultado


def _scraping_direto(soup: BeautifulSoup) -> list:
    """
    Fallback: scraping direto de elementos HTML.
    O site FIFA usa renderização dinâmica, então isso pode falhar.
    Se falhar, usar o endpoint alternativo abaixo.
    """
    resultado = []
    linhas = soup.select("tr.fi-table__tr")
    for linha in linhas:
        try:
            posicao = linha.select_one(".fi-table__rank").get_text(strip=True)
            selecao = linha.select_one(".fi-t__nText").get_text(strip=True)
            pontos = linha.select_one(".fi-table__pts").get_text(strip=True)
            resultado.append({
                "posicao": int(posicao),
                "selecao": selecao,
                "pontos": float(pontos.replace(",", ".")),
                "variacao": 0,
            })
        except (AttributeError, ValueError):
            continue
    return resultado


def coletar_ranking_via_api_publica() -> pd.DataFrame:
    """
    Alternativa mais confiável: coleta ranking FIFA via endpoint público
    que algumas ferramentas expõem (ex: api.football-data.org ou datasets Kaggle).
    Use esta função se o scraping do site FIFA falhar.
    """
    print("[FIFA Ranking - API Pública] Tentando endpoint alternativo...")

    # Este endpoint agrega dados do ranking FIFA de forma estruturada
    url = "https://api.football-data.org/v4/competitions/WC/teams"
    headers = {"X-Auth-Token": "SUA_CHAVE_FOOTBALL_DATA_ORG"}  # Gratuito em football-data.org

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        times = data.get("teams", [])

        resultado = []
        for time in times:
            resultado.append({
                "selecao": time.get("name", ""),
                "pais_codigo": time.get("tla", ""),
                "area": time.get("area", {}).get("name", ""),
            })

        df = pd.DataFrame(resultado)
        print(f"[FIFA Ranking - API Pública] {len(df)} seleções coletadas.")
        return df

    except requests.RequestException as e:
        print(f"[FIFA Ranking - API Pública] ERRO: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    df = coletar_ranking_fifa()
    if df.empty:
        print("Tentando via API pública...")
        df = coletar_ranking_via_api_publica()
    print(df.head(20))
