# 🏆 Copa do Mundo 2026 — Sistema de Previsão de Resultados

> Projeto de portfólio | Engenharia de Dados | Python + Streamlit

## Sobre o Projeto

Pipeline completo de dados para previsão de resultados da Copa do Mundo FIFA 2026 (EUA, México e Canadá — 11 jun a 19 jul).

O sistema coleta dados de múltiplas fontes, calcula um índice de força para cada seleção e gera probabilidades para cada confronto. Durante a competição, os resultados são atualizados automaticamente via GitHub Actions.

---

## Estrutura do Projeto

```
worldcup2026/
│
├── collectors/                  # Módulos de coleta de dados
│   ├── ranking_fifa.py          # Scraping do Ranking FIFA
│   └── selecoes_copa.py         # Seleções classificadas e grupos
│
├── processors/                  # Transformação e cálculo
│   └── calcular_pesos.py        # Índice de força das seleções
│
├── data/
│   ├── raw/                     # Dados brutos (CSV)
│   └── processed/               # Dados tratados (CSV)
│
├── .github/
│   └── workflows/
│       └── update_data.yml      # GitHub Actions — atualização automática
│
├── main_fase1.py                # Orquestrador Fase 1
├── config.py                    # Configurações centrais
├── requirements.txt
└── README.md
```

---

## Pipeline de Dados

```
[COLETA]                [PROCESSAMENTO]             [PRODUTO]
Ranking FIFA      →                             →
Eliminatórias     →   Índice de Força      →   Dashboard Streamlit
Grupos/Resultados →   Probabilidades       →   (ao vivo durante a Copa)
API-Football      →
```

---

## Fontes de Dados

| Fonte | Dados | Tipo de Acesso |
|---|---|---|
| FIFA (site oficial) | Ranking FIFA atualizado | Web scraping |
| football-data.org | Grupos, times, resultados | API gratuita (chave) |
| API-Football | Escalações, estatísticas ao vivo | API gratuita (limitado) |
| Dataset manual | Histórico Copa 2022, eliminatórias | CSV local |

---

## Metodologia — Índice de Força

O índice de força de cada seleção é calculado pela combinação ponderada de:

| Componente | Peso | Justificativa |
|---|---|---|
| Ranking FIFA | 50% | Métrica oficial que já pondera força de adversários e resultados recentes |
| Dificuldade das Eliminatórias | 30% | Seleções que passaram por fases mais competitivas têm maior preparo |
| Histórico Copa 2022 | 10% | Referência histórica (peso reduzido pela mudança de 32 para 48 seleções) |
| Fator sede | 10% | EUA, México e Canadá têm vantagem de torcida e adaptação logística |

---

## Decisões Arquiteturais

### Por que Streamlit e não Power BI?
O dashboard precisa ser acessível publicamente via link direto, sem licença, e atualizado com dados em tempo real durante a Copa. O Streamlit publicado no Streamlit Cloud atende todos esses requisitos de forma gratuita.

### Por que GitHub Actions para automação?
A coleta automática de resultados durante a Copa é implementada via GitHub Actions (cron job), eliminando a necessidade de servidor dedicado. O histórico de execuções fica visível no próprio repositório, demonstrando o pipeline em funcionamento.

### Por que não usar scraping de notícias + NLP para escalações?
Durante a avaliação do projeto, foi considerada a possibilidade de coletar escalações prováveis via scraping de portais esportivos (ge.globo, ESPN) combinado com processamento de linguagem natural (NLP) para extração das informações.

A abordagem foi descartada em favor da **API-Football** pelos seguintes motivos:
1. **Confiabilidade**: dados estruturados diretamente da fonte, sem risco de quebra por mudanças de layout HTML
2. **Manutenção**: durante a Copa, com jogos diários, um scraper frágil comprometeria a estabilidade do pipeline
3. **Precisão**: a API entrega escalações confirmadas ~1h antes do jogo — mais confiável que especulações de sites de notícias

A feature de análise de notícias está documentada como **evolução futura** do projeto.

---

## Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/worldcup2026

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure sua chave de API (opcional para Fase 1)
cp .env.example .env
# edite .env com sua chave do football-data.org

# 4. Execute a coleta inicial
python main_fase1.py
```

---

## Roadmap

- [x] **Fase 1** — Coleta base: ranking FIFA, seleções, grupos, índice de força
- [ ] **Fase 2** — Modelo preditivo: probabilidade por confronto, validação histórica
- [ ] **Fase 3** — Dashboard Streamlit: previsões interativas, publicação
- [ ] **Fase 4** — Ao vivo: atualização automática via GitHub Actions durante a Copa

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Pandas](https://img.shields.io/badge/Pandas-2.2-green)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-black)

---

*Projeto desenvolvido como parte de portfólio de transição de carreira para a área de dados.*
