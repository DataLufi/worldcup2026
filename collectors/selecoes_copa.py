# collectors/selecoes_copa.py
# 48 selecoes classificadas — lista FINAL apos repescagem (abril/2026)
#
# Repescagem UEFA:              Turquia, Suecia, Republica Tcheca, Bosnia e Herzegovina
# Repescagem intercontinental:  Iraque (venceu Bolivia), RD Congo (venceu Jamaica)
# Fora: Italia, Polonia, Dinamarca, Nigeria, Costa Rica, Serbia, Kosovo, Jamaica, Bolivia
#
# Grupos: sorteio FIFA (05/12/2025) + repescagem confirmada (31/03/2026)
# Fonte: cnnbrasil.com.br, agenciabrasil.ebc.com.br, olympics.com
# Atualizado: 10/05/2026

import pandas as pd
import os
from datetime import datetime

DATA_RAW       = "data/raw"
DATA_PROCESSED = "data/processed"

ELIMINATORIAS_CONFIG = {
    "UEFA":     {"vagas": 16, "dificuldade_base": 9.0},
    "CONMEBOL": {"vagas":  6, "dificuldade_base": 8.5},
    "CONCACAF": {"vagas":  6, "dificuldade_base": 6.5},
    "CAF":      {"vagas":  9, "dificuldade_base": 6.0},
    "AFC":      {"vagas":  8, "dificuldade_base": 6.0},
    "OFC":      {"vagas":  1, "dificuldade_base": 4.0},
}

# Lista FINAL — 48 selecoes, zero pendentes
SELECOES_CLASSIFICADAS = [
    # UEFA — 16 vagas (12 diretas + 4 pela repescagem europeia)
    {"selecao": "Alemanha",             "confederacao": "UEFA",     "codigo": "GER"},
    {"selecao": "Espanha",              "confederacao": "UEFA",     "codigo": "ESP"},
    {"selecao": "Inglaterra",           "confederacao": "UEFA",     "codigo": "ENG"},
    {"selecao": "Franca",               "confederacao": "UEFA",     "codigo": "FRA"},
    {"selecao": "Portugal",             "confederacao": "UEFA",     "codigo": "POR"},
    {"selecao": "Holanda",              "confederacao": "UEFA",     "codigo": "NED"},
    {"selecao": "Belgica",              "confederacao": "UEFA",     "codigo": "BEL"},
    {"selecao": "Croacia",              "confederacao": "UEFA",     "codigo": "CRO"},
    {"selecao": "Austria",              "confederacao": "UEFA",     "codigo": "AUT"},
    {"selecao": "Suica",                "confederacao": "UEFA",     "codigo": "SUI"},
    {"selecao": "Escocia",              "confederacao": "UEFA",     "codigo": "SCO"},
    {"selecao": "Noruega",              "confederacao": "UEFA",     "codigo": "NOR"},
    # Repescagem europeia (confirmados em 31/03/2026)
    {"selecao": "Turquia",              "confederacao": "UEFA",     "codigo": "TUR"},
    {"selecao": "Suecia",               "confederacao": "UEFA",     "codigo": "SWE"},
    {"selecao": "Republica Tcheca",     "confederacao": "UEFA",     "codigo": "CZE"},
    {"selecao": "Bosnia e Herzegovina", "confederacao": "UEFA",     "codigo": "BIH"},

    # CONMEBOL — 6 vagas
    {"selecao": "Argentina",            "confederacao": "CONMEBOL", "codigo": "ARG"},
    {"selecao": "Brasil",               "confederacao": "CONMEBOL", "codigo": "BRA"},
    {"selecao": "Colombia",             "confederacao": "CONMEBOL", "codigo": "COL"},
    {"selecao": "Equador",              "confederacao": "CONMEBOL", "codigo": "ECU"},
    {"selecao": "Paraguai",             "confederacao": "CONMEBOL", "codigo": "PAR"},
    {"selecao": "Uruguai",              "confederacao": "CONMEBOL", "codigo": "URU"},

    # CONCACAF — 6 vagas (3 paises-sede garantidos + 3 via eliminatorias)
    {"selecao": "Canada",               "confederacao": "CONCACAF", "codigo": "CAN"},  # sede
    {"selecao": "Estados Unidos",       "confederacao": "CONCACAF", "codigo": "USA"},  # sede
    {"selecao": "Mexico",               "confederacao": "CONCACAF", "codigo": "MEX"},  # sede
    {"selecao": "Curacao",              "confederacao": "CONCACAF", "codigo": "CUW"},
    {"selecao": "Haiti",                "confederacao": "CONCACAF", "codigo": "HAI"},
    {"selecao": "Panama",               "confederacao": "CONCACAF", "codigo": "PAN"},

    # CAF — 9 vagas (9 diretas + RD Congo via repescagem intercontinental = 10 total)
    {"selecao": "Africa do Sul",        "confederacao": "CAF",      "codigo": "RSA"},
    {"selecao": "Algeria",              "confederacao": "CAF",      "codigo": "ALG"},
    {"selecao": "Cabo Verde",           "confederacao": "CAF",      "codigo": "CPV"},
    {"selecao": "Costa do Marfim",      "confederacao": "CAF",      "codigo": "CIV"},
    {"selecao": "Egito",                "confederacao": "CAF",      "codigo": "EGY"},
    {"selecao": "Gana",                 "confederacao": "CAF",      "codigo": "GHA"},
    {"selecao": "Marrocos",             "confederacao": "CAF",      "codigo": "MAR"},
    {"selecao": "Senegal",              "confederacao": "CAF",      "codigo": "SEN"},
    {"selecao": "Tunisia",              "confederacao": "CAF",      "codigo": "TUN"},
    # Repescagem intercontinental (venceu Jamaica)
    {"selecao": "RD Congo",             "confederacao": "CAF",      "codigo": "COD"},

    # AFC — 8 vagas (7 diretas + Iraque via repescagem intercontinental)
    {"selecao": "Arabia Saudita",       "confederacao": "AFC",      "codigo": "KSA"},
    {"selecao": "Australia",            "confederacao": "AFC",      "codigo": "AUS"},
    {"selecao": "Catar",                "confederacao": "AFC",      "codigo": "QAT"},
    {"selecao": "Coreia do Sul",        "confederacao": "AFC",      "codigo": "KOR"},
    {"selecao": "Ira",                  "confederacao": "AFC",      "codigo": "IRN"},
    {"selecao": "Japao",                "confederacao": "AFC",      "codigo": "JPN"},
    {"selecao": "Jordania",             "confederacao": "AFC",      "codigo": "JOR"},
    {"selecao": "Uzbequistao",          "confederacao": "AFC",      "codigo": "UZB"},
    # Repescagem intercontinental (venceu Bolivia — ultimo classificado, 48o)
    {"selecao": "Iraque",               "confederacao": "AFC",      "codigo": "IRQ"},

    # OFC — 1 vaga
    {"selecao": "Nova Zelandia",        "confederacao": "OFC",      "codigo": "NZL"},
]

