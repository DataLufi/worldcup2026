# models/modelo_preditivo.py
# Fase 2 — Modelo preditivo de confrontos
#
# Para cada jogo, calcula:
#   1. Probabilidade de vitória/empate/derrota (%)
#   2. Placar mais provável
#
# Metodologia:
#   - Diferença de índice de força entre os dois times
#   - Distribuição de Poisson para gols esperados
#   - Ajuste por fator sede e forma recente
#   - Validação histórica contra resultados de Copas anteriores

import pandas as pd
import numpy as np
from scipy.stats import poisson
import os
from datetime import datetime

DATA_PROCESSED = "data/processed"


# -----------------------------------------------------------------------
# CONSTANTES DO MODELO
# -----------------------------------------------------------------------

# Média histórica de gols por jogo em Copas do Mundo (últimas 4 edições)
# Fonte: FIFA — usado para calibrar o modelo de Poisson
MEDIA_GOLS_COPA = 2.64

# Bônus de gols esperados para o time da casa/sede
FATOR_SEDE_GOLS = 0.15   # +15% nos gols esperados para países-sede

# Teto de gols considerados pelo modelo (0 a N)
TETO_GOLS = 6

# Número de simulações Monte Carlo para classificação dos grupos
N_SIMULACOES = 10_000


# -----------------------------------------------------------------------
# MÓDULO 1 — GOLS ESPERADOS
# -----------------------------------------------------------------------

def calcular_gols_esperados(
    indice_forca_a: float,
    indice_forca_b: float,
    sede_a: bool = False,
    sede_b: bool = False,
) -> tuple:
    """
    Calcula os gols esperados (λ) para cada time usando a diferença
    de índice de força normalizada e a média histórica de Copas.

    Parâmetros:
        indice_forca_a : índice de força do time A (0-100)
        indice_forca_b : índice de força do time B (0-100)
        sede_a         : True se o time A é país-sede
        sede_b         : True se o time B é país-sede

    Retorna:
        (lambda_a, lambda_b) — gols esperados por cada time
    """
    forca_a = indice_forca_a / 100
    forca_b = indice_forca_b / 100

    soma = forca_a + forca_b
    proporcao_a = forca_a / soma
    proporcao_b = forca_b / soma

    lambda_a = proporcao_a * MEDIA_GOLS_COPA
    lambda_b = proporcao_b * MEDIA_GOLS_COPA

    if sede_a:
        lambda_a *= (1 + FATOR_SEDE_GOLS)
    if sede_b:
        lambda_b *= (1 + FATOR_SEDE_GOLS)

    return round(lambda_a, 4), round(lambda_b, 4)


# -----------------------------------------------------------------------
# MÓDULO 2 — DISTRIBUIÇÃO DE POISSON
# -----------------------------------------------------------------------

def matriz_probabilidades(lambda_a: float, lambda_b: float) -> np.ndarray:
    """
    Gera a matriz de probabilidades de placar usando distribuição de Poisson.

    A distribuição de Poisson é amplamente usada em modelos de previsão
    de futebol (Dixon-Coles, 1997) por modelar bem eventos raros e
    independentes — como gols em uma partida.

    Retorna:
        Matriz (TETO_GOLS+1) x (TETO_GOLS+1) onde
        matriz[i][j] = probabilidade de placar i x j
    """
    gols = np.arange(0, TETO_GOLS + 1)
    prob_a = poisson.pmf(gols, lambda_a)
    prob_b = poisson.pmf(gols, lambda_b)
    return np.outer(prob_a, prob_b)


