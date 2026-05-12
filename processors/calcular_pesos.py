# processors/calcular_pesos.py
# Calcula o indice de forca (0-100) para cada selecao classificada
#
# Fontes do fallback:
#   Ranking FIFA: atualizado em 01/04/2026 (fonte: FIFA.com / Wikipedia)
#   1 Franca 1877.32 | 2 Espanha 1876.40 | 3 Argentina 1874.81
#   4 Inglaterra 1825.97 | 5 Portugal 1763.83 | 6 Brasil 1761.16
#   7 Holanda 1757.87 | 8 Marrocos 1755.87 | 9 Belgica 1734.71
#   10 Alemanha 1730.37 | 11 Croacia 1717.07 | 13 Colombia 1693.09
#   14 Senegal 1688.99 | 15 Mexico 1681.03 | 16 Estados Unidos 1673.13
#   17 Uruguai 1673.07 | 18 Japao 1660.43 | 19 Suica 1649.40

import pandas as pd
import numpy as np
import os
from datetime import datetime

DATA_PROCESSED = "data/processed"


def calcular_peso_selecoes(
    df_selecoes: pd.DataFrame,
    df_ranking: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera o indice de forca (0-100) de cada selecao combinando:
      - Ranking FIFA normalizado       : peso 50%
      - Dificuldade das eliminatorias  : peso 30%
      - Historico Copa 2022            : peso 10%
      - Fator pais-sede                : peso 10%
    """
    print("[Pesos] Calculando indice de forca das selecoes...")

    df = df_selecoes.copy()

    # --- 1. Merge com ranking FIFA coletado ---
    if not df_ranking.empty and "selecao" in df_ranking.columns:
        df = df.merge(
            df_ranking[["selecao", "posicao", "pontos"]],
            on="selecao", how="left"
        )
    else:
        print("[Pesos] Ranking FIFA nao disponivel. Usando fallback (01/04/2026).")
        df["posicao"] = _ranking_aproximado(df["selecao"])
        df["pontos"]  = _pontos_aproximados(df["selecao"])

    # --- 2. Score Ranking FIFA (0-1, posicao 1 = 1.0) ---
    max_pos = df["posicao"].max() if df["posicao"].notna().any() else 210
    df["score_ranking"] = (1 - ((df["posicao"] - 1) / max_pos)).clip(0, 1)

    # --- 3. Score Eliminatorias (0-1) ---
    df["score_eliminatoria"] = df["dificuldade_eliminatoria"] / 10.0

    # --- 4. Fator sede ---
    df["score_sede"] = df["pais_sede"].astype(float) * 0.05

    # --- 5. Historico Copa 2022 ---
    df["score_historico"] = df["selecao"].map(_historico_copa2022()).fillna(0.30)

    # --- 6. Indice de forca final ---
    df["indice_forca"] = (
        df["score_ranking"]      * 0.50 +
        df["score_eliminatoria"] * 0.30 +
        df["score_historico"]    * 0.10 +
        df["score_sede"]         * 0.10
    )

    # Normaliza 0-100
    imin = df["indice_forca"].min()
    imax = df["indice_forca"].max()
    df["indice_forca_100"] = ((df["indice_forca"] - imin) / (imax - imin) * 100).round(2)

    df["ranking_projeto"] = df["indice_forca"].rank(ascending=False).astype(int)
    df["calculado_em"]    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(DATA_PROCESSED, exist_ok=True)
    caminho = f"{DATA_PROCESSED}/selecoes_com_pesos.csv"
    df.sort_values("ranking_projeto").to_csv(caminho, index=False)
    print(f"[Pesos] Salvo: {caminho}")

    return df.sort_values("ranking_projeto")


# ---------------------------------------------------------------------------
# FALLBACK — Ranking FIFA oficial de 01/04/2026
# Nomes sem acentos para compatibilidade com selecoes_copa.py
# Fonte: FIFA.com / Wikipedia / imirante.com (01/04/2026)
# ---------------------------------------------------------------------------

def _ranking_aproximado(selecoes: pd.Series) -> pd.Series:
    ranking = {
        # Top 20 — fonte: FIFA 01/04/2026
        "Franca":           1,
        "Espanha":          2,
        "Argentina":        3,
        "Inglaterra":       4,
        "Portugal":         5,
        "Brasil":           6,
        "Holanda":          7,
        "Marrocos":         8,
        "Belgica":          9,
        "Alemanha":        10,
        "Croacia":         11,
        "Colombia":        13,
        "Senegal":         14,
        "Mexico":          15,
        "Estados Unidos":  16,
        "Uruguai":         17,
        "Japao":           18,
        "Suica":           19,
        # 21-50 estimados com base no ranking 01/04/2026
        "Austria":         21,
        "Equador":         22,
        "Coreia do Sul":   23,
        "Turquia":         24,
        "Australia":       25,
        "Noruega":         26,
        "Suecia":          27,
        "Escocia":         28,
        "Ira":             29,
        "Paraguai":        30,
        "Jordania":        31,
        "Uzbequistao":     32,
        "Canada":          33,
        "Republica Tcheca":34,
        "Bosnia e Herzegovina": 36,
        "Catar":           37,
        "Iraque":          38,
        "Tunisia":         39,
        "Arabia Saudita":  40,
        "Africa do Sul":   41,
        "Cabo Verde":      42,
        "Costa do Marfim": 43,
        "Egito":           44,
        "Gana":            45,
        "RD Congo":        46,
        "Algeria":         47,
        "Nova Zelandia":   48,
        "Panama":          49,
        "Haiti":           50,
        "Curacao":         75,
    }
    return selecoes.map(ranking).fillna(80)


def _pontos_aproximados(selecoes: pd.Series) -> pd.Series:
    pontos = {
        # Pontos reais — fonte: FIFA 01/04/2026
        "Franca":          1877.32,
        "Espanha":         1876.40,
        "Argentina":       1874.81,
        "Inglaterra":      1825.97,
        "Portugal":        1763.83,
        "Brasil":          1761.16,
        "Holanda":         1757.87,
        "Marrocos":        1755.87,
        "Belgica":         1734.71,
        "Alemanha":        1730.37,
        "Croacia":         1717.07,
        "Colombia":        1693.09,
        "Senegal":         1688.99,
        "Mexico":          1681.03,
        "Estados Unidos":  1673.13,
        "Uruguai":         1673.07,
        "Japao":           1660.43,
        "Suica":           1649.40,
        # Estimados (abaixo do top 18)
        "Austria":         1610.00,
        "Equador":         1600.00,
        "Coreia do Sul":   1595.00,
        "Turquia":         1580.00,
        "Australia":       1560.00,
        "Noruega":         1550.00,
        "Suecia":          1540.00,
        "Escocia":         1530.00,
        "Ira":             1520.00,
        "Paraguai":        1510.00,
        "Jordania":        1490.00,
        "Uzbequistao":     1480.00,
        "Canada":          1470.00,
        "Republica Tcheca":1460.00,
        "Bosnia e Herzegovina": 1440.00,
        "Catar":           1420.00,
        "Iraque":          1400.00,
        "Tunisia":         1390.00,
        "Arabia Saudita":  1380.00,
        "Africa do Sul":   1370.00,
        "Cabo Verde":      1350.00,
        "Costa do Marfim": 1340.00,
        "Egito":           1330.00,
        "Gana":            1320.00,
        "RD Congo":        1310.00,
        "Algeria":         1300.00,
        "Nova Zelandia":   1280.00,
        "Panama":          1260.00,
        "Haiti":           1200.00,
        "Curacao":         1100.00,
    }
    return selecoes.map(pontos).fillna(1150.00)


def _historico_copa2022() -> dict:
    """
    Score baseado na Copa 2022 (Qatar).
    Nota: Copa 2022 tinha 32 selecoes — peso reduzido (10%) pois a mudanca
    para 48 selecoes invalida comparacao direta de colocacoes.
    Nomes sem acentos para compatibilidade com selecoes_copa.py.
    """
    return {
        "Argentina":       1.00,   # Campea
        "Franca":          0.85,   # Vice
        "Croacia":         0.75,   # 3o lugar
        "Marrocos":        0.65,   # 4o lugar (1a selecao africana na semi)
        "Holanda":         0.55,   # Quartas
        "Brasil":          0.55,   # Quartas
        "Inglaterra":      0.55,   # Quartas
        "Portugal":        0.55,   # Quartas
        "Espanha":         0.40,   # Oitavas
        "Alemanha":        0.20,   # Fase de grupos (eliminacao precoce)
        "Japao":           0.40,   # Oitavas (surpreendeu)
        "Coreia do Sul":   0.40,   # Oitavas
        "Senegal":         0.40,   # Oitavas
        "Australia":       0.40,   # Oitavas
        "Suica":           0.40,   # Oitavas
        "Estados Unidos":  0.40,   # Oitavas
        "Polonia":         0.30,   # Grupos
        "Mexico":          0.30,   # Grupos
        "Canada":          0.25,   # Grupos (estreia)
        "Uruguai":         0.30,   # Grupos
        "Colombia":        0.30,   # Nao estava em 2022 — media
        "Belgica":         0.30,   # Grupos
        "Cameroes":        0.30,   # Grupos
    }


if __name__ == "__main__":
    df_sel = pd.DataFrame([
        {"selecao": "Brasil",   "confederacao": "CONMEBOL", "codigo": "BRA",
         "dificuldade_eliminatoria": 8.5, "pais_sede": False},
        {"selecao": "Franca",   "confederacao": "UEFA",     "codigo": "FRA",
         "dificuldade_eliminatoria": 9.0, "pais_sede": False},
        {"selecao": "Argentina","confederacao": "CONMEBOL", "codigo": "ARG",
         "dificuldade_eliminatoria": 8.5, "pais_sede": False},
        {"selecao": "Estados Unidos","confederacao": "CONCACAF","codigo": "USA",
         "dificuldade_eliminatoria": 6.5, "pais_sede": True},
    ])
    df_res = calcular_peso_selecoes(df_sel, pd.DataFrame())
    print(df_res[["selecao","ranking_projeto","indice_forca_100"]].to_string(index=False))
