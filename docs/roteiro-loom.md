# Roteiro do vídeo — o que falar e onde clicar

Duração alvo: 3 minutos. Leia em voz natural, sem pressa.

---

## PASSO 1 — Abertura (sem mostrar tela) · 0:00 a 0:45

**FALE:**

"Essa é a atualização da sprint do Paris Group Copilot.

O problema que o produto resolve é o seguinte: num venture studio, toda vez que
um produto novo começa, o time refaz o enquadramento e as hipóteses do zero,
porque o aprendizado dos produtos anteriores está espalhado em várias ferramentas
e ninguém consegue consultar.

Quem sente essa dor é o product manager, no começo de cada MVP.

A promessa do produto é reduzir esse trabalho inicial de cerca de oito horas para
duas horas ou menos."

---

## PASSO 2 — Página de Projeto · 0:45

**CLIQUE:** http://localhost:3000/projeto

**FALE:**

"Essa é a página de Projeto, construída em Next.js com TypeScript."

---

## PASSO 3 — Página de Hipótese · 1:00

**CLIQUE:** http://localhost:3000/hipotese

**FALE:**

"E essa é a página de Hipótese de Valor. As duas rotas estão navegáveis."

---

## PASSO 4 — Contrato da API · 1:15

**CLIQUE:** http://localhost:8000/docs

**FALE:**

"Esse é o contrato da API, gerado automaticamente pelo backend. Ele lista os
endpoints de Projeto e de Hipótese, com o formato de entrada e de saída de cada um."

---

## PASSO 5 — Criar um projeto ao vivo · 1:30

**CLIQUE, nesta ordem, dentro da página que já está aberta:**

1. Na linha verde escrita `POST /projetos`
2. No botão `Try it out`, no canto direito
3. No botão azul `Execute`

**FALE enquanto clica:**

"Vou criar um projeto agora, ao vivo, direto pelo contrato."

---

## PASSO 6 — Mostrar o resultado · 1:50

**FALE, apontando para a resposta que apareceu na tela:**

"O dado foi gravado e voltou com identificador e data de criação. O backend roda
num container junto de um banco PostgreSQL, e a stack inteira sobe com um comando só."

---

## PASSO 7 — Decisões técnicas · 2:15

**FALE (pode voltar a mostrar só o seu rosto ou o documento):**

"Foram três decisões técnicas nesta sprint.

A primeira: o backend foi feito em FastAPI com contrato OpenAPI. Isso diverge do
padrão da casa, que é TypeScript de ponta a ponta, e o custo dessa escolha está
documentado — perdemos a verificação automática de tipos entre o frontend e o backend.

A segunda: usamos PostgreSQL desde o ambiente local, em vez de SQLite, para que o
ambiente de desenvolvimento seja idêntico ao de produção.

A terceira: frontend e backend ficam no mesmo repositório, para que uma mudança de
contrato seja um commit só, revisado de uma vez."

---

## PASSO 8 — Bloqueios e fechamento · 2:40 a 3:00

**FALE:**

"Existem dois bloqueios ativos.

O primeiro é que o repositório ainda não tem integração contínua, então os Pull
Requests entram sem verificação automática. São duas horas de trabalho para resolver.

O segundo é a decisão de manter o backend em FastAPI ou migrar para o padrão da
casa. Essa depende da primeira.

Os dois bloqueios estão comigo.

O próximo passo imediato é configurar a integração contínua. Obrigado."

---

## Checklist antes de apertar o botão de gravar

- [ ] Serviços no ar (banco, API e frontend)
- [ ] Abas já abertas: `localhost:3000/projeto`, `localhost:3000/hipotese`, `localhost:8000/docs`
- [ ] Microfone funcionando
- [ ] Notificações do sistema silenciadas