def calcular_probabilidades(matriz: np.ndarray) -> dict:
    """
    A partir da matriz de placares, calcula:
    - Probabilidade de vitória do time A
    - Probabilidade de empate
    - Probabilidade de vitória do time B
    - Placar mais provável
    - Top 5 placares mais prováveis
    """
    n = matriz.shape[0]

    prob_vitoria_a = 0.0
    prob_empate    = 0.0
    prob_vitoria_b = 0.0

    for i in range(n):
        for j in range(n):
            p = matriz[i, j]
            if i > j:
                prob_vitoria_a += p
            elif i == j:
                prob_empate += p
            else:
                prob_vitoria_b += p

    total = prob_vitoria_a + prob_empate + prob_vitoria_b
    prob_vitoria_a = round((prob_vitoria_a / total) * 100, 1)
    prob_empate    = round((prob_empate    / total) * 100, 1)
    prob_vitoria_b = round((prob_vitoria_b / total) * 100, 1)

    idx_max = np.unravel_index(np.argmax(matriz), matriz.shape)
    placar_mais_provavel = f"{idx_max[0]} x {idx_max[1]}"
    prob_placar_mais_provavel = round(float(matriz[idx_max]) * 100, 1)

    indices_flat = np.argsort(matriz, axis=None)[::-1][:5]
    top5 = []
    for idx in indices_flat:
        i, j = np.unravel_index(idx, matriz.shape)
        top5.append({
            "placar": f"{i} x {j}",
            "probabilidade": round(float(matriz[i, j]) * 100, 1)
        })

    return {
        "prob_vitoria_a":  prob_vitoria_a,
        "prob_empate":     prob_empate,
        "prob_vitoria_b":  prob_vitoria_b,
        "placar_provavel": placar_mais_provavel,
        "prob_placar":     prob_placar_mais_provavel,
        "top5_placares":   top5,
    }


# -----------------------------------------------------------------------
# MÓDULO 3 — INTERFACE PRINCIPAL
# -----------------------------------------------------------------------

