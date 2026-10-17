# jev-router

Roteador de tamanho de tarefa: a cada mensagem, o Jev (`typesafe-ai/jev`, pelo AI Gateway da Vercel) diz se o pedido é `tiny`, `everyday`, `large` ou `hardest`. O Claude recebe uma nota e decide se delega a um agente (`jev-haiku`, `jev-sonnet`, `jev-opus`).

## O limite

O Claude Code não troca de modelo por mensagem, e um hook não muda o modelo da sessão. O roteador é só uma **nota** somada a **agentes fixados por modelo**. O Jev apenas classifica; nada que ele responde dispara ação. `hardest` não é delegado: o modelo atual faz.

## Uso

- `/jev-router:on`, `/jev-router:off`, `/jev-router:status`
- Usa `AI_GATEWAY_API_KEY` do ambiente ou, se faltar, de `~/.jev_env`; sem nenhuma, tenta sem cabeçalho (proxy da nuvem). Sem chave, lentidão (4 s) ou erro, a mensagem segue normal.
- Ignoradas: mensagens começando com `/` ou `!`, com menos de 20 caracteres, ou com `#privado` / `[privado]`.
- Log em `~/.claude/jev-router/log.jsonl` (sem o texto das mensagens). Outra pasta: `JEV_ROUTER_HOME`.
