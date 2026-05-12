# 🏆 Projeto FIFA — Planejamento Completo para GitHub Projects

> **Repositório:** `worldcup2026`
> **Descrição do projeto:** Pipeline completo de dados para previsão de resultados da Copa do Mundo FIFA 2026 — coleta, modelagem, dashboard e atualização automática ao vivo.
> **Período:** Mai/2026 → Jul/2026

---

## Como usar este documento no GitHub Projects

1. Crie um novo repositório chamado `worldcup2026`
2. Vá em **Projects → New Project → Board** (estilo Kanban)
3. Crie as colunas: `Backlog | Em andamento | Em revisão | Concluído`
4. Vá em **Milestones** e crie cada fase abaixo como um Milestone com a data de entrega
5. Para cada item de issue abaixo, crie uma **Issue** no repositório associando ao Milestone correspondente
6. No GitHub Projects, adicione as issues ao board

---

---

# MILESTONE 1 — Fundação e Coleta de Dados
**Prazo:** 15/Mai/2026
**Objetivo:** Ter o ambiente configurado e os dados base de todas as 48 seleções prontos para alimentar o modelo.
**Entregável:** Dataset `selecoes_com_pesos.csv` gerado e validado.

---

## Issue #1 — Setup do ambiente de desenvolvimento
**Labels:** `setup` `infra`
**Prioridade:** 🔴 Alta
**Descrição:**
Configurar todo o ambiente local e repositório GitHub para o projeto.

**Subtarefas:**
- [ ] Criar repositório `worldcup2026` no GitHub (público)
- [ ] Executar `setup_projeto.ipynb` célula a célula e confirmar que todas passam sem erro
- [ ] Verificar criação de todas as pastas: `data/raw`, `data/processed`, `data/resultados`, `collectors`, `processors`, `models`, `dashboard`, `notebooks`, `.github/workflows`
- [ ] Criar conta gratuita em football-data.org e obter chave de API
- [ ] Criar conta gratuita em API-Football (RapidAPI) e obter chave de API
- [ ] Preencher chaves no arquivo `.env` e confirmar que `config.py` lê corretamente
- [ ] Confirmar que `.env` está no `.gitignore` e NÃO aparece no `git status`
- [ ] Fazer primeiro commit com a estrutura inicial do projeto
- [ ] Escrever descrição do repositório e adicionar tópicos: `python`, `data-science`, `fifa`, `world-cup`, `streamlit`, `machine-learning`

**Critério de aceite:** `python main_fase1.py` roda sem erros de importação.

---

## Issue #2 — Coleta do Ranking FIFA
**Labels:** `coleta` `dados`
**Prioridade:** 🔴 Alta
**Descrição:**
Implementar e validar a coleta do Ranking FIFA oficial com fallback para API pública.

**Subtarefas:**
- [ ] Executar `collectors/ranking_fifa.py` e verificar o retorno
- [ ] Se scraping do site FIFA falhar, testar `coletar_ranking_via_api_publica()` com a chave do football-data.org
- [ ] Confirmar que o arquivo `data/raw/ranking_fifa_YYYYMMDD.csv` é gerado
- [ ] Validar que o DataFrame contém colunas: `posicao`, `selecao`, `pontos`, `pais_codigo`
- [ ] Verificar se as top 10 seleções do ranking real estão presentes e na ordem correta
- [ ] Documentar no código qual fonte foi usada (scraping ou API) e por quê

**Critério de aceite:** CSV gerado com no mínimo 48 seleções e ranking FIFA reconhecível.

---

## Issue #3 — Dataset das 48 seleções classificadas
**Labels:** `coleta` `dados`
**Prioridade:** 🔴 Alta
**Descrição:**
Montar e validar o dataset base com todas as seleções classificadas para a Copa 2026.

**Subtarefas:**
- [ ] Verificar lista de seleções classificadas em `collectors/selecoes_copa.py` contra a lista oficial da FIFA
- [ ] Atualizar as vagas marcadas como "A confirmar" conforme divulgação oficial
- [ ] Confirmar confederação de cada seleção (UEFA, CONMEBOL, CONCACAF, CAF, AFC, OFC)
- [ ] Validar flags de país-sede: EUA, México e Canadá marcados como `pais_sede = True`
- [ ] Confirmar que os grupos disponíveis em `coletar_grupos_copa()` estão corretos
- [ ] Atualizar grupos que ainda não foram divulgados assim que a FIFA anunciar
- [ ] Salvar `data/raw/selecoes_classificadas.csv` e revisar manualmente

