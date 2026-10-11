#!/usr/bin/env python3
"""Convert LeyChile XML (EsquemaIntercambioNorma v1.0) to LawCodex Markdown.

Usage: cl_convert.py [RAW_DIR] [REPO_DIR]
Reads RAW_DIR/targets.json and RAW_DIR/xml/<idNorma>.xml (produced by cl_fetch.py).
"""
import datetime
import json
import os
import re
import sys
import unicodedata

from lxml import etree

NS = "{http://www.leychile.cl/esquemas}"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", "_raw", "cl"))
REPO = sys.argv[2] if len(sys.argv) > 2 else os.path.abspath(os.path.join(HERE, ".."))
PARSER = etree.XMLParser(huge_tree=True, resolve_entities=False, no_network=True)
TODAY = datetime.date.today().isoformat()

ARTICLE_TYPES = {"Artículo", "Disposición Transitoria", "Artículo Transitorio"}


def slugify(s, maxlen=90):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def clean(s):
    return (s or "").replace("\xa0", " ").strip()


def norm_cmp(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


MD_ESCAPE = re.compile(r"^([#>+\-*]|\d+[.)])(\s)")


def paragraphs(text):
    """Split a LeyChile Texto block into paragraphs.

    In the conNotas=False rendering each paragraph is one line, normally indented.
    A non-indented line following a non-empty line is treated as a continuation
    of a hard-wrapped paragraph.
    """
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    paras, cur = [], []
    for line in text.split("\n"):
        if not line.strip():
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        indented = line[:1] in (" ", "\t")
        if cur and indented:
            paras.append(" ".join(cur))
            cur = []
        cur.append(line.strip())
    if cur:
        paras.append(" ".join(cur))
    out = []
    for p in paras:
        p = re.sub(r"[ \t]{2,}", " ", p)
        p = p.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")
        p = p.replace("<", "&lt;")
        p = MD_ESCAPE.sub(lambda m: "\\" + m.group(1) + m.group(2), p)
        out.append(p)
    return out


def strip_title(paras, title):
    """Drop leading paragraphs that only repeat the heading title."""
    if not title:
        return paras
    t = norm_cmp(title)
    acc = ""
    for i, p in enumerate(paras):
        acc += norm_cmp(p)
        if acc == t:
            return paras[i + 1:]
        if not t.startswith(acc):
            break
    return paras


def heading(level, text, out):
    text = re.sub(r"\s+", " ", text).strip()
    if level <= 6:
        out.append("#" * level + " " + text)
    else:
        out.append(f"**{text}**")
    out.append("")


def emit_paras(paras, out):
    for p in paras:
        out.append(p)
        out.append("")


def walk(ef, level, out):
    tipo = ef.get("tipoParte") or ""
    transitorio = ef.get("transitorio") == "transitorio"
    md = ef.find(NS + "Metadatos")
    nombre = clean(md.findtext(NS + "NombreParte")) if md is not None else ""
    titulo = clean(md.findtext(NS + "TituloParte")) if md is not None else ""
    texto = ef.findtext(NS + "Texto")
    children = ef.findall(NS + "EstructurasFuncionales/" + NS + "EstructuraFuncional")
    paras = paragraphs(texto)

    if tipo in ARTICLE_TYPES:
        if tipo == "Disposición Transitoria":
            label = f"Disposición transitoria {nombre}".strip()
        else:
            label = f"Artículo {nombre}".strip() if nombre else (titulo or "Artículo")
            if transitorio and "transitori" not in label.lower():
                label += " transitorio"
        heading(level, label, out)
        emit_paras(paras, out)
    else:
        if titulo:
            label = titulo
        elif nombre:
            label = f"{tipo} {nombre}".strip()
        else:
            label = ""
        if label and (children or titulo):
            heading(level, label, out)
            emit_paras(strip_title(paras, label), out)
        else:
            emit_paras(paras, out)
    for c in children:
        walk(c, level + 1 if (children and (titulo or nombre)) else level, out)


def yq(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(target, path):
    root = etree.parse(path, PARSER).getroot()
    idn = root.get("normaId")
    ident = root.find(NS + "Identificador")
    tns = [(clean(tn.findtext(NS + "Tipo")), clean(tn.findtext(NS + "Numero")))
           for tn in ident.findall(NS + "TiposNumeros/" + NS + "TipoNumero")]
    organismos = [clean(o.text) for o in ident.findall(NS + "Organismos/" + NS + "Organismo")]
    meta = root.find(NS + "Metadatos")
    titulo_norma = clean(meta.findtext(NS + "TituloNorma"))
    title = target["titulo"]
    norma = ", ".join(f"{t} {n}".strip() for t, n in tns)
    fm = [
        "---",
        f"title: {yq(title)}",
        f"identifier: {yq(idn)}",
        f"norma: {yq(norma)}",
        f"official_title: {yq(titulo_norma)}",
        "type: " + ("constitution" if target["kind"] == "constitucion" else "code"),
        "jurisdiction: cl",
        "language: es",
    ]
    if organismos:
        fm.append(f"issuer: {yq('; '.join(organismos))}")
    if ident.get("fechaPromulgacion"):
        fm.append(f"date: {ident.get('fechaPromulgacion')}")
    if ident.get("fechaPublicacion"):
        fm.append(f"published: {ident.get('fechaPublicacion')}")
    fv = root.get("fechaVersion") or ""
    if fv.startswith("2222"):
        # LeyChile uses 2222-02-02 for amendments whose entry into force is
        # undetermined; the XML text already includes them.
        real = [e.get("fechaVersion") for e in root.iter(NS + "EstructuraFuncional")
                if e.get("fechaVersion") and not e.get("fechaVersion").startswith("2222")]
        if real:
            fm.append(f"last_amended: {max(real)}")
        fm.append("pending_amendments: true  # text includes amendments with undetermined entry-into-force date (LeyChile version 2222-02-02)")
    elif fv:
        fm.append(f"last_amended: {fv}")
    fm.append("status: " + ("repealed" if root.get("derogado") == "derogado" else "in_force"))
    fm.append(f"source: {yq('https://www.bcn.cl/leychile/navegar?idNorma=' + idn)}")
    fm.append(f"source_xml: {yq('https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=' + idn + '&conNotas=False')}")
    fm.append(f"retrieved: {TODAY}")
    fm.append("---")
    out = fm + ["", f"# {title}", ""]
    enc = root.find(NS + "Encabezado")
    if enc is not None:
        emit_paras(paragraphs(enc.findtext(NS + "Texto")), out)
    for ef in root.findall(NS + "EstructurasFuncionales/" + NS + "EstructuraFuncional"):
        walk(ef, 2, out)
    prom = root.find(NS + "Promulgacion")
    if prom is not None:
        p = paragraphs(prom.findtext(NS + "Texto"))
        if p:
            emit_paras(p, out)
    anexos = root.findall(NS + "Anexos/" + NS + "Anexo")
    for i, ax in enumerate(anexos, 1):
        t = clean(ax.findtext(NS + "Metadatos/" + NS + "Titulo"))
        heading(2, t or f"Anexo {i}" if len(anexos) > 1 else (t or "Anexo"), out)
        emit_paras(paragraphs(ax.findtext(NS + "Texto")), out)
    names = [clean(n.text) for n in root.iter("{http://valida.aem.gob.cl}Nombre")]
    if names:
        out.append("---")
        out.append("")
        out.append("Archivos adjuntos en la fuente oficial (no reproducidos aquí): "
                   + ", ".join(names) + f" — https://www.bcn.cl/leychile/navegar?idNorma={idn}")
        out.append("")
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main():
    targets = json.load(open(os.path.join(RAW, "targets.json"), encoding="utf-8"))
    for t in targets:
        path = os.path.join(RAW, "xml", f"{t['idNorma']}.xml")
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        if t["kind"] == "constitucion":
            rel = os.path.join("constitucion", "constitucion-politica-de-la-republica.md")
        else:
            rel = os.path.join("codigos", slugify(t["titulo"]) + ".md")
        md = convert(t, path)
        dest = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print(f"{rel}  {len(md)//1024} KiB")


if __name__ == "__main__":
    main()
