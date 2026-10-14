---
name: jev
description: >
  Usar o Jev, modelo System One da TypeSafe, para decisões rápidas e baratas
  (escolher uma opção, dar uma nota numa escala, estimar a chance de algo ser
  verdade) sobre texto livre, sempre pelo AI Gateway da Vercel. Usar quando uma
  funcionalidade precisa classificar, extrair, ordenar ou triar texto, ou quando
  o usuário pedir "use o Jev". Não usar para escrever texto, conversar, raciocinar,
  contar, fazer contas ou datas.
---

# Jev pelo AI Gateway da Vercel

Jev não escreve texto. Recebe um estado (texto ou dados) mais perguntas tipadas
e devolve decisões: `choice` (uma opção), `score` (nota numa escala) ou `noul`
(chance de algo ser verdade), quase sempre com a confiança.

Regra geral: o Jev decide, o Claude escreve. Quando o Jev não tem certeza, a
decisão volta para uma pessoa ou para o Claude.

## Configuração (sempre esta, nunca a API direta)

- Chave: variável de ambiente `AI_GATEWAY_API_KEY`. Nunca imprimir, nunca gravar
  em arquivo versionado, nunca colocar em código de navegador. Só em servidor
  (por exemplo, Vercel Functions).
- Base URL: `https://ai-gateway.vercel.sh/typesafe`
- Modelo: `typesafe-ai/jev`
- SDK: `@typesafe-ai/sdk`, `new TypeSafeClient({ apiKey, baseURL })`, método `systemOne(request)`.
- Se `AI_GATEWAY_API_KEY` não existir, parar e avisar o usuário. Nunca pedir que
  cole a chave no chat e nunca enviar outra credencial no lugar dela.

## Antes de escrever código

A API e os modelos mudam. Ler a documentação atual:
- Índice: https://docs.typesafe.ai/llms.txt
- API e primitivas: https://docs.typesafe.ai/api.md e https://docs.typesafe.ai/primitives.md
- Gateway da Vercel: buscar "TypeSafe" na documentação do AI Gateway
- Para o desenho das perguntas, usar também a skill `typesafe:typesafe-ai`, se
  estiver instalada.

Confirmar o caminho exato do endpoint no gateway com uma chamada de teste antes
de qualquer experimento maior.

## Como usar

1. Escolher a primitiva pelo significado da resposta: Choice (uma entre várias),
   Score (grau numa dimensão), Noul (sim ou não com probabilidade).
2. Uma pergunta estreita por julgamento. Perguntas independentes sobre o mesmo
   estado vão juntas na mesma chamada.
3. Incluir uma opção "nenhuma das anteriores" quando fizer sentido.
4. Usar a confiança: abaixo de um limite (comece em 0,6 e ajuste com dados reais),
   marcar para revisão humana.
5. Medir tempo, custo e acerto numa amostra real antes de adotar.

## Quando não usar

Escrita, conversa, raciocínio longo, contagem, contas e datas. Essas partes ficam
em código ou com o Claude. Tudo que vai para o Jev sai do computador do usuário,
então perguntar antes de enviar dados privados.