**Critério de aceite:** 48 seleções no CSV, sem duplicatas, todas com confederação preenchida.

---

## Issue #4 — Cálculo do índice de força (pesos)
**Labels:** `processamento` `modelo`
**Prioridade:** 🔴 Alta
**Descrição:**
Cruzar ranking FIFA com dados das eliminatórias para gerar o índice de força (0-100) de cada seleção.

**Subtarefas:**
- [ ] Executar `processors/calcular_pesos.py` com os dados coletados nas issues #2 e #3
- [ ] Verificar se o merge entre ranking FIFA e dataset de seleções está correto (sem muitos NaN)
- [ ] Analisar o top 10 do índice de força e comparar com o senso comum (Argentina, França, Brasil devem estar no topo)
- [ ] Validar os pesos aplicados: Ranking FIFA 50%, Eliminatórias 30%, Histórico 10%, Sede 10%
- [ ] Verificar se países-sede (EUA, MEX, CAN) estão recebendo o bônus corretamente
- [ ] Confirmar geração de `data/processed/selecoes_com_pesos.csv`
- [ ] Fazer análise exploratória rápida: distribuição do índice por confederação

**Critério de aceite:** `selecoes_com_pesos.csv` gerado com coluna `indice_forca_100` entre 0 e 100 para todas as seleções.

---

## Issue #5 — Execução e validação do pipeline completo (Fase 1)
**Labels:** `validação` `pipeline`
**Prioridade:** 🟡 Média
**Descrição:**
Garantir que o pipeline completo da Fase 1 roda do início ao fim sem intervenção manual.

**Subtarefas:**
- [ ] Executar `python main_fase1.py` do zero (sem arquivos em `data/`) e confirmar que todos os CSVs são gerados
- [ ] Verificar se o fallback funciona: testar com chave de API inválida e confirmar que o modo offline entra
- [ ] Conferir os 4 CSVs gerados: `ranking_fifa`, `selecoes_classificadas`, `grupos_copa2026`, `selecoes_com_pesos`
- [ ] Fazer commit de todos os arquivos (exceto `.env` e `data/raw/*.csv` se forem grandes)
- [ ] Abrir Pull Request da branch `fase1` para `main` e fazer merge

**Critério de aceite:** `main_fase1.py` executa em menos de 2 minutos e gera todos os arquivos esperados.

---

---

# MILESTONE 2 — Modelo Preditivo
**Prazo:** 22/Mai/2026
**Objetivo:** Ter o modelo de previsão funcionando, validado e gerando probabilidades + placares para todos os jogos da fase de grupos.
**Entregável:** `previsoes_grupos.csv` e `simulacao_classificacao.csv` gerados e validados.

---

## Issue #6 — Implementação do modelo de Poisson
**Labels:** `modelo` `ciência-de-dados`
**Prioridade:** 🔴 Alta
**Descrição:**
Validar e testar os módulos do modelo preditivo baseado em distribuição de Poisson.

**Subtarefas:**
- [ ] Executar `python models/modelo_preditivo.py` em modo standalone e verificar output
- [ ] Confirmar que `calcular_gols_esperados()` retorna valores plausíveis (entre 0.5 e 2.5 gols por time)
- [ ] Verificar que a matriz de probabilidades soma ~100% (pode ter pequeno resíduo por truncamento no teto de 6 gols)
- [ ] Testar `prever_jogo()` para pelo menos 5 confrontos diferentes e analisar se as probabilidades fazem sentido
- [ ] Confirmar que o fator sede aumenta os gols esperados do país-sede (+15%)
- [ ] Testar confronto entre times de índice muito diferente (ex: Argentina x Haiti) e verificar se a probabilidade é alta o suficiente para o favorito (esperado: >85%)
- [ ] Testar confronto equilibrado (ex: França x Brasil) e verificar se as probabilidades são próximas

**Critério de aceite:** `prever_jogo("Brasil", "França", df)` retorna dicionário completo com probabilidades somando 100%.

---