# Grupos OFICIAIS — sorteio FIFA (05/12/2025) com repescagens preenchidas (31/03/2026)
# Fonte: agenciabrasil.ebc.com.br, cnnbrasil.com.br, olympics.com
# Jogo de abertura: 11/jun — Mexico x Africa do Sul (Estadio Azteca)
# Final: 19/jul — MetLife Stadium, Nova Jersey
GRUPOS_OFICIAIS = {
    "A": ["Mexico",         "Africa do Sul",        "Coreia do Sul",    "Republica Tcheca"],
    "B": ["Canada",         "Bosnia e Herzegovina", "Catar",            "Suica"],
    "C": ["Brasil",         "Marrocos",             "Escocia",          "Haiti"],
    "D": ["Estados Unidos", "Paraguai",             "Australia",        "Turquia"],
    "E": ["Alemanha",       "Curacao",              "Costa do Marfim",  "Equador"],
    "F": ["Holanda",        "Japao",                "Suecia",           "Tunisia"],
    "G": ["Belgica",        "Egito",                "Ira",              "Nova Zelandia"],
    "H": ["Espanha",        "Cabo Verde",           "Arabia Saudita",   "Uruguai"],
    "I": ["Franca",         "Senegal",              "Iraque",           "Noruega"],
    "J": ["Argentina",      "Algeria",              "Austria",          "Jordania"],
    "K": ["Portugal",       "RD Congo",             "Uzbequistao",      "Colombia"],
    "L": ["Inglaterra",     "Croacia",              "Gana",             "Panama"],
}


def gerar_dataset_selecoes() -> pd.DataFrame:
    """Gera dataset com as 48 selecoes classificadas."""
    print("[Selecoes] Gerando dataset das 48 selecoes...")

    df = pd.DataFrame(SELECOES_CLASSIFICADAS)
    df = df.drop_duplicates(subset=["codigo"]).reset_index(drop=True)

    df["dificuldade_eliminatoria"] = df["confederacao"].map(
        {k: v["dificuldade_base"] for k, v in ELIMINATORIAS_CONFIG.items()}
    ).fillna(5.0)

    paises_sede = ["USA", "MEX", "CAN"]
    df["pais_sede"] = df["codigo"].isin(paises_sede)
    df["gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(DATA_RAW, exist_ok=True)
    caminho = f"{DATA_RAW}/selecoes_classificadas.csv"
    df.to_csv(caminho, index=False)
    print(f"[Selecoes] Salvo: {caminho} ({len(df)} selecoes)")
    return df


def coletar_grupos_copa() -> pd.DataFrame:
    """Retorna os grupos oficiais da Copa 2026."""
    print("[Grupos] Carregando grupos oficiais da Copa 2026...")

    registros = []
    for grupo, selecoes in GRUPOS_OFICIAIS.items():
        for selecao in selecoes:
            registros.append({"grupo": grupo, "selecao": selecao})

    df = pd.DataFrame(registros)
    os.makedirs(DATA_RAW, exist_ok=True)
    caminho = f"{DATA_RAW}/grupos_copa2026.csv"
    df.to_csv(caminho, index=False)
    print(f"[Grupos] Salvo: {caminho} ({df['grupo'].nunique()} grupos)")
    return df


if __name__ == "__main__":
    df_s = gerar_dataset_selecoes()
    print("\n--- Selecoes por Confederacao ---")
    print(df_s.groupby("confederacao").size().to_string())

    df_g = coletar_grupos_copa()
    print("\n--- Grupos Oficiais ---")
    for g in sorted(df_g["grupo"].unique()):
        times = df_g[df_g["grupo"] == g]["selecao"].tolist()
        print(f"  Grupo {g}: {', '.join(times)}")
