# Roteiro — Demo em vídeo (Loom, 3 minutos)

> ⚠️ Caso de treino: a apresentação é dirigida a investidores fictícios da empresa
> fictícia Vitalis, para o exercício do Módulo 2.

Três blocos, com tempo definido. O limite de 3 minutos é regra: demonstrações
longas perdem atenção.

## Bloco 1 — Contexto de negócio (0:00 – 0:45)

O que dizer, sem abrir código:

- Qual problema o produto resolve: em um venture studio, cada produto novo começa
  com o time remontando enquadramento e hipóteses do zero, porque o aprendizado dos
  produtos anteriores está espalhado e não é consultável
- Quem sente essa dor: o product manager, no início de cada MVP
- O que o produto promete: reduzir o tempo de enquadramento inicial de cerca de
  8 horas para 2 horas ou menos

## Bloco 2 — Demonstração na tela (0:45 – 2:15)

O que mostrar, nesta ordem:

1. `http://localhost:3000/projeto` — a página de Projeto
2. `http://localhost:3000/hipotese` — a página de Hipótese de Valor
3. `http://localhost:8000/docs` — o contrato da API, disparando um `POST /projetos`
   ao vivo e mostrando a resposta
4. `GET /hipoteses?projeto_id=1` — mostrando que o dado foi realmente gravado no banco

Comentar durante a demonstração: o backend roda em container junto de um PostgreSQL,
e sobe inteiro com um comando só.

## Bloco 3 — Decisões, bloqueios e próximos passos (2:15 – 3:00)

- Três decisões da sprint: FastAPI com OpenAPI (e o custo assumido), PostgreSQL por
  paridade com produção, monorepo para manter contrato e interface no mesmo commit
- Dois bloqueios: ausência de CI, e a decisão pendente sobre manter ou migrar o backend
- Próximo passo imediato: configurar o CI

## Antes de gravar

- Deixar as duas abas já abertas, para não gastar tempo digitando endereço
- Subir a stack antes: `docker compose up -d` e `npm run dev`
- O link do vídeo entra em `docs/sprint-update-investidores.md` e na descrição da
  Pull Request