## Issue #7 — Validação histórica contra Copa 2022
**Labels:** `validação` `modelo`
**Prioridade:** 🔴 Alta
**Descrição:**
Executar a validação do modelo contra os resultados reais da Copa 2022 e documentar a acurácia.

**Subtarefas:**
- [ ] Executar `validar_modelo_copa2022()` e registrar a acurácia obtida
- [ ] Verificar se a acurácia está acima de 50% (linha de base — melhor que aleatório)
- [ ] Analisar os jogos onde o modelo errou: existem padrões? (zebras, jogos equilibrados?)
- [ ] Documentar no README a acurácia obtida e a referência de mercado (50–60%)
- [ ] Salvar `data/processed/validacao_copa2022.csv` e commitar
- [ ] Se acurácia < 50%: revisar os pesos do índice de força e re-executar

**Critério de aceite:** Acurácia ≥ 50% documentada com print do resultado.

---

## Issue #8 — Previsões da fase de grupos
**Labels:** `modelo` `dados`
**Prioridade:** 🔴 Alta
**Descrição:**
Gerar previsões para todos os 72 jogos da fase de grupos (12 grupos × 6 jogos cada).

**Subtarefas:**
- [ ] Confirmar que todos os 12 grupos estão preenchidos em `data/raw/grupos_copa2026.csv`
- [ ] Executar `prever_fase_grupos()` e verificar que 72 jogos foram gerados
- [ ] Analisar o CSV `previsoes_grupos.csv`: verificar que há colunas de probabilidade, placar provável e top 5 placares
- [ ] Identificar os 5 jogos com maior probabilidade de zebra (favorito com menos de 55%)
- [ ] Identificar os 5 jogos mais desequilibrados (favorito com mais de 85%)
- [ ] Commitar `data/processed/previsoes_grupos.csv`

**Critério de aceite:** 72 linhas no CSV, sem valores nulos nas colunas principais.

---

## Issue #9 — Simulação Monte Carlo dos grupos
**Labels:** `modelo` `simulação`
**Prioridade:** 🟡 Média
**Descrição:**
Simular 10.000 vezes cada grupo para calcular a probabilidade de classificação de cada seleção.

**Subtarefas:**
- [ ] Executar `simular_classificacao_grupo()` para todos os 12 grupos
- [ ] Verificar que a soma de `prob_classificar` por grupo é ~200% (2 times se classificam)
- [ ] Identificar as 5 seleções com maior probabilidade de se classificar
- [ ] Identificar as 5 seleções com menor probabilidade (candidatas a zebra)
- [ ] Salvar `data/processed/simulacao_classificacao.csv`
- [ ] Comparar resultado da simulação com o senso comum do futebol

**Critério de aceite:** Todos os 12 grupos simulados, Brasil e Argentina com >70% de probabilidade de classificar.

---

## Issue #10 — Notebook de metodologia (portfólio)
**Labels:** `documentação` `portfólio`
**Prioridade:** 🟡 Média
**Descrição:**
Revisar e enriquecer o notebook `fase2_metodologia.ipynb` para uso no portfólio.

**Subtarefas:**
- [ ] Executar todas as células do notebook e confirmar que os gráficos aparecem corretamente
- [ ] Verificar se o heatmap da matriz de placares está legível e bem formatado
- [ ] Adicionar célula de conclusão com interpretação dos resultados
- [ ] Adicionar comentários explicativos em cada célula (para quem não conhece o modelo)
- [ ] Exportar o notebook como HTML para publicação fácil (`jupyter nbconvert --to html`)
- [ ] Commitar notebook e HTML gerado

**Critério de aceite:** Notebook executa do início ao fim sem erros com `Kernel → Restart & Run All`.

---

## Issue #11 — Execução e validação do pipeline completo (Fase 2)
**Labels:** `validação` `pipeline`
**Prioridade:** 🟡 Média
**Descrição:**
Garantir que `main_fase2.py` encadeia corretamente todas as etapas da Fase 2.

**Subtarefas:**
- [ ] Executar `python main_fase2.py` após ter os dados da Fase 1
- [ ] Confirmar geração de `previsoes_grupos.csv`, `simulacao_classificacao.csv` e `validacao_copa2022.csv`
- [ ] Verificar que o resumo final do script está correto
- [ ] Abrir Pull Request da branch `fase2` para `main` e fazer merge

**Critério de aceite:** `main_fase2.py` executa sem erros e exibe resumo no terminal.

