# LawCodex — Chile (cl)

Chilean legislation as Markdown, from **Ley Chile**, the official legislative database of the
Biblioteca del Congreso Nacional de Chile (BCN): https://www.bcn.cl/leychile

Part of [LawCodex](https://github.com/LawCodex): one public repository per jurisdiction.

Retrieved: **2026-10-12**. Language: Spanish (`es`), the only official language.

## What is covered

| Category | Directory | Files |
|---|---|---|
| Constitución Política de la República (consolidated text, D.S. 100 of 2005, as amended) | `constitucion/` | 1 |
| Codes (all 15 codes listed by Ley Chile on its *Códigos* page) | `codigos/` | 15 |
| Leyes | `leyes/` | 0 (not collected, see below) |
| Decretos con fuerza de ley (DFL) | `dfl/` | 0 (not collected, see below) |
| Decretos ley (DL) | `dl/` | 0 (not collected, see below) |
| **Total** | | **16** |

Every text is the current consolidated version (*texto actualizado*) as published by Ley Chile,
without BCN's editorial margin notes (`conNotas=False`).

| Text | Official norm | Ley Chile idNorma | Last amended |
|---|---|---|---|
| [Constitución Política de la República de Chile](constitucion/constitucion-politica-de-la-republica.md) | Decreto 100 (2005) | 242302 | 2026-04-16 |
| [Código Aeronáutico](codigos/codigo-aeronautico.md) | Ley 18.916 | 30287 | 2026-01-19 |
| [Código Civil](codigos/codigo-civil.md) | DFL 1 (2000), Justicia | 172986 | 2025-08-28 ¹ |
| [Código de Aguas](codigos/codigo-de-aguas.md) | DFL 1.122 (1981) | 5605 | 2026-10-09 |
| [Código de Comercio](codigos/codigo-de-comercio.md) | Código de Comercio (1865) | 1974 | 2023-09-23 |
| [Código de Derecho Internacional Privado](codigos/codigo-de-derecho-internacional-privado.md) | Decreto 374 (1934), Código Bustamante | 12820 | 1934-04-25 |
| [Código de Justicia Militar](codigos/codigo-de-justicia-militar.md) | Decreto 2.226 (1944) | 18914 | 2023-04-10 |
| [Código de Minería](codigos/codigo-de-mineria.md) | Ley 18.248 | 29668 | 2023-12-30 |
| [Código de Procedimiento Civil](codigos/codigo-de-procedimiento-civil.md) | Ley 1.552 (1902) | 22740 | 2022-06-30 |
| [Código de Procedimiento Penal](codigos/codigo-de-procedimiento-penal.md) | Ley 1.853 (1906) | 22960 | 2012-06-27 |
| [Código del Trabajo](codigos/codigo-del-trabajo.md) | DFL 1 (2002), Trabajo | 207436 | 2026-07-23 |
| [Código Orgánico de Tribunales](codigos/codigo-organico-de-tribunales.md) | Ley 7.421 (1943) | 25563 | 2026-04-02 |
| [Código Penal](codigos/codigo-penal.md) | Código Penal (1874) | 1984 | 2026-08-20 ¹ |
| [Código Procesal Penal](codigos/codigo-procesal-penal.md) | Ley 19.696 | 176595 | 2026-07-22 |
| [Código Sanitario](codigos/codigo-sanitario.md) | DFL 725 (1967) | 5595 | 2025-09-29 |
| [Código Tributario](codigos/codigo-tributario.md) | DL 830 (1974) | 6374 | 2025-07-11 |

¹ Ley Chile's latest version of these codes (version date `2222-02-02`) already incorporates a few
amendments whose entry into force is undetermined; such files carry `pending_amendments: true`
in their front matter. The code is reproduced exactly as Ley Chile's latest version.

Where a code is enacted inside a larger norm (e.g. the Código Civil within DFL 1 of 2000, which
also consolidates the Registro Civil law and others; the Código del Trabajo within DFL 1 of 2002;
the Código Tributario as article 1 of DL 830), the whole norm is reproduced, with the code under
its *Doble articulado* heading.

## What is NOT covered, and why

**Leyes (≈21,800 numbered laws), DFLs, DLs and decretos supremos are not included.**

Ley Chile's API terms of use (*Condiciones de uso API Ley Chile*, v1.1, section 3 "Usos
prohibidos", linked from https://www.bcn.cl/leychile — API documentation at
https://www.bcn.cl/leychile/leychile-api-doc/leychile-api-doc) expressly prohibit, without the
express authorisation of the Biblioteca:

- "Realizar extracciones masivas, sistemáticas o automatizadas de datos, directa o indirectamente,
  a través de la API, con el objeto de replicar, reconstruir o generar una base de datos
  sustancialmente equivalente a Ley Chile";
- "Utilizar la API para fines de indexación masiva, creación de repositorios estructurados de gran
  escala o almacenamiento persistente que excedan los fines declarados de uso".

These are classed as *infracciones gravísimas*. The standard quota is 500 requests per API key per
24 hours, and quota extensions are reserved to public institutions with a cooperation agreement
(*convenio*), at the discretion of the BCN Director. The legacy key-less XML service still answers
single-norm requests, but its listing service (`servicio 39`, all idNorma by type) already requires
an API key. Collecting every law would therefore be exactly the kind of systematic replication the
terms forbid, so this repository was limited to a small number of individual retrievals (16 norm
requests plus one request for the list of codes, spaced 5 s apart).

Other sources were checked and are not usable for a full corpus:

- **Diario Oficial** (https://www.diariooficial.interior.gob.cl): `robots.txt` disallows
  `/publicaciones/` and `/edicionelectronica/`; it only carries original (non-consolidated)
  publications, electronic edition since 2016.
- **datos.bcn.cl** (BCN linked open data / SPARQL endpoint): metadata only (titles, numbers,
  dates, links to Ley Chile), no consolidated text; partially outdated (e.g. DFL entries end in 2022).

**Consent needed to complete the corpus:** written authorisation from the Biblioteca del Congreso
Nacional (Sección Ley Chile, contact: https://www.bcn.cl/leychile/consulta/contacto) for a
one-time bulk export or an API quota extension covering all *Leyes*, *Decretos con Fuerza de
Ley* and *Decretos Ley* (≈30,000 norms), for non-commercial publication with attribution. With
such authorisation the scripts below can be extended (enumerate `idLey=1…21842` and the DFL/DL
idNorma lists from datos.bcn.cl) to fill `leyes/<year>/ley-<n>-<slug>.md`, `dfl/` and `dl/`.

Also not included: BCN's editorial notes (*notas*), history of the law (*historia de la ley*),
earlier versions, attached binary files (e.g. scanned PDFs/images — referenced by name at the end
of the affected files, with a link to the official page), decretos supremos, resoluciones and
other secondary regulation, treaties.

## Format

One Markdown file per norm, UTF-8, LF. YAML front matter:

```yaml
title: "Código Penal"
identifier: "1984"                 # Ley Chile idNorma
norma: "Código PENAL"              # official type and number as given by Ley Chile
official_title: "..."              # TituloNorma
type: code                         # constitution | code
jurisdiction: cl
language: es
issuer: "MINISTERIO DE JUSTICIA"
date: 1874-11-12                   # promulgation
published: 1874-11-12              # publication in the Diario Oficial
last_amended: 2026-08-20           # Ley Chile version date
status: in_force
source: "https://www.bcn.cl/leychile/navegar?idNorma=1984"
source_xml: "https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=1984&conNotas=False"
retrieved: 2026-10-12
```

The body follows Ley Chile's structural markup (*EstructurasFuncionales*): Libro / Título /
Párrafo / Capítulo / Sección headings map to `##`…`######`, each article (or transitional
provision) gets its own heading, deeper levels fall back to **bold** labels. The article text is
reproduced verbatim (including the article's own number line, e.g. "ART. 8." or
"Artículo 1°.-"). The decree's preamble (*encabezado*) precedes the structure and the promulgation
formula closes it.

## Licence / copyright

Per Ley Chile's terms of use (section 9 "Licencia y propiedad intelectual"), the legal,
regulatory, administrative and judicial texts disseminated through Ley Chile are outside the scope
of copyright ("los textos oficiales de carácter público no son objeto de propiedad intelectual");
the BCN claims no copyright over them. BCN's own metadata, schemas, descriptors and compilations are
licensed CC BY-NC-ND 4.0. Source attribution: **"Ley Chile – Biblioteca del Congreso Nacional"**,
retrieved 2026-10-12. This repository is non-commercial and makes no claim to be an official
publication; only the Diario Oficial and Ley Chile are authoritative. Nothing here is an
interpretation by the BCN.

## Regenerate

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/cl_fetch.py      # downloads XML into ../_raw/cl/ (override with CL_RAW=...)
python3 scripts/cl_convert.py    # writes constitucion/ and codigos/
```

`cl_fetch.py` uses the descriptive User-Agent `LawCodex/1.0 (+https://github.com/LawCodex)`, waits
5 s between requests and caches downloads. www.leychile.cl / www.bcn.cl publish no robots.txt rules
for these paths (datos.bcn.cl asks for `Crawl-delay: 10`; only a handful of SPARQL queries were made
there while evaluating sources).
