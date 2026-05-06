# 🏆 WorldCup2026 — Previsão de Resultados em Tempo Real

> Pipeline preditivo para a Copa do Mundo FIFA 2026
> `Python` · `Streamlit` · `GitHub Actions` · `scikit-learn`

---

## O Problema

A Copa do Mundo FIFA 2026 começa em junho.
48 seleções. 104 jogos. Centenas de variáveis.

Modelos de previsão existem — mas a maioria para no resultado da fase de grupos.
Este não.

**O WorldCup2026 acompanha a Copa do início ao fim — e se atualiza sozinho.**

---

## A Pergunta Central

> **Quem vai ganhar — e o que os dados dizem sobre isso?**

---

## Como Funciona

O pipeline combina três camadas de inteligência:

**Camada 1 — Força das Seleções**
Índice de força calculado a partir de quatro componentes ponderados:

| Componente | Peso | Fonte |
|---|---|---|
| Ranking FIFA | 50% | API oficial FIFA |
| Desempenho nas Eliminatórias | 30% | football-data.org |
| Histórico em Copas | 10% | Dataset histórico |
| Fator sede | 10% | EUA · México · Canadá |

**Camada 2 — Modelo Preditivo**
Distribuição de Poisson para gols esperados por confronto + Simulação Monte Carlo para propagação do torneio. Validado contra os resultados reais da Copa 2022.

**Camada 3 — Atualização Automática**
GitHub Actions executa o pipeline diariamente durante a Copa. Resultados reais alimentam o modelo. Probabilidades se atualizam a cada rodada — sem intervenção manual.

---

## O Pipeline

```
[COLETA]
Python → API-Football + football-data.org + ranking FIFA
Dados de 48 seleções · eliminatórias · histórico

        ↓

[PROCESSAMENTO]
Índice de força (0–100) por seleção
Pesos: Ranking FIFA 50% · Eliminatórias 30% · Histórico 10% · Sede 10%

        ↓

[MODELO PREDITIVO]
Distribuição de Poisson → gols esperados por confronto
Simulação Monte Carlo → probabilidade de classificação por fase

        ↓

[ATUALIZAÇÃO AO VIVO]
GitHub Actions → execução diária durante a Copa
Resultados reais alimentam o modelo
Probabilidades recalculadas a cada rodada

        ↓

[DASHBOARD]
Streamlit Cloud → público · interativo · atualizado automaticamente
```

---

## Dashboard

O dashboard está publicado no Streamlit Cloud e acessível por qualquer pessoa via link.

**Páginas:**

| Página | Conteúdo |
|---|---|
| Visão Geral | Probabilidades de título por seleção |
| Grupos | Previsões e classificação esperada por grupo |
| Confrontos | Probabilidades jogo a jogo com placar provável |
| Simulação do Torneio | Monte Carlo — quem chega onde |
| Metodologia | Como o modelo funciona e como interpretar os resultados |

> 🔗 Link do dashboard: *disponível após publicação*

---

## Estrutura do Projeto

```
worldcup2026/
├── collectors/              ← coleta de dados via API
│   ├── ranking_fifa.py
│   ├── selecoes_copa.py
│   └── resultados_ao_vivo.py
├── processors/              ← cálculo de pesos e índice de força
│   └── calcular_pesos.py
├── models/                  ← modelo preditivo
│   └── modelo_preditivo.py
├── dashboard/               ← Streamlit
│   └── app.py
├── notebooks/               ← metodologia e validação
│   ├── 01_metodologia.ipynb
│   └── 02_validacao_copa2022.ipynb
├── data/
│   ├── raw/                 ← dados coletados
│   └── processed/           ← datasets tratados
└── .github/workflows/
    └── atualizacao_diaria.yml
```

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)

---

## Status do Projeto

| Milestone | Prazo | Status |
|---|---|---|
| 1 — Fundação e Coleta de Dados | 15/Mai/2026 | 🔄 Em andamento |
| 2 — Modelo Preditivo | 22/Mai/2026 | ⏳ Aguardando M1 |
| 3 — Dashboard Streamlit | 31/Mai/2026 | ⏳ Aguardando M2 |
| 4 — Automação e Atualização ao Vivo | 11/Jun/2026 | ⏳ Aguardando M3 |
| 5 — Documentação e Publicação | 05/Jun/2026 | ⏳ Paralelo ao M3 |
| 6 — Acompanhamento ao Vivo | 19/Jul/2026 | ⏳ Durante a Copa |

---

## Como Executar Localmente

```bash
pip install -r requirements.txt

# Fase 1 — coleta e índice de força
python main_fase1.py

# Fase 2 — modelo preditivo
python main_fase2.py

# Dashboard
streamlit run dashboard/app.py
```

> ⚠️ Necessário criar conta gratuita em football-data.org e API-Football (RapidAPI) e configurar as chaves em `.env`.
> Consulte `.env.example` para o formato esperado.

---

## Sobre

Projeto desenvolvido pela **Lufi Data Consulting** como parte do portfólio de transição de carreira para dados.

Engenheiro de Produção com 10 anos de experiência em operações, processos e análise administrativa — agora usando dados como ferramenta de decisão de negócio.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/filholuiz)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/DataLufi)

---

*Previsões geradas por modelo estatístico — não constituem certeza de resultado.*
*Dados coletados de fontes públicas: FIFA, football-data.org, API-Football.*