---

---

# MILESTONE 3 — Dashboard Streamlit
**Prazo:** 31/Mai/2026
**Objetivo:** Dashboard publicado online, acessível por qualquer pessoa via link, com visual profissional e todas as previsões interativas.
**Entregável:** Link público do Streamlit Cloud funcionando.

---

## Issue #12 — Estrutura base do dashboard
**Labels:** `dashboard` `streamlit`
**Prioridade:** 🔴 Alta
**Descrição:**
Criar a estrutura inicial do dashboard Streamlit com navegação entre páginas.

**Subtarefas:**
- [ ] Criar `dashboard/app.py` como ponto de entrada do Streamlit
- [ ] Implementar menu de navegação lateral com as seções: Visão Geral, Grupos, Confrontos, Simulação, Metodologia
- [ ] Criar função de carregamento de dados com cache (`@st.cache_data`) para não recarregar CSVs a cada interação
- [ ] Implementar tratamento de erro caso os CSVs não existam (mensagem amigável ao usuário)
- [ ] Testar localmente com `streamlit run dashboard/app.py`

**Critério de aceite:** Dashboard abre no browser local sem erros.

---

## Issue #13 — Página: Visão Geral
**Labels:** `dashboard` `streamlit`
**Prioridade:** 🔴 Alta
**Descrição:**
Página inicial com ranking das seleções e métricas gerais da Copa.

**Subtarefas:**
- [ ] Exibir cards com métricas: total de seleções, grupos, jogos previstos
- [ ] Gráfico de barras horizontal com top 20 seleções por índice de força (colorido por confederação)
- [ ] Tabela interativa com todas as 48 seleções ordenada por índice de força
- [ ] Filtro por confederação
- [ ] Exibir data da última atualização dos dados

**Critério de aceite:** Página carrega em menos de 3 segundos e o gráfico é interativo.

---

## Issue #14 — Página: Grupos
**Labels:** `dashboard` `streamlit`
**Prioridade:** 🔴 Alta
**Descrição:**
Página com visualização de todos os grupos e probabilidades de classificação.

**Subtarefas:**
- [ ] Selector de grupo (A até L)
- [ ] Para cada grupo: exibir tabela com as 4 seleções, índice de força e probabilidade de classificar
- [ ] Gráfico de barras com probabilidade de classificação e 1º lugar por seleção
- [ ] Exibir os 6 jogos do grupo com placar provável e probabilidades (estilo grade de confrontos)
- [ ] Destacar visualmente o favorito de cada confronto

**Critério de aceite:** Trocar o seletor de grupo atualiza todos os elementos da página corretamente.

---

## Issue #15 — Página: Confrontos
**Labels:** `dashboard` `streamlit`
**Prioridade:** 🔴 Alta
**Descrição:**
Página para o usuário simular qualquer confronto entre duas seleções.

**Subtarefas:**
- [ ] Dois seletores de seleção (Time A × Time B)
- [ ] Botão "Simular confronto"
- [ ] Exibir probabilidades em gauge ou barras horizontais estilo comparação
- [ ] Exibir placar mais provável em destaque visual
- [ ] Exibir top 5 placares com barra de probabilidade de cada um
- [ ] Exibir gols esperados por time
- [ ] Exibir índice de força de cada time lado a lado

**Critério de aceite:** Qualquer combinação de duas seleções gera previsão sem erro.

---

## Issue #16 — Página: Simulação do torneio
**Labels:** `dashboard` `streamlit`
**Prioridade:** 🟡 Média
**Descrição:**
Página com resultado agregado das simulações Monte Carlo de todos os grupos.

**Subtarefas:**
- [ ] Tabela geral com probabilidade de classificação de todas as 48 seleções
- [ ] Gráfico de bolhas ou treemap colorido por confederação
- [ ] Filtro por confederação para comparar chances regionais
- [ ] Destacar os países-sede com ícone ou cor diferente

**Critério de aceite:** Tabela exibe todas as 48 seleções com probabilidade de classificar.

---

## Issue #17 — Página: Metodologia
**Labels:** `dashboard` `documentação`
**Prioridade:** 🟡 Média
**Descrição:**
Página explicando a metodologia do projeto de forma didática (voltada para recrutadores e interessados).

