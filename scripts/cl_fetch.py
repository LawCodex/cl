#!/usr/bin/env python3
"""Fetch the Constitution and the codes of Chile from LeyChile (BCN).

Deliberately limited to a small, fixed list of norms (one request each):
the LeyChile API terms of use ("Condiciones de uso API Ley Chile", section 3)
prohibit mass/systematic/automated extraction aimed at replicating Ley Chile
or building large-scale structured repositories without the express
authorisation of the Biblioteca del Congreso Nacional. See README.md.

Raw XML is cached in _raw/cl/xml/ (outside the repository).
"""
import json
import os
import sys
import time

import requests

UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
BASE = "https://www.leychile.cl/Consulta/obtxml"
CODIGOS = "https://nuevo.leychile.cl/servicios/Consulta/getCodigos"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("CL_RAW", os.path.abspath(os.path.join(HERE, "..", "..", "_raw", "cl")))
DELAY = 5.0  # seconds between requests

CONSTITUTION = {"idNorma": "242302", "titulo": "Constitución Política de la República de Chile",
                "kind": "constitucion"}


def get(session, url, params=None):
    for attempt in range(5):
        try:
            r = session.get(url, params=params, timeout=120)
            if r.status_code == 200:
                return r
            print(f"  HTTP {r.status_code} for {url} {params}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"  error {e}", file=sys.stderr)
        time.sleep(DELAY * (2 ** attempt))
    raise SystemExit(f"giving up on {url} {params}")


def main():
    os.makedirs(os.path.join(RAW, "xml"), exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA
    cod_path = os.path.join(RAW, "codigos.json")
    if not os.path.exists(cod_path):
        r = get(s, CODIGOS)
        open(cod_path, "wb").write(r.content)
        time.sleep(DELAY)
    codigos = json.load(open(cod_path, encoding="utf-8"))
    targets = [CONSTITUTION] + [
        {"idNorma": c["idNorma"], "titulo": c["titulo"].strip(), "kind": "codigo"} for c in codigos
    ]
    json.dump(targets, open(os.path.join(RAW, "targets.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for t in targets:
        out = os.path.join(RAW, "xml", f"{t['idNorma']}.xml")
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            continue
        print(f"fetch {t['idNorma']} {t['titulo']}")
        r = get(s, BASE, {"opt": "7", "idNorma": t["idNorma"], "conNotas": "False"})
        if not r.content.lstrip().startswith(b"<?xml"):
            raise SystemExit(f"unexpected response for {t['idNorma']}: {r.content[:200]!r}")
        open(out, "wb").write(r.content)
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
