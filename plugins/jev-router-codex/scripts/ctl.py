#!/usr/bin/env python3
"""Uso: ctl.py on|off|status"""
import json, os, sys
from collections import Counter
from pathlib import Path

H = Path(os.environ.get("JEV_ROUTER_HOME") or Path.home() / ".codex" / "jev-router")
STATE = H / "state.json"


def enabled():
    try:
        return json.loads(STATE.read_text()).get("enabled", True)
    except Exception:
        return True


def main(cmd):
    if cmd in ("on", "off"):
        H.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"enabled": cmd == "on"}))
        print(f"Roteador Jev {'ligado' if cmd == 'on' else 'desligado'}.")
    elif cmd == "status":
        rows = []
        try:
            for line in open(H / "log.jsonl"):
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
        except OSError:
            pass
        tiers = Counter(r["tier"] for r in rows if r.get("tier"))
        acts = Counter(r["action"] for r in rows)
        costs = [r["cost"] for r in rows if r.get("cost") is not None]
        secs = [r["secs"] for r in rows if r.get("secs") is not None]
        print(f"Roteador Jev: {'ligado' if enabled() else 'desligado'}")
        print(f"Mensagens registradas: {len(rows)}")
        print("Por tamanho:", dict(tiers) or "-")
        print("Por ação:", dict(acts) or "-")
        print(f"Custo total: US$ {sum(costs):.6f}")
        print(f"Tempo médio: {sum(secs) / len(secs):.2f} s" if secs else "Tempo médio: -")
    else:
        sys.exit("Uso: ctl.py on|off|status")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
