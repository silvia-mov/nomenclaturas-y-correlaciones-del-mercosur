"""Lee las tablas de correlación de la OMA (Tabla II, 6 dígitos) y las guarda como pares.

Los PDF se bajan de la página de la OMA y se guardan en originales/oma/ (no se publican aquí):
  SA 2012 -> 2017: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs_nomenclature_previous_editions/hs-nomenclature-2017-edition/correlation-tables-hs-2012-to-2017.aspx
    - table_ii_trp1217_en_rev1.pdf  (Tabla II, octubre 2016; ya incluye la corrección 2)
    - table_ii_a_trp1217_en.pdf     (anexo de la Tabla II, capítulo 44)
  SA 2017 -> 2022: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition/correlation-tables-hs-2017-2022.aspx
    - table-ii_en.pdf               (Tabla II, noviembre 2020)

Uso: python python/leer_oma.py originales/oma datos
Crea datos/oma_2012_2017.json y datos/oma_2017_2022.json. Necesita pdftotext (poppler).

Cada par es (origen, destino, ex). El origen puede ser:
  - una subpartida de 6 dígitos (por ejemplo "030211");
  - una partida de 4 dígitos, cuando la OMA escribe la partida ("30.04") o una lista de partidas en
    texto ("Applicable subheadings, in particular in headings 84.13, 84.14, ...");
  - un capítulo de 2 dígitos, cuando la OMA escribe "in particular in Chapters 84, 85, 90 ...".
En los dos últimos casos cualquier subpartida de esa partida o capítulo puede ir a esos destinos,
además de seguir en su propia subpartida.
"""
import json, os, re, subprocess, sys

carpeta, salida = sys.argv[1:3]
EDICIONES = {
    '2012_2017': {'tabla': ['table_ii_trp1217_en_rev1.pdf'], 'anexo44': ['table_ii_a_trp1217_en.pdf'], 'minimo': 600},
    '2017_2022': {'tabla': ['table-ii_en.pdf'], 'anexo44': [], 'minimo': 600},
}
# Errores de tipeo del PDF (se corrigen antes de leer).
# SA 2017 -> 2022: "28933.34" es la subpartida 2933.34 con la nota 2 pegada; "8549,29" es 8549.29.
ARREGLOS = {'28933.34': '2933.34', '8549,29': '8549.29'}
COL = 62   # a partir de esta columna del texto empieza la columna de la edición nueva

COD = re.compile(r'(?<![\d.])(\d{4})\.(\d{2})(?![\d])')
DEST = re.compile(r'(ex\s?)?(?<![\d.])(\d{4})\.(\d{2})(?![\d])')
PARTIDA = re.compile(r'(?<![\d.])(\d{2})\.(\d{2})(?!\d)(?!\.\d)')   # admite punto final ("95.06.")


def origenes_de_texto(texto):
    """Partidas (4 dígitos) y capítulos (2 dígitos) nombrados en un bloque de texto."""
    out = {a + b for a, b in PARTIDA.findall(texto)}
    for m in re.finditer(r'Chap(?:ter|itre)s?\s+([\d,\s]+(?:(?:and|et)\s+\d{2})?)', texto):
        out |= set(re.findall(r'\b(\d{2})\b', m.group(1)))
    return out


def leer(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    for mal, bien in ARREGLOS.items():
        txt = txt.replace(mal, bien)
    entradas, cur = [], None
    for line in txt.splitlines():
        izq, der = line[:COL], line[COL:]
        c = COD.search(izq)
        p = re.fullmatch(r'\s*(\d{2})\.(\d{2})\s*', izq)
        if c:
            cur = {'origen': {c.group(1) + c.group(2)}, 'texto': None, 'dest': []}
            entradas.append(cur)
        elif p:
            cur = {'origen': {p.group(1) + p.group(2)}, 'texto': None, 'dest': []}
            entradas.append(cur)
        elif re.search(r'Applicable subheadings|Sous-positions applicables', izq):
            cur = {'origen': set(), 'texto': izq, 'dest': []}
            entradas.append(cur)
        elif cur is not None and cur['texto'] is not None and izq.strip():
            cur['texto'] += ' ' + izq
        if cur is not None:
            for m in DEST.finditer(der):
                cur['dest'].append((m.group(2) + m.group(3), bool(m.group(1))))
    pares = []
    for e in entradas:
        origen = e['origen'] if e['texto'] is None else origenes_de_texto(e['texto'])
        for o in sorted(origen):
            for d, ex in e['dest']:
                pares.append((o, d, ex))
    return pares


for ed, cfg in EDICIONES.items():
    tabla = [p for f in cfg['tabla'] for p in leer(os.path.join(carpeta, f))]
    anexo = [p for f in cfg['anexo44'] for p in leer(os.path.join(carpeta, f))]
    assert len(tabla) > cfg['minimo'], (ed, len(tabla))
    json.dump({'fuente': f'OMA, Tabla II SA {ed.replace("_", " -> ")}', 'tabla': tabla, 'anexo44': anexo},
              open(os.path.join(salida, f'oma_{ed}.json'), 'w'), ensure_ascii=False)
    por = {n: len({a for a, _, _ in tabla if len(a) == n}) for n in (6, 4, 2)}
    print(f'SA {ed}: {len(tabla)} pares | orígenes: {por[6]} subpartidas, {por[4]} partidas, {por[2]} capítulos | anexo {len(anexo)}')
