"""Lee las tablas de correlación de la OMA (Tabla II, 6 dígitos) y las guarda como pares.

Los PDF se bajan de la página de la OMA y se guardan en originales/oma/ (no se publican aquí):
  SA 2002 -> 2007: hs_correlation2007_table_ii_e_rev4cor.pdf (Tabla II con las correcciones 1, 2, 3 y 5;
                   la corrección 4 solo cambia la Tabla I)
  SA 2007 -> 2012: ii_trp0712rev3eng_fr.pdf (Tabla II con las correcciones 1 y 2)
  (las dos vienen en la release "OMA" del repositorio varios y en la página de ediciones anteriores de la OMA)
  SA 2012 -> 2017: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs_nomenclature_previous_editions/hs-nomenclature-2017-edition/correlation-tables-hs-2012-to-2017.aspx
    - table_ii_trp1217_en_rev1.pdf  (Tabla II, octubre 2016; ya incluye la corrección 2)
    - table_ii_a_trp1217_en.pdf     (anexo de la Tabla II, capítulo 44)
  SA 2017 -> 2022: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition/correlation-tables-hs-2017-2022.aspx
    - table-ii_en.pdf               (Tabla II, noviembre 2020)

Uso: python python/leer_oma.py originales/oma datos
Crea datos/oma_AAAA_AAAA.json para cada edición. Necesita pdftotext (poppler).

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
EDICIONES = {   # col = columna del texto donde empieza la columna de la edición nueva
    '2002_2007': {'tabla': ['hs_correlation2007_table_ii_e_rev4cor.pdf'], 'anexo44': [], 'minimo': 700, 'col': 35},
    '2007_2012': {'tabla': ['ii_trp0712rev3eng_fr.pdf'], 'anexo44': [], 'minimo': 300, 'col': 30},
    '2012_2017': {'tabla': ['table_ii_trp1217_en_rev1.pdf'], 'anexo44': ['table_ii_a_trp1217_en.pdf'], 'minimo': 600, 'col': 62},
    '2017_2022': {'tabla': ['table-ii_en.pdf'], 'anexo44': [], 'minimo': 600, 'col': 62},
}
# Errores de tipeo del PDF (se corrigen antes de leer).
# SA 2017 -> 2022: "28933.34" es la subpartida 2933.34 con la nota 2 pegada; "8549,29" es 8549.29.
ARREGLOS = {'28933.34': '2933.34', '8549,29': '8549.29'}

COD = re.compile(r'(?<![\d.])(\d{4})\.(\d{2})(?![\d])')
DEST = re.compile(r'(ex\s?)?(?<![\d.])(\d{4})\.(\d{2})(?![\d])')
PARTIDA = re.compile(r'(?<![\d.])(\d{2})\.(\d{2})(?!\d)(?!\.\d)')   # admite punto final ("95.06.")
TEXTO = re.compile(r'Applicable subheadings|Sous-positions applicables')


def prefijos_de_texto(texto):
    """Partidas (4 dígitos) y capítulos (2 dígitos) nombrados en un bloque de texto."""
    out = {a + b for a, b in PARTIDA.findall(texto)}
    for m in re.finditer(r'Chap(?:ter|itre)s?\s+([\d,\s]+(?:(?:and|et)\s+\d{2})?)', texto):
        out |= set(re.findall(r'\b(\d{2})\b', m.group(1)))
    return out


def leer(pdf, col):
    """Pares (origen, destino, ex). Origen y destino pueden ser subpartida (6), partida (4) o capítulo (2):
    la OMA a veces escribe "subpartidas aplicables, en particular de las partidas o capítulos ..." del lado
    de la edición vieja (origen) o del lado de la nueva (destino)."""
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    for mal, bien in ARREGLOS.items():
        txt = txt.replace(mal, bien)
    entradas, cur = [], None
    texto_o = texto_d = False      # se está juntando texto del lado viejo (origen) o del nuevo (destino)
    for line in txt.splitlines():
        if not line.strip():
            texto_d = False
            continue
        tl = [m for m in TEXTO.finditer(line) if m.start() < col]
        tr = [m for m in TEXTO.finditer(line) if m.start() >= col]
        izq, der = line[:col], line[col:]
        c = COD.search(izq)
        p = re.fullmatch(r'\s*(\d{2})\.(\d{2})\s*', izq)
        if c or p:
            cod = c.group(1) + c.group(2) if c else p.group(1) + p.group(2)
            cur = {'origen': {cod}, 'texto_o': None, 'dest': [], 'texto_d': '', 'prev': None}
            entradas.append(cur); texto_o = texto_d = False
        elif tl:
            cur = {'origen': set(), 'texto_o': izq, 'dest': [], 'texto_d': '', 'prev': cur}
            entradas.append(cur); texto_o, texto_d = True, False
        elif texto_o and izq.strip():
            cur['texto_o'] += ' ' + izq
        if cur is None:
            continue
        if tr:
            texto_d = True
        if texto_d:
            cur['texto_d'] += ' ' + der
        else:
            for m in DEST.finditer(der):
                cur['dest'].append((m.group(2) + m.group(3), bool(m.group(1))))
    pares = []
    for e in entradas:
        origen = e['origen'] if e['texto_o'] is None else prefijos_de_texto(e['texto_o'])
        if e['texto_o'] is not None and not origen and e['prev'] is not None:
            origen = e['prev']['origen']   # "Applicable subheadings" que repite el origen de la línea anterior (30.04)
        dest = list(e['dest']) + [(x, True) for x in sorted(prefijos_de_texto(e['texto_d']))]
        for o in sorted(origen):
            for d, ex in dest:
                pares.append((o, d, ex))
    return pares


for ed, cfg in EDICIONES.items():
    tabla = [p for f in cfg['tabla'] for p in leer(os.path.join(carpeta, f), cfg['col'])]
    anexo = [p for f in cfg['anexo44'] for p in leer(os.path.join(carpeta, f), cfg['col'])]
    assert len(tabla) > cfg['minimo'], (ed, len(tabla))
    json.dump({'fuente': f'OMA, Tabla II SA {ed.replace("_", " -> ")}', 'tabla': tabla, 'anexo44': anexo},
              open(os.path.join(salida, f'oma_{ed}.json'), 'w'), ensure_ascii=False)
    por = {n: len({a for a, _, _ in tabla if len(a) == n}) for n in (6, 4, 2)}
    pd = {n: len({b for _, b, _ in tabla if len(b) == n}) for n in (6, 4, 2)}
    print(f'SA {ed}: {len(tabla)} pares | orígenes: {por[6]} subpartidas, {por[4]} partidas, {por[2]} capítulos | '
          f'destinos: {pd[6]} subpartidas, {pd[4]} partidas, {pd[2]} capítulos | anexo {len(anexo)}')
