# claude-skills

Marketplace pessoal de plugins do Claude Code.

    claude plugin marketplace add nielebock/claude-skills
    claude plugin install jev@nielebock-skills

## Codex

O catálogo nativo `.agents/plugins/marketplace.json` fornece a skill Jev e o roteador Codex (Luna/Sol/Astra). O catálogo Claude permanece separado.

```sh
codex plugin marketplace add https://github.com/nielebock/claude-skills.git
codex plugin add jev@nielebock-skills
codex plugin add jev-router-codex@nielebock-skills
```

Após instalar, revise o hook no gerenciador nativo `/hooks`. Atualizações do catálogo Git distribuem as versões publicadas; mudanças no hook podem exigir nova confiança. Não há troca automática do modelo principal. O roteador envia até 4.000 caracteres de pedidos elegíveis à Vercel/TypeSafe; `#privado` ou `[privado]` no pedido impede esse envio.

Para quem migra de `jev-codex-local`: instale a versão Git, desative a versão local e revise o novo hook, evitando dois roteadores ativos. O estado em ~/.codex/jev-router é reutilizado.

Testes offline: `python3 plugins/jev-router-codex/scripts/test_route.py`.