**Subtarefas:**
- [ ] Seção: "Como funciona o modelo" com texto explicativo e diagrama do pipeline
- [ ] Seção: "Fontes de dados" com tabela de APIs usadas
- [ ] Seção: "Decisões técnicas" com as justificativas documentadas (Poisson, Streamlit vs Power BI, GitHub Actions, API-Football vs scraping de notícias)
- [ ] Seção: "Acurácia do modelo" com o resultado da validação Copa 2022
- [ ] Link para o repositório GitHub e para o notebook de metodologia
- [ ] Seção: "Sobre o autor" com breve apresentação e links (LinkedIn, GitHub)

**Critério de aceite:** Página legível e sem jargão excessivo — um não-técnico deve entender o projeto.

---

## Issue #18 — Identidade visual e responsividade
**Labels:** `dashboard` `design`
**Prioridade:** 🟡 Média
**Descrição:**
Garantir que o dashboard tem uma identidade visual consistente e funciona bem em diferentes tamanhos de tela.

**Subtarefas:**
- [ ] Definir paleta de cores do projeto (sugestão: verde/amarelo/azul Brasil ou tons neutros com destaque em verde FIFA)
- [ ] Adicionar logo ou título estilizado no header
- [ ] Configurar `theme` no `.streamlit/config.toml`
- [ ] Testar em resolução desktop (1920×1080) e notebook (1366×768)
- [ ] Verificar se tabelas têm scroll horizontal quando necessário
- [ ] Adicionar favicon da Copa do Mundo

**Critério de aceite:** Dashboard visualmente consistente, sem elementos "padrão cinza" do Streamlit sem customização.

---

## Issue #19 — Publicação no Streamlit Cloud
**Labels:** `deploy` `infra`
**Prioridade:** 🔴 Alta
**Descrição:**
Publicar o dashboard online de forma gratuita e acessível por qualquer pessoa.

**Subtarefas:**
- [ ] Criar conta em share.streamlit.io (gratuito)
- [ ] Conectar repositório GitHub ao Streamlit Cloud
- [ ] Configurar `requirements.txt` com todas as dependências (confirmar que não há biblioteca faltando)
- [ ] Adicionar variáveis de ambiente (chaves de API) nas configurações do Streamlit Cloud (Secrets)
- [ ] Fazer deploy e confirmar que o link público funciona
- [ ] Testar todas as páginas no link público
- [ ] Adicionar o link público no README do repositório

**Critério de aceite:** Link público funciona sem login e carrega em menos de 10 segundos.

---

## Issue #20 — Testes de regressão do dashboard
**Labels:** `validação` `dashboard`
**Prioridade:** 🟢 Baixa
**Descrição:**
Garantir que o dashboard não quebra em cenários de borda.

**Subtarefas:**
- [ ] Testar seleção do mesmo time nos dois lados do confronto (ex: Brasil x Brasil)
- [ ] Testar com CSVs vazios ou corrompidos — dashboard deve mostrar mensagem de erro amigável
- [ ] Testar em modo mobile (Chrome DevTools → toggle device)
- [ ] Verificar que todos os gráficos têm título e labels legíveis
- [ ] Verificar que não há valores `NaN` visíveis ao usuário final

**Critério de aceite:** Nenhum erro `Exception` exposto ao usuário em nenhum cenário testado.

---

---

# MILESTONE 4 — Automação e Atualização ao Vivo
**Prazo:** 11/Jun/2026 (início da Copa)
**Objetivo:** Pipeline totalmente automatizado rodando via GitHub Actions, alimentando o dashboard com resultados reais durante a Copa.
**Entregável:** GitHub Actions executando com sucesso e dashboard atualizando automaticamente.

---

## Issue #21 — Coletor de resultados ao vivo (API-Football)
**Labels:** `coleta` `fase4` `automação`
**Prioridade:** 🔴 Alta
**Descrição:**
Criar o módulo que coleta resultados dos jogos em tempo real via API-Football.

**Subtarefas:**
- [ ] Criar `collectors/resultados_ao_vivo.py`
- [ ] Implementar coleta de jogos do dia via endpoint `/fixtures` da API-Football
- [ ] Implementar coleta de estatísticas por jogo via endpoint `/fixtures/statistics`
- [ ] Implementar coleta de escalações via endpoint `/fixtures/lineups`
- [ ] Salvar resultados em `data/resultados/resultados_YYYYMMDD.csv`
- [ ] Implementar lógica de não duplicar resultados já coletados
- [ ] Testar com jogo passado para validar o formato dos dados

