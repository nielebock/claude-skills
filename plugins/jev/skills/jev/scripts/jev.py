#!/usr/bin/env python3
"""Chama o Jev (typesafe-ai/jev) pela API compatível com TypeSafe do AI Gateway da Vercel.

Uso: jev.py request.json      (ou o JSON pela entrada padrão)
Request: {"state": <texto ou objeto>, "questions": {nome: {type, instructions, criteria}}}
Autenticação: se AI_GATEWAY_API_KEY existir como variável de ambiente, vai como Bearer.
Na nuvem, o proxy do ambiente pode injetar a chave sozinho (segredo de rede para
ai-gateway.vercel.sh). A chave nunca é impressa.
Imprime a resposta completa mais "seconds" (tempo total) e "cost_usd", ou o erro HTTP exato.
"""
import json, os, sys, time, urllib.request, urllib.error

URL = "https://ai-gateway.vercel.sh/typesafe/v1/systemone"
MODEL = "typesafe-ai/jev"


def main():
    key = os.environ.get("AI_GATEWAY_API_KEY")
    req = json.load(open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin)
    req.setdefault("model", MODEL)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    http = urllib.request.Request(URL, data=json.dumps(req).encode(), headers=headers)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(http, timeout=60) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": True, "http_status": e.code, "body": e.read().decode()}, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": True, "exception": repr(e)}, indent=2))
        sys.exit(1)
    body["seconds"] = round(time.perf_counter() - t0, 3)
    cost = body.get("provider_metadata", {}).get("gateway", {}).get("cost")
    body["cost_usd"] = float(cost) if cost is not None else None
    print(json.dumps(body, indent=2))


if __name__ == "__main__":
    main()
