#!/usr/bin/env python3
"""Hook UserPromptSubmit: o Jev classifica o tamanho do pedido; o Claude decide o resto.

Sempre sai com código 0 e nunca bloqueia. Não grava o texto da mensagem nem a chave.
Pasta de estado e log: ~/.claude/jev-router (ou JEV_ROUTER_HOME).
"""
import json, os, sys, time, urllib.request
from pathlib import Path

URL = "https://ai-gateway.vercel.sh/typesafe/v1/systemone"
MODEL = "typesafe-ai/jev"
MIN_CONF, CTX_MAX, MIN_LEN, MAX_CHARS, TIMEOUT = 0.6, 0.6, 20, 4000, 4
AGENT = {"tiny": ("jev-haiku", "Haiku"), "everyday": ("jev-sonnet", "Sonnet"), "large": ("jev-opus", "Opus")}

QUESTIONS = {
    "tier": {
        "type": "choice",
        "instructions": "How big is the task the user is asking for? Pick the smallest tier that fits, unless a mistake would be costly.",
        "criteria": {
            "tiny": "a lookup, a rename, a trivial edit, a one-line answer",
            "everyday": "an email, a short text, a small code change, a simple explanation",
            "large": "several steps, research, a change across many files, a full report",
            "hardest": "strategy, architecture, security, legal, money, or any decision where a mistake is expensive",
        },
    },
    "needs_context": {
        "type": "noul",
        "instructions": "The message is a short reply that only makes sense inside the previous conversation.",
    },
}


def home():
    return Path(os.environ.get("JEV_ROUTER_HOME") or Path.home() / ".claude" / "jev-router")


def log(**row):
    try:
        h = home()
        h.mkdir(parents=True, exist_ok=True)
        with open(h / "log.jsonl", "a") as f:
            f.write(json.dumps({"ts": int(time.time()), **row}) + "\n")
    except Exception:
        pass


def enabled():
    try:
        return json.loads((home() / "state.json").read_text()).get("enabled", True)
    except Exception:
        return True


def ask(text):
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        raise RuntimeError("no key")
    req = urllib.request.Request(
        URL,
        data=json.dumps({"model": MODEL, "state": text, "questions": QUESTIONS}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt") or ""
    except Exception:
        return
    if not enabled():
        return
    low = prompt.lower()
    s = prompt.lstrip()
    if s.startswith(("/", "!")) or len(prompt.strip()) < MIN_LEN:
        return log(action="skip:short")
    if "#privado" in low or "[privado]" in low:
        return log(action="skip:private")

    t0 = time.perf_counter()
    try:
        full = ask(prompt[:MAX_CHARS])
        res = full["answers"]
        secs = round(time.perf_counter() - t0, 2)
        cost = (full.get("provider_metadata", {}).get("gateway", {}) or {}).get("cost")
        cost = float(cost) if cost is not None else None
        tier = res["tier"]["choice"]
        conf = round(float(res["tier"]["confidence"]), 2)
        ctx = round(float(res["needs_context"]["noul"]), 2)
    except Exception:
        return log(action="error", secs=round(time.perf_counter() - t0, 2))

    base = dict(tier=tier, conf=conf, ctx=ctx, secs=secs, cost=cost)
    if ctx >= CTX_MAX:
        return log(action="skip:context", **base)
    if conf < MIN_CONF:
        return log(action="skip:lowconf", **base)
    if tier == "hardest" or tier not in AGENT:
        return log(action="self", **base)

    agent, model = AGENT[tier]
    log(action="delegate", **base)
    print(json.dumps({
        "systemMessage": f"Jev: {tier} ({conf}) → {model}",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"Roteador Jev: tarefa dimensionada como {tier} (confiança {conf}). "
                f"Se o trabalho for autossuficiente, delegue ao agente {agent} com briefing completo "
                "e repasse o resultado. Se depender do contexto desta conversa, ou se as instruções "
                "do projeto fixarem modelo e esforço, faça você mesmo."
            ),
        },
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