**Critério de aceite:** Script coleta resultado de um jogo real da API e salva no CSV corretamente.

---

## Issue #22 — Atualização automática de probabilidades
**Labels:** `modelo` `fase4`
**Prioridade:** 🔴 Alta
**Descrição:**
Após cada jogo, atualizar as probabilidades dos jogos futuros com base nos resultados reais.

**Subtarefas:**
- [ ] Criar `processors/atualizar_probabilidades.py`
- [ ] Implementar lógica de "forma recente": times que venceram ganham bônus no índice de força
- [ ] Implementar penalização por derrota
- [ ] Recalcular classificação dos grupos com resultados reais acumulados
- [ ] Recalcular probabilidades do mata-mata conforme os classificados forem definidos
- [ ] Salvar índice de força atualizado em `data/processed/selecoes_com_pesos_atualizado.csv`

**Critério de aceite:** Após simular uma vitória do Brasil, o índice de força do Brasil aumenta e as probabilidades dos próximos jogos são recalculadas.

---

## Issue #23 — GitHub Actions: pipeline de coleta automática
**Labels:** `infra` `ci-cd` `fase4`
**Prioridade:** 🔴 Alta
**Descrição:**
Configurar o GitHub Actions para rodar a coleta automaticamente 2x ao dia durante a Copa.

**Subtarefas:**
- [ ] Revisar `.github/workflows/update_data.yml` gerado na Fase 1
- [ ] Adicionar step de coleta de resultados ao vivo (`resultados_ao_vivo.py`)
- [ ] Adicionar step de atualização de probabilidades (`atualizar_probabilidades.py`)
- [ ] Configurar os Secrets no GitHub: `API_FOOTBALL_KEY` e `FOOTBALL_DATA_KEY`
- [ ] Fazer primeiro `workflow_dispatch` manual e confirmar que roda sem erro
- [ ] Verificar que o commit automático dos dados aparece no histórico do repositório
- [ ] Configurar notificação de falha por email (GitHub Settings → Notifications)

**Critério de aceite:** Workflow roda manualmente com sucesso e commita arquivos atualizados.

---

## Issue #24 — Dashboard: seção de resultados ao vivo
**Labels:** `dashboard` `fase4`
**Prioridade:** 🔴 Alta
**Descrição:**
Adicionar ao dashboard a seção de resultados reais e comparação com as previsões.

**Subtarefas:**
- [ ] Criar página "Resultados" no dashboard
- [ ] Exibir tabela de jogos já realizados com: data, placar real, placar previsto, probabilidade prevista
- [ ] Destacar visualmente quando o modelo acertou o vencedor
- [ ] Calcular e exibir acurácia acumulada durante a Copa (% de acertos até o momento)
- [ ] Exibir próximos jogos com previsões
- [ ] Atualizar automaticamente ao recarregar a página (dados vêm do CSV mais recente)

**Critério de aceite:** Após o primeiro jogo da Copa, a página de resultados exibe o placar real e a comparação com a previsão.

---

## Issue #25 — Monitoramento e alertas do pipeline
**Labels:** `infra` `monitoramento`
**Prioridade:** 🟡 Média
**Descrição:**
Garantir que falhas no pipeline sejam detectadas rapidamente.

**Subtarefas:**
- [ ] Implementar logging estruturado nos scripts de coleta (`logging` do Python)
- [ ] Salvar logs em `logs/coleta_YYYYMMDD.log`
- [ ] Adicionar step no GitHub Actions que verifica se o CSV de resultados foi atualizado
- [ ] Configurar GitHub Actions para falhar (e notificar) se a API retornar erro
- [ ] Adicionar badge de status do workflow no README (`![workflow](link_do_badge)`)

**Critério de aceite:** Badge de status aparece no README e fica verde após workflow bem-sucedido.

---

---

# MILESTONE 5 — Documentação e Publicação do Portfólio
**Prazo:** 05/Jun/2026 (antes do início da Copa)
**Objetivo:** Projeto completamente documentado, com README profissional e pronto para ser apresentado em entrevistas e divulgado no LinkedIn.
**Entregável:** README completo, notebooks organizados e post de divulgação redigido.

