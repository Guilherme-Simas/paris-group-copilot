# Arquitetura — Paris Group Copilot

> Cada decisão abaixo é justificada pelos dois critérios centrais do modelo de
> Venture Studio: **velocidade de criação de MVPs** e **reutilização entre
> produtos do studio** — mais um terceiro que sustenta os dois no tempo:
> **manutenção simples**.
>
> Regra que governa o documento: *a complexidade só se paga com retorno medido.*

---

## Visão geral da stack

| Camada | Escolha | Porta |
|---|---|---|
| Frontend | Next.js 16 (App Router) + TypeScript + Tailwind | 3000 |
| Backend | FastAPI (Python 3.12) | 8000 |
| Banco | PostgreSQL 16 | 5432 |
| Orquestração local | Docker Compose | — |
| Contrato | OpenAPI gerado pelo FastAPI, em `/docs` | — |

Organização: **monorepo** — `src/` (frontend) e `api/` (backend) no mesmo
repositório, com `docker-compose.yml` na raiz.

---

## 1. Next.js e não Remix

**Velocidade de MVP.** O App Router transforma pasta em rota sem nenhum arquivo
de configuração: criar `src/app/hipotese/page.tsx` publica `/hipotese`. Num
studio que valida ideias em dias, o custo de adicionar uma tela precisa ser
próximo de zero — e aqui é literalmente criar um arquivo.

**Reutilização.** O `layout.tsx` funciona como molde herdado por todas as
páginas. É o ponto de entrada natural para um design system compartilhado entre
os produtos da frota (o PageShell): um layout, N produtos herdando. Remix é
tecnicamente competente, mas a frota já está padronizada em Next.js — e no
modelo de studio a escolha certa é a que **todos os produtos já usam**, porque é
ela que permite mover desenvolvedor e agente de IA entre projetos sem recomeçar
o aprendizado.

**Manutenção.** Sendo o padrão da casa, upgrade de versão e correção de bug são
feitos uma vez e aproveitados por todos os produtos.

---

## 2. PostgreSQL e não SQLite

**Decisão pelo critério de paridade entre desenvolvimento e produção.**

O que roda na máquina do desenvolvedor é exatamente o que roda em produção no
Railway: mesmo banco, mesma versão, mesmo comportamento. Com SQLite, o MVP
funcionaria localmente e exigiria **troca de banco no momento do deploy** — ou
seja, uma migração de infraestrutura justamente quando o produto começa a ter
usuário real e a hipótese está sendo medida. É o pior momento possível para
introduzir uma classe nova de bug.

**Velocidade de MVP.** Paridade elimina a categoria inteira de erro "funciona
aqui, quebra lá", que é cara porque só aparece depois do deploy.

**Reutilização.** Todos os produtos do studio falam o mesmo dialeto SQL e podem
compartilhar modelagem, migrações e recursos que o SQLite não oferece (JSONB,
busca textual, extensões). Aprendizado de modelagem no produto N serve ao N+1.

**Manutenção.** Um único banco para toda a frota significa um único conjunto de
scripts de backup, monitoramento e recuperação.

---

## 3. FastAPI em `api/` — e a divergência consciente com o padrão da casa

O desafio prescreve FastAPI com contrato OpenAPI. **Isso diverge do padrão
canônico da Paris Group**, que é Full-TS ponta a ponta (Next.js + tRPC +
Drizzle), e a divergência está registrada aqui de propósito.

**O que o FastAPI entrega bem:**

- Contrato OpenAPI gerado automaticamente a partir dos modelos Pydantic, sem
  escrever especificação à mão. O `/docs` vira documentação executável — dá para
  disparar requisição pela própria tela, o que acelera validação manual no MVP.
- Validação de request e response declarada junto do modelo: o schema é a
  fonte de verdade do endpoint.
- Ecossistema Python para IA/ML disponível no mesmo processo.

**O que essa escolha custa — e é o ponto central:**

O sistema passa a ter **duas linguagens e dois sistemas de tipos**. O contrato
entre frontend e backend deixa de ser verificado pelo compilador e passa a
depender de geração de cliente ou sincronização manual. As consequências, na
ordem em que aparecem:

1. **Divergência silenciosa** — renomear um campo no backend não quebra o
   frontend na compilação. Quebra em produção, na frente do usuário.
2. **Alucinação de contrato** — o agente de IA que escreve o frontend precisa
   *adivinhar* o formato do payload em vez de ler o tipo. Erro plausível e
   confiante é o modo de falha mais caro que existe.
3. **Retrabalho** — o mesmo modelo de dados existe duas vezes (Pydantic e
   TypeScript) e as duas cópias precisam ser mantidas em sincronia para sempre.

No padrão Full-TS, o tipo nasce no schema do banco (Drizzle), atravessa o tRPC e
chega ao componente de tela sem redigitação. Um `pnpm typecheck` valida o sistema
inteiro em segundos — o gate automático mais rápido e confiável para um time que
trabalha lado a lado com agentes de IA.

**Conclusão:** a arquitetura entregue aqui funciona e cumpre o desafio, mas
sacrifica o portão de tipos ponta a ponta. Num studio que aposta velocidade em
execução assistida por IA, esse portão é justamente o que torna a velocidade
segura. Por isso a recomendação para a próxima onda deste produto é migrar o
backend para tRPC + Drizzle sobre o mesmo PostgreSQL, mantendo Next.js e Docker
Compose inalterados.

### Por que FastAPI e não Express (dado que o desafio pede backend separado)

Se o requisito é um backend em linguagem distinta, FastAPI supera Express em dois
pontos que interessam ao studio: o contrato OpenAPI é **gerado do código** em vez
de mantido à parte, e a validação de entrada e saída vem embutida. Express exigiria
montar essa camada manualmente em cada produto — custo que se repete a cada MVP e
que o studio não deveria pagar mais de uma vez.

---

## 4. Monorepo: `api/` dentro do mesmo repositório

**Decisão pelo critério de "uma mudança, um PR".**

Uma alteração de contrato quase sempre toca backend e frontend ao mesmo tempo.
No monorepo isso é um commit, revisado de uma vez, com o estado consistente em
qualquer ponto do histórico. Em repositórios separados, a mesma alteração vira
duas PRs, duas versões a sincronizar e dois deploys a coordenar — e existe uma
janela em que produção está inconsistente.

**Velocidade de MVP.** Menos coordenação por mudança; o time gasta tempo no
produto, não em versionamento cruzado.

**Reutilização.** O chassi do studio é clonado inteiro — frontend, backend e
infraestrutura juntos. Produto novo nasce com o esqueleto completo em vez de ser
montado peça por peça a cada MVP.

**Manutenção.** Um repositório, um CI, um histórico. E o agente de IA lê o
sistema inteiro no mesmo contexto, o que reduz erro de contrato.

---

## 5. Docker Compose para a infraestrutura local

**Velocidade de MVP.** `docker compose up` entrega banco e API prontos. Onboarding
de um desenvolvedor novo deixa de ser um roteiro de instalação e passa a ser um
comando — e o mesmo vale para um agente de IA que precise subir o ambiente.

**Reutilização.** O `docker-compose.yml` é praticamente idêntico entre os produtos
do studio: muda o nome do serviço e as variáveis. É artefato de chassi, não de
produto.

**Manutenção.** As versões de banco e runtime ficam declaradas em arquivo
versionado. Não existe "na minha máquina é a 14" — está escrito no repositório,
e o `healthcheck` garante que a API só sobe depois que o banco aceita conexão.

---

## Resumo das decisões

| Decisão | Critério que a sustenta |
|---|---|
| Next.js (App Router) | Rota = pasta: custo quase zero por tela nova; layout compartilhado como base de design system da frota |
| PostgreSQL | Paridade dev/produção — sem troca de banco no deploy, quando o produto já tem usuário |
| FastAPI + OpenAPI | Contrato gerado do código; **divergência consciente** do padrão Full-TS, com custo documentado |
| Monorepo | Uma mudança, um PR; chassi clonado inteiro; contexto completo para agentes de IA |
| Docker Compose | Ambiente em um comando; arquivo de infra reutilizável entre produtos |