def prever_jogo(
    time_a: str,
    time_b: str,
    df_selecoes: pd.DataFrame,
) -> dict:
    """
    Gera a previsão completa para um confronto.

    Parâmetros:
        time_a      : nome do time A
        time_b      : nome do time B
        df_selecoes : DataFrame com índices de força e dados das seleções

    Retorna:
        Dicionário com probabilidades, placares e metadados
    """
    dados_a = df_selecoes[df_selecoes["selecao"] == time_a]
    dados_b = df_selecoes[df_selecoes["selecao"] == time_b]

    if dados_a.empty or dados_b.empty:
        times_faltando = []
        if dados_a.empty:
            times_faltando.append(time_a)
        if dados_b.empty:
            times_faltando.append(time_b)
        raise ValueError(f"Time(s) não encontrado(s): {', '.join(times_faltando)}")

    forca_a = float(dados_a["indice_forca_100"].iloc[0])
    forca_b = float(dados_b["indice_forca_100"].iloc[0])
    sede_a  = bool(dados_a["pais_sede"].iloc[0])
    sede_b  = bool(dados_b["pais_sede"].iloc[0])

    lambda_a, lambda_b = calcular_gols_esperados(forca_a, forca_b, sede_a, sede_b)
    matriz   = matriz_probabilidades(lambda_a, lambda_b)
    resultado = calcular_probabilidades(matriz)

    return {
        "time_a":            time_a,
        "time_b":            time_b,
        "indice_forca_a":    round(forca_a, 1),
        "indice_forca_b":    round(forca_b, 1),
        "gols_esperados_a":  lambda_a,
        "gols_esperados_b":  lambda_b,
        "sede_a":            sede_a,
        "sede_b":            sede_b,
        **resultado,
        "gerado_em":         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def prever_fase_grupos(df_selecoes: pd.DataFrame, df_grupos: pd.DataFrame) -> pd.DataFrame:
    """
    Gera previsões para todos os jogos da fase de grupos.
    Cada grupo tem 4 times — 6 jogos por grupo, 72 jogos no total.
    """
    print("[Modelo] Gerando previsões da fase de grupos...")

    previsoes = []

    for grupo in df_grupos["grupo"].unique():
        times_grupo = df_grupos[df_grupos["grupo"] == grupo]["selecao"].tolist()

        for i in range(len(times_grupo)):
            for j in range(i + 1, len(times_grupo)):
                time_a = times_grupo[i]
                time_b = times_grupo[j]
                try:
                    previsao = prever_jogo(time_a, time_b, df_selecoes)
                    previsao["grupo"] = grupo
                    previsoes.append(previsao)
                except ValueError as e:
                    print(f"  ⚠️  Pulando {time_a} x {time_b}: {e}")

    df_previsoes = pd.DataFrame(previsoes)

    os.makedirs(DATA_PROCESSED, exist_ok=True)
    caminho = f"{DATA_PROCESSED}/previsoes_grupos.csv"
    df_previsoes.to_csv(caminho, index=False)
    print(f"[Modelo] {len(df_previsoes)} previsões salvas em: {caminho}")

    return df_previsoes


# -----------------------------------------------------------------------
# MÓDULO 4 — SIMULAÇÃO MONTE CARLO (classificação por grupo)
# -----------------------------------------------------------------------

def simular_classificacao_grupo(
    times: list,
    df_selecoes: pd.DataFrame,
    n_simulacoes: int = N_SIMULACOES
) -> pd.DataFrame:
    """
    Simula N vezes a fase de grupos para 4 times.
    Retorna a probabilidade de cada time classificar (1º ou 2º lugar).

    Monte Carlo: sorteia placares com base nas probabilidades de Poisson
    e acumula qual time se classifica em cada simulação.
    """
    contagem_classificados = {time: 0 for time in times}
    contagem_1o_lugar      = {time: 0 for time in times}

    confrontos = [
        (times[i], times[j])
        for i in range(len(times))
        for j in range(i + 1, len(times))
    ]

    for _ in range(n_simulacoes):
        pontos     = {time: 0 for time in times}
        saldo_gols = {time: 0 for time in times}

        for time_a, time_b in confrontos:
            try:
                dados_a = df_selecoes[df_selecoes["selecao"] == time_a]
                dados_b = df_selecoes[df_selecoes["selecao"] == time_b]

                if dados_a.empty or dados_b.empty:
                    continue

                forca_a = float(dados_a["indice_forca_100"].iloc[0])
                forca_b = float(dados_b["indice_forca_100"].iloc[0])
                sede_a  = bool(dados_a["pais_sede"].iloc[0])
                sede_b  = bool(dados_b["pais_sede"].iloc[0])

                lambda_a, lambda_b = calcular_gols_esperados(
                    forca_a, forca_b, sede_a, sede_b
                )

                gols_a = np.random.poisson(lambda_a)
                gols_b = np.random.poisson(lambda_b)

                if gols_a > gols_b:
                    pontos[time_a] += 3
                elif gols_a < gols_b:
                    pontos[time_b] += 3
                else:
                    pontos[time_a] += 1
                    pontos[time_b] += 1

                saldo_gols[time_a] += gols_a - gols_b
                saldo_gols[time_b] += gols_b - gols_a

            except Exception:
                continue

        tabela = sorted(
            times,
            key=lambda t: (pontos[t], saldo_gols[t]),
            reverse=True
        )

        contagem_classificados[tabela[0]] += 1
        contagem_classificados[tabela[1]] += 1
        contagem_1o_lugar[tabela[0]] += 1

    return pd.DataFrame([
        {
            "selecao":          time,
            "prob_classificar": round(contagem_classificados[time] / n_simulacoes * 100, 1),
            "prob_1o_lugar":    round(contagem_1o_lugar[time]      / n_simulacoes * 100, 1),
        }
        for time in times
    ]).sort_values("prob_classificar", ascending=False)


# -----------------------------------------------------------------------
# MÓDULO 5 — VALIDAÇÃO HISTÓRICA (Copa 2022)
# -----------------------------------------------------------------------

def validar_modelo_copa2022(df_selecoes: pd.DataFrame) -> dict:
    """
    Valida o modelo contra os resultados reais da Copa 2022.
    Métrica: % de jogos onde o modelo acertou o vencedor.

    Nota metodológica: modelos de Poisson tipicamente atingem 50-60%
    de acurácia nessa métrica — acima de 50% já supera o acaso.
    """
    print("[Validação] Testando modelo contra Copa 2022...")

    jogos_2022 = [
        ("Argentina",      "Arábia Saudita",  1, 2),
        ("França",         "Austrália",        4, 1),
        ("Espanha",        "Costa Rica",       7, 0),
        ("Brasil",         "Sérvia",           2, 0),
        ("Portugal",       "Gana",             3, 2),
        ("Alemanha",       "Japão",            1, 2),
        ("França",         "Dinamarca",        2, 1),
        ("Brasil",         "Suíça",            1, 0),
        ("Argentina",      "México",           2, 0),
        ("Espanha",        "Alemanha",         1, 1),
        ("França",         "Polônia",          3, 1),
        ("Inglaterra",     "Senegal",          3, 0),
        ("Argentina",      "Austrália",        2, 1),
        ("Japão",          "Croácia",          1, 1),
        ("Brasil",         "Coreia do Sul",    4, 1),
        ("Marrocos",       "Espanha",          0, 0),
        ("Croácia",        "Brasil",           1, 1),
        ("Argentina",      "Holanda",          2, 2),
        ("França",         "Inglaterra",       2, 1),
        ("Marrocos",       "Portugal",         1, 0),
        ("Argentina",      "Croácia",          3, 0),
        ("França",         "Marrocos",         2, 0),
        ("Argentina",      "França",           3, 3),
    ]

    acertos = 0
    total   = 0
    detalhes = []

    for time_a, time_b, gols_a, gols_b in jogos_2022:
        try:
            prev = prever_jogo(time_a, time_b, df_selecoes)
        except ValueError:
            continue

        total += 1

        resultado_real = "A" if gols_a > gols_b else ("B" if gols_a < gols_b else "E")
        probs = {
            "A": prev["prob_vitoria_a"],
            "E": prev["prob_empate"],
            "B": prev["prob_vitoria_b"],
        }
        resultado_previsto = max(probs, key=probs.get)
        acerto = resultado_real == resultado_previsto
        if acerto:
            acertos += 1

        detalhes.append({
            "jogo":            f"{time_a} x {time_b}",
            "resultado_real":  f"{gols_a}-{gols_b}",
            "previsao_modelo": prev["placar_provavel"],
            "prob_a":          prev["prob_vitoria_a"],
            "prob_e":          prev["prob_empate"],
            "prob_b":          prev["prob_vitoria_b"],
            "acerto_vencedor": acerto,
        })

    acuracia = round(acertos / total * 100, 1) if total > 0 else 0
    print(f"[Validação] Acurácia: {acuracia}% ({acertos}/{total})")
    print(f"[Validação] Referência: modelos de Poisson tipicamente atingem 50-60%.")

    df_det = pd.DataFrame(detalhes)
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    df_det.to_csv(f"{DATA_PROCESSED}/validacao_copa2022.csv", index=False)

    return {"acuracia": acuracia, "acertos": acertos, "total": total, "detalhes": df_det}


# -----------------------------------------------------------------------
# EXECUÇÃO STANDALONE (teste direto)
# -----------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    caminho = f"{DATA_PROCESSED}/selecoes_com_pesos.csv"

    if os.path.exists(caminho):
        df_selecoes = pd.read_csv(caminho)
        print(f"✅ Dataset carregado: {len(df_selecoes)} seleções")
    else:
        print("⚠️  Fase 1 não executada. Usando dados mockados para demonstração.\n")
        df_selecoes = pd.DataFrame([
            {"selecao": "Brasil",         "indice_forca_100": 85.0, "pais_sede": False},
            {"selecao": "Argentina",      "indice_forca_100": 92.0, "pais_sede": False},
            {"selecao": "França",         "indice_forca_100": 90.0, "pais_sede": False},
            {"selecao": "Espanha",        "indice_forca_100": 88.0, "pais_sede": False},
            {"selecao": "Inglaterra",     "indice_forca_100": 84.0, "pais_sede": False},
            {"selecao": "Portugal",       "indice_forca_100": 83.0, "pais_sede": False},
            {"selecao": "Alemanha",       "indice_forca_100": 80.0, "pais_sede": False},
            {"selecao": "Marrocos",       "indice_forca_100": 70.0, "pais_sede": False},
            {"selecao": "Japão",          "indice_forca_100": 65.0, "pais_sede": False},
            {"selecao": "Estados Unidos", "indice_forca_100": 60.0, "pais_sede": True},
            {"selecao": "México",         "indice_forca_100": 58.0, "pais_sede": True},
            {"selecao": "Canadá",         "indice_forca_100": 55.0, "pais_sede": True},
            {"selecao": "Escócia",        "indice_forca_100": 55.0, "pais_sede": False},
            {"selecao": "Senegal",        "indice_forca_100": 63.0, "pais_sede": False},
            {"selecao": "Coreia do Sul",  "indice_forca_100": 62.0, "pais_sede": False},
            {"selecao": "Haiti",          "indice_forca_100": 30.0, "pais_sede": False},
            {"selecao": "Arábia Saudita", "indice_forca_100": 45.0, "pais_sede": False},
            {"selecao": "Croácia",        "indice_forca_100": 75.0, "pais_sede": False},
            {"selecao": "Holanda",        "indice_forca_100": 82.0, "pais_sede": False},
            {"selecao": "Austrália",      "indice_forca_100": 52.0, "pais_sede": False},
            {"selecao": "Polônia",        "indice_forca_100": 58.0, "pais_sede": False},
            {"selecao": "Suíça",          "indice_forca_100": 67.0, "pais_sede": False},
            {"selecao": "Dinamarca",      "indice_forca_100": 72.0, "pais_sede": False},
            {"selecao": "Gana",           "indice_forca_100": 40.0, "pais_sede": False},
            {"selecao": "Costa Rica",     "indice_forca_100": 42.0, "pais_sede": False},
            {"selecao": "Sérvia",         "indice_forca_100": 60.0, "pais_sede": False},
        ])

    print("\n" + "=" * 55)
    print(" FASE 2 — Demonstração do Modelo Preditivo")
    print("=" * 55)

    # Previsão: Brasil x França
    print("\n📊 Brasil x França")
    print("-" * 40)
    prev = prever_jogo("Brasil", "França", df_selecoes)
    print(f"  Índice de força  : Brasil {prev['indice_forca_a']} | França {prev['indice_forca_b']}")
    print(f"  Gols esperados   : Brasil {prev['gols_esperados_a']} | França {prev['gols_esperados_b']}")
    print(f"  Probabilidades   : Brasil {prev['prob_vitoria_a']}% | Empate {prev['prob_empate']}% | França {prev['prob_vitoria_b']}%")
    print(f"  Placar provável  : {prev['placar_provavel']} (prob: {prev['prob_placar']}%)")
    print(f"\n  Top 5 placares:")
    for p in prev["top5_placares"]:
        print(f"    {p['placar']}  →  {p['probabilidade']}%")

    # Previsão com fator sede
    print("\n📊 Estados Unidos x Alemanha (EUA = sede)")
    print("-" * 40)
    prev2 = prever_jogo("Estados Unidos", "Alemanha", df_selecoes)
    print(f"  Probabilidades   : EUA {prev2['prob_vitoria_a']}% | Empate {prev2['prob_empate']}% | Alemanha {prev2['prob_vitoria_b']}%")
    print(f"  Placar provável  : {prev2['placar_provavel']}")
    print(f"  (Bônus sede EUA: +{FATOR_SEDE_GOLS*100:.0f}% nos gols esperados)")

    # Validação histórica
    print("\n" + "=" * 55)
    print(" Validação — Copa 2022")
    print("=" * 55)
    val = validar_modelo_copa2022(df_selecoes)

    # Simulação Monte Carlo
    print("\n" + "=" * 55)
    print(" Simulação Monte Carlo — Grupo C (Brasil, Marrocos, Escócia, Haiti)")
    print("=" * 55)
    df_sim = simular_classificacao_grupo(
        ["Brasil", "Marrocos", "Escócia", "Haiti"],
        df_selecoes,
        n_simulacoes=5_000
    )
    print(df_sim.to_string(index=False))