---

## Issue #26 — README profissional
**Labels:** `documentação` `portfólio`
**Prioridade:** 🔴 Alta
**Descrição:**
Escrever o README definitivo do projeto — principal ponto de contato de recrutadores com o repositório.

**Subtarefas:**
- [ ] Adicionar GIF ou screenshot do dashboard no topo do README
- [ ] Seção "Sobre o projeto": o que é, o que faz, por que foi criado
- [ ] Seção "Demo": link direto para o Streamlit Cloud
- [ ] Seção "Pipeline": diagrama ASCII ou imagem do fluxo de dados
- [ ] Seção "Fontes de dados": tabela com APIs usadas
- [ ] Seção "Metodologia": resumo do modelo de Poisson e Monte Carlo
- [ ] Seção "Decisões técnicas": justificativas documentadas (Streamlit vs Power BI, API-Football vs scraping de notícias, GitHub Actions)
- [ ] Seção "Acurácia do modelo": resultado da validação Copa 2022
- [ ] Seção "Como executar": passo a passo para rodar localmente
- [ ] Seção "Roadmap": próximas features planejadas
- [ ] Badges no topo: Python version, Streamlit, License, workflow status
- [ ] Adicionar seção "Sobre o autor" com links para LinkedIn e GitHub

**Critério de aceite:** README lido por uma pessoa não-técnica deve ser entendido em menos de 3 minutos.

---

## Issue #27 — Organização dos notebooks
**Labels:** `documentação` `portfólio`
**Prioridade:** 🟡 Média
**Descrição:**
Organizar e padronizar todos os notebooks do projeto para apresentação.

**Subtarefas:**
- [ ] Renomear notebooks com prefixo numérico: `01_setup.ipynb`, `02_metodologia_fase2.ipynb`
- [ ] Garantir que todos os notebooks executam do início ao fim com `Restart & Run All`
- [ ] Adicionar célula de introdução em cada notebook explicando o objetivo
- [ ] Adicionar célula de conclusão com principais insights
- [ ] Exportar notebooks como HTML e adicionar em `docs/`
- [ ] Adicionar link para os notebooks no README

**Critério de aceite:** Todos os notebooks exportados em HTML e acessíveis via link no README.

---

## Issue #28 — Documentação das decisões técnicas (ADR)
**Labels:** `documentação`
**Prioridade:** 🟢 Baixa
**Descrição:**
Registrar formalmente as principais decisões arquiteturais do projeto em um documento de ADR (Architecture Decision Record).

**Subtarefas:**
- [ ] Criar `docs/decisoes_tecnicas.md`
- [ ] Documentar: escolha do Streamlit vs Power BI
- [ ] Documentar: escolha do modelo de Poisson vs outros modelos (regressão logística, ELO)
- [ ] Documentar: API-Football vs scraping de notícias + NLP para escalações
- [ ] Documentar: GitHub Actions vs servidor dedicado para automação
- [ ] Documentar: Ranking FIFA como base principal vs resultado da Copa anterior (mudança 32→48 seleções)
- [ ] Adicionar link para `decisoes_tecnicas.md` no README e na página de Metodologia do dashboard

**Critério de aceite:** Documento com pelo menos 5 decisões registradas com contexto, alternativas consideradas e justificativa.

---

## Issue #29 — Post de divulgação no LinkedIn
**Labels:** `portfólio` `divulgação`
**Prioridade:** 🟡 Média
**Descrição:**
Redigir o post de divulgação do projeto no LinkedIn para maximizar visibilidade.

**Subtarefas:**
- [ ] Redigir texto do post com: gancho de abertura, o que o projeto faz, o que foi aprendido, link para o dashboard e para o repositório
- [ ] Preparar 2-3 screenshots do dashboard para usar como mídia do post
- [ ] Definir hashtags relevantes: #DataScience #Python #Streamlit #FIFAWorldCup2026 #PortfolioDeDados
- [ ] Publicar após o deploy do Streamlit Cloud estar funcionando
- [ ] Marcar tecnologias e ferramentas usadas

**Critério de aceite:** Post publicado com link funcional para o dashboard.

---

---

