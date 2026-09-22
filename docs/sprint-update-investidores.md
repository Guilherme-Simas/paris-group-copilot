# Atualização Assíncrona de Sprint — Paris Group Copilot

> ⚠️ **Caso de treino.** A empresa Vitalis, o CTO, os investidores da série B e a
> rodada de investimento citados neste documento são fictícios, criados para o
> exercício do Módulo 2 do curso Paris Group Copilot.

**Autor:** Guilherme Simas
**Público:** revisão técnica assíncrona — sem reunião
**Repositório:** https://github.com/Guilherme-Simas/paris-group-copilot
**Demo em vídeo (3:18):** https://github.com/user-attachments/assets/f0ffa76b-418c-4e00-8281-66e893e2d16c
**Roteiro da demo:** `docs/roteiro-loom.md`

---

## 1. Contexto

O Paris Group Copilot é uma ferramenta para times de venture studio conduzirem a
descoberta e a execução de MVPs. O problema que ele resolve: a cada produto novo,
o time remonta enquadramento e hipóteses do zero, porque o aprendizado dos MVPs
anteriores está espalhado em ferramentas diferentes e não é consultável.

**Estado ao fim desta sprint:**

- Aplicação Next.js com TypeScript, com as rotas `/projeto` e `/hipotese` navegáveis
- Backend em FastAPI com as entidades Projeto e Hipótese, quatro endpoints e
  contrato OpenAPI publicado em `/docs`
- PostgreSQL 16 provisionado via Docker Compose, com dados persistindo entre execuções
- Documentação de produto versionada: enquadramento, arquitetura e handoffs
- Fluxo de contribuição operando: branch, Conventional Commits, Pull Request com
  template de quatro blocos e merge com squash

**Validação executada:** rotas respondendo HTTP 200; containers do banco e da API
saudáveis; criação e leitura de Projeto e Hipótese testadas com dados persistidos
no PostgreSQL.

---

## 2. Decisões técnicas da sprint

### D1 — Backend em FastAPI com contrato OpenAPI, divergindo do padrão Full-TS

**Decisão:** o backend foi implementado em Python com FastAPI, expondo contrato
OpenAPI gerado automaticamente a partir dos modelos.

**Justificativa:** o FastAPI gera o contrato e a validação de request e response a
partir do próprio código, e o `/docs` funciona como documentação executável — dá
para disparar requisições pela tela, o que acelera a validação manual durante o MVP.

**Custo assumido, registrado explicitamente:** o sistema passa a ter duas
linguagens e dois sistemas de tipos. O contrato entre frontend e backend deixa de
ser verificado pelo compilador e passa a depender de sincronização. Consequências:
renomear um campo no backend não quebra o frontend na compilação — quebra em
produção; e agentes de IA que escrevem o frontend precisam inferir o formato do
payload em vez de ler o tipo.

A análise completa está em `docs/arquitetura.md`. A decisão de manter ou migrar
está listada como bloqueio ativo (B2).

### D2 — PostgreSQL em vez de SQLite

**Decisão:** PostgreSQL 16 desde o ambiente local.

**Justificativa:** paridade entre desenvolvimento e produção. O que roda na máquina
do desenvolvedor é idêntico ao que roda em produção. Com SQLite, seria necessário
trocar de banco no momento do deploy — ou seja, introduzir uma classe nova de erro
exatamente quando o produto começa a ter usuário real e a hipótese está sendo medida.

Ganho adicional para o modelo de studio: todos os produtos compartilham o mesmo
dialeto SQL, a mesma modelagem e o mesmo conjunto de scripts de backup e monitoramento.

### D3 — Monorepo: backend em `api/` no mesmo repositório do frontend

**Decisão:** frontend, backend e infraestrutura num único repositório.

**Justificativa:** uma alteração de contrato quase sempre toca backend e frontend ao
mesmo tempo. No monorepo isso é um commit, revisado de uma vez, com o estado
consistente em qualquer ponto do histórico. Em repositórios separados, a mesma
alteração vira duas Pull Requests, duas versões a sincronizar e dois deploys a
coordenar — com uma janela em que produção fica inconsistente.

---

## 3. Bloqueios ativos

### B1 — Repositório sem integração contínua

**Situação:** não há CI configurado. Pull Requests são abertos e mesclados sem
verificação automática de tipos, testes ou lint.

**Impacto:** o repositório cumpre a forma do processo — branch, PR, merge — sem a
garantia que justifica o processo existir. Qualquer erro que passe pela revisão
humana chega à `main`.

**Responsável:** Guilherme Simas
**Prazo esperado:** 2 horas de trabalho, previsto para o início da próxima sprint

### B2 — Decisão pendente sobre a arquitetura do backend

**Situação:** manter o backend em FastAPI ou migrar para tRPC + Drizzle sobre o
mesmo PostgreSQL, alinhando ao padrão Full-TS da organização.

**Impacto:** define se vale continuar investindo no backend atual. Quanto mais código
for escrito sobre o FastAPI, mais cara fica a migração. A decisão também determina
se o projeto terá verificação de tipos ponta a ponta — o mecanismo que permite que
agentes de IA escrevam código com segurança.

**Responsável:** Guilherme Simas
**Prazo esperado:** 1 dia útil, após a configuração do CI (B1), que é pré-requisito
para medir o impacto da migração com segurança

---

## 4. Próximos passos

| # | Ação | Responsável | Prazo estimado |
|---|---|---|---|
| 1 | Configurar CI com verificação de tipos e lint a cada Pull Request | Guilherme Simas | 2 horas |
| 2 | Decidir B2: manter FastAPI ou migrar para tRPC + Drizzle | Guilherme Simas | 1 dia útil |
| 3 | Adicionar testes automatizados dos quatro endpoints da API | Guilherme Simas | 4 horas |
| 4 | Instrumentar os eventos que medem a hipótese de valor do produto | Guilherme Simas | 1 dia útil |
