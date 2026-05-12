# 🏆 Copa do Mundo 2026 — Sistema de Previsão de Resultados

> ⚠️ **Este repositório está arquivado.** Veja o contexto completo abaixo.

---

## Status: Arquivado — Maio/2026

Este projeto foi desenvolvido para aproveitar a janela da Copa do Mundo 2026 com um pipeline completo de dados para previsão de resultados — coleta de dados, modelo preditivo e dashboard interativo ao vivo.

Durante o desenvolvimento, múltiplos problemas com as APIs de dados de futebol (instabilidade de autenticação, rate limits restritivos, dados incompletos no período pré-Copa) tornaram o pipeline dependente de scraping frágil e fallbacks manuais, incompatíveis com o cronograma disponível antes de 11 de junho.

A decisão foi consolidar os objetivos técnicos deste projeto — **Streamlit público**, **GitHub Actions** e **dado dinâmico** — no projeto **Prisma**, que já tinha essas camadas planejadas e em desenvolvimento ativo, com narrativa de negócio mais robusta e sem dependência de API externa instável.

Repositório mantido como registro de decisão estratégica e de todo o trabalho desenvolvido até o ponto de pivô.

---

## O que foi construído antes do arquivamento

A Fase 1 foi **completamente concluída** e a Fase 2 **implementada e validada**:

### ✅ Fase 1 — Coleta e Processamento Base
- Pipeline de coleta do Ranking FIFA com scraping + fallback para football-data.org + fallback interno com dados reais de abril/2026
- Dataset completo das **48 seleções classificadas** — lista final pós-repescagem (31/03/2026), incluindo UEFA (16), CONMEBOL (6), CONCACAF (6), CAF (10), AFC (9) e OFC (1)
- **12 grupos oficiais** mapeados com o sorteio FIFA de dezembro/2025
- Índice de força (0–100) calculado para cada seleção com ponderação: Ranking FIFA (50%), Dificuldade das eliminatórias (30%), Histórico Copa 2022 (10%), Fator sede (10%)
- Notebook didático `fase1_coleta_base.ipynb` com análise exploratória e gráficos interativos

### ✅ Fase 2 — Modelo Preditivo
- Modelo baseado em **distribuição de Poisson** (Dixon & Coles, 1997) — referência acadêmica clássica para previsão de resultados de futebol
- Previsão de **probabilidade de vitória/empate/derrota** e **placar mais provável** para cada confronto
- **Top 5 placares** com respectivas probabilidades por jogo
- **Simulação Monte Carlo** (5.000–10.000 iterações) para estimar probabilidade de classificação por grupo
- Validação retroativa contra resultados reais da Copa 2022 — acurácia de **52–58%** (referência de mercado para modelos de Poisson: 50–60%)
- Notebook didático `fase2_modelo_preditivo.ipynb` com visualizações interativas

### ✅ Gestão do Projeto
- **GitHub Projects** estruturado com 6 milestones, 31 issues e roadmap visual completo
- Issues #1 a #5 (Fase 1) **fechadas com entrega**
- Decisões arquiteturais documentadas (ver seção abaixo)

---

## Decisões Técnicas Documentadas

Este projeto serviu também como exercício de decisão arquitetural. As escolhas abaixo foram deliberadas e documentadas:

**Streamlit vs Power BI**
Dashboard precisava ser acessível via link público, sem licença, com dados em tempo real durante a Copa. Streamlit Cloud atende todos esses requisitos gratuitamente.

**GitHub Actions vs servidor dedicado**
Automação de coleta de dados implementada como cron job no GitHub Actions — sem custo de servidor, com histórico de execuções visível no repositório como evidência do pipeline em funcionamento.

**API-Sports direto vs RapidAPI**
Cadastro direto em `dashboard.api-sports.io` (header: `x-apisports-key`) — mais estável e sem intermediário. RapidAPI apresentou instabilidade durante o desenvolvimento.

**Sem scraping de notícias + NLP para escalações**
Avaliado e descartado em favor da API-Sports: dados estruturados entregues diretamente pela fonte, sem risco de quebra por mudança de HTML. Durante a Copa, com jogos diários, um scraper frágil comprometeria a estabilidade do pipeline. Documentado como evolução futura.

**Ranking FIFA vs resultado da Copa anterior**
A Copa 2026 tem 48 seleções (vs. 32 em 2022), tornando a comparação direta de colocações inválida. O Ranking FIFA já pondera força de adversários e resultados recentes — é a métrica mais robusta disponível.

---

## Por que arquivar e não deletar

Deletar seria esconder. Arquivar é documentar.

Este repositório representa:
- Decisão estratégica tomada com base em dados (cronograma vs. dependência técnica instável), não em ego
- Gestão de risco real: identificar que um componente do pipeline compromete a entrega e redirecionar o esforço
- Evidência de raciocínio por escrito — habilidade valorizada em times de dados

O código existente demonstra estrutura de projeto Python, tentativa de integração com API externa, modelagem estatística com Poisson e Monte Carlo, e organização de repositório profissional.

---

## Stack utilizada

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![SciPy](https://img.shields.io/badge/SciPy-Poisson-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-planejado-red)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-planejado-black)

---

## Projeto substituto

Os objetivos técnicos deste projeto — Streamlit público, GitHub Actions e dado dinâmico — foram absorvidos pelo **[Projeto Prisma](https://github.com/DataLufi)**, que entrega a mesma demonstração de stack com narrativa de negócio mais robusta e sem dependência de API externa instável.

---

[![GitHub](https://img.shields.io/badge/GitHub-DataLufi-black?logo=github)](https://github.com/DataLufi)

*Projeto de portfólio — transição de carreira para a área de dados.*
*Arquivado em maio/2026 após decisão estratégica de consolidação de stack.*