# MILESTONE 6 — Acompanhamento ao Vivo durante a Copa
**Prazo:** 11/Jun → 19/Jul/2026
**Objetivo:** Manter o pipeline funcionando durante toda a Copa, corrigir falhas rapidamente e evoluir o projeto com os dados reais.
**Entregável:** Dashboard atualizado ao longo de toda a competição.

---

## Issue #30 — Monitoramento diário durante a Copa
**Labels:** `fase4` `monitoramento`
**Prioridade:** 🔴 Alta
**Descrição:**
Rotina de acompanhamento para garantir que o pipeline está saudável durante a Copa.

**Subtarefas:**
- [ ] Verificar diariamente se o GitHub Actions executou com sucesso (badge + aba Actions)
- [ ] Confirmar que novos resultados aparecem no dashboard após cada rodada de jogos
- [ ] Verificar manualmente a acurácia acumulada do modelo a cada 5 jogos
- [ ] Registrar qualquer falha no pipeline e tempo de resolução em `docs/incidentes.md`
- [ ] Atualizar o post do LinkedIn com a acurácia do modelo após cada fase (grupos, oitavas, quartas, semis, final)

**Critério de aceite:** Nenhuma interrupção no dashboard por mais de 24 horas durante a Copa.

---

## Issue #31 — Análise pós-Copa
**Labels:** `análise` `portfólio`
**Prioridade:** 🟡 Média
**Descrição:**
Após o término da Copa, produzir uma análise completa do desempenho do modelo.

**Subtarefas:**
- [ ] Calcular acurácia final do modelo (% de jogos com vencedor correto)
- [ ] Calcular erro médio absoluto do placar previsto vs real
- [ ] Identificar as maiores zebras previstas e as que o modelo acertou
- [ ] Criar notebook `03_analise_pos_copa.ipynb` com análise completa
- [ ] Atualizar README com resultados finais do modelo
- [ ] Publicar post de encerramento no LinkedIn com resultados

**Critério de aceite:** Notebook com análise completa e métricas finais publicado no repositório.

---

---

## Resumo dos Milestones

| Milestone | Prazo | Issues | Status |
|---|---|---|---|
| 1 — Fundação e Coleta | 15/Mai/2026 | #1 ao #5 | 🔄 Em andamento |
| 2 — Modelo Preditivo | 22/Mai/2026 | #6 ao #11 | ⏳ Aguardando M1 |
| 3 — Dashboard Streamlit | 31/Mai/2026 | #12 ao #20 | ⏳ Aguardando M2 |
| 4 — Automação ao Vivo | 11/Jun/2026 | #21 ao #25 | ⏳ Aguardando M3 |
| 5 — Documentação e Portfólio | 05/Jun/2026 | #26 ao #29 | ⏳ Paralelo ao M3 |
| 6 — Acompanhamento da Copa | 19/Jul/2026 | #30 ao #31 | ⏳ Durante a Copa |

**Total: 31 issues | 6 milestones | ~75 dias de projeto**

---

## Labels sugeridas para criar no repositório

| Label | Cor | Uso |
|---|---|---|
| `setup` | #6B7280 | Configuração de ambiente |
| `coleta` | #3B82F6 | Scraping e APIs |
| `dados` | #06B6D4 | Manipulação de datasets |
| `processamento` | #8B5CF6 | ETL e transformações |
| `modelo` | #EC4899 | Modelo preditivo e ML |
| `ciência-de-dados` | #F59E0B | Análises e estatística |
| `simulação` | #EF4444 | Monte Carlo |
| `dashboard` | #10B981 | Streamlit |
| `streamlit` | #FF4B4B | Streamlit especificamente |
| `infra` | #374151 | GitHub Actions, deploy |
| `ci-cd` | #1F2937 | Pipelines de automação |
| `deploy` | #059669 | Publicação |
| `validação` | #D97706 | Testes e checagens |
| `pipeline` | #7C3AED | Orquestração |
| `documentação` | #6D28D9 | README, notebooks, ADRs |
| `portfólio` | #BE185D | Itens voltados para visibilidade |
| `divulgação` | #DB2777 | LinkedIn, redes sociais |
| `fase4` | #065F46 | Itens de automação ao vivo |
| `monitoramento` | #1E40AF | Alertas e logs |
| `análise` | #92400E | Análises exploratórias |
| `design` | #701A75 | Visual do dashboard |
| `automação` | #064E3B | Scripts automáticos |
