# Jev para Codex
Versão Codex do jev-router, distribuída pelo catálogo Git nielebock-skills. Mapa: tiny=gpt-6-luna, everyday=gpt-6-sol, large=gpt-6-astra; hardest permanece no modelo atual. Nunca muda o modelo principal. A delegação é recomendação, condicionada a ferramenta, modelo disponível e contexto suficiente.

Hook UserPromptSubmit requer revisão/confiança nativa do Codex. Credencial existente: AI_GATEWAY_API_KEY ou ~/.jev_env; nunca copiada. Envia até 4.000 caracteres do pedido elegível ao AI Gateway/TypeSafe. Ignora /, !, menos de 20 caracteres e #privado/[privado]. Timeout de 4 segundos, falhas não bloqueiam. Logs locais sem texto nem chave em ~/.codex/jev-router. Sem fallback de modelo oculto: na indisponibilidade, o agente principal assume.

Status: python3 scripts/ctl.py status; desativar: python3 scripts/ctl.py off. Instalação: `codex plugin marketplace add https://github.com/nielebock/claude-skills.git` e `codex plugin add jev-router-codex@nielebock-skills`. O catálogo Git distribui novas versões na atualização dos marketplaces. Hooks alterados exigem nova revisão de confiança. O estado existente em ~/.codex/jev-router é preservado.
