"""Listas de Paraguay notificadas al MERCOSUR: BK, BIT, LNE y Régimen de Materias Primas (RMP).

Lee las notificaciones de Paraguay (releases "mercosur_listas" del repositorio varios, ya descomprimidas
en una carpeta), y para cada código:
  - toma el arancel nacional vigente (ANV) que figura en la notificación;
  - busca la versión de la NCM vigente en la fecha de la notificación;
  - lo traduce a la última versión de la NCM con el mapeo (datos/cadena.json).

Uso: python python/listas_notificadas.py <carpeta con los zip descomprimidos> datos/versiones.json datos/cadena.json datos/listas salidas/Listas_BK_BIT_LNE_RMP.xlsx
"""
import csv, glob, hashlib, json, os, re, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

carpeta, vers_path, cad_path, salida_csv, salida_xlsx = sys.argv[1:6]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
V.update(C.get('versiones_extra', {}))
ORDEN = [v for v, _ in C['orden']]
IDX = {v: i for i, v in enumerate(ORDEN)}
FIN = C['fin']

# Notificaciones de Paraguay: etiqueta, fecha (verificada en el encabezado de cada archivo) y archivo.
# Se dejan afuera: el archivo "al 31.07.2026" (adentro dice 31/01/2026 y es idéntico al de enero 2026),
# la versión "copia" de julio 2022 (se usa el anexo original) y las listas de Uruguay.
NOTIFS = [
    ('2018-S1', '2018-06-30', '2018-08-07 Nota MRE-Py 095*'),
    ('2020-01', '2020-01-31', 'Notificaci*31_01_2020-PY_rev.xlsx'),
    ('2020-07', '2020-07-31', '83612_*'),
    ('2021-01', '2021-01-31', '85815_*'),
    ('2021-07', '2021-07-31', 'MRE-PY_E267_2022*'),
    ('2022-01', '2022-01-31', 'MRE-PY_E975_2022*'),
    ('2022-07', '2022-07-31', 'MRE-PY_E1742_2022*_ANE.xlsx'),
    ('2023-07', '2023-07-31', '96835_*'),
    ('2023-12', '2023-12-31', '99502_*'),
    ('2025-01', '2025-01-31', '105305_*'),
    ('2025-07', '2025-07-31', '*31.07.2025*'),
    ('2026-01', '2026-01-31', '*31.01.2026*'),
]
# Régimen de Materias Primas: listas anuales (el arancel dentro del régimen es 0 %).
RMP = [('2018', '2018-01-01', 'MRE-PY_E001_2021*(5).xlsx', 'AÑO 2018'),
       ('2019', '2019-01-01', 'MRE-PY_E001_2021*(5).xlsx', 'AÑO 2019'),
       ('2020-S1', '2020-01-01', 'MRE-PY_E001_2021*(5).xlsx', '1ER SEMESTRE 2020'),
       ('2023', '2023-01-01', 'RMP.LISTA_2023-2024(6).xlsx', 'AÑO 2023'),
       ('2024', '2024-01-01', 'RMP.LISTA_2023-2024(6).xlsx', 'AÑO 2024'),
       ('2025', '2025-01-01', 'RMP.LISTA_2025.xlsx', 'AÑO 2025')]
NOMBRE = {'BK': 'Bienes de capital', 'BIT': 'Bienes de informática y telecomunicaciones',
          'LNE': 'Lista nacional de excepciones al AEC', 'RMP': 'Régimen de materias primas'}


def uno(pat):
    m = sorted(glob.glob(os.path.join(carpeta, '**', pat), recursive=True))
    distintos = {hashlib.md5(open(f, 'rb').read()).hexdigest() for f in m}
    assert len(distintos) == 1, (pat, m)
    return m[0]


def nombre_archivo(f):
    b = os.fsencode(os.path.basename(f))
    try:
        return b.decode('utf-8')
    except UnicodeDecodeError:
        return b.decode('cp437')


def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip().replace(',', '.'))
    except (TypeError, ValueError):
        return None


def leer_notif(f):
    """{lista: [(ncm8, anv)]} de una notificación con hojas BK, BIT y LNE."""
    out = {}
    for ws in openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets:
        nombre = ws.title.strip().upper()
        if nombre not in ('BK', 'BIT', 'LNE'):
            continue
        col, items = None, []
        for r in ws.iter_rows(values_only=True):
            r = list(r)
            if col is None:
                cand = [i for i, c in enumerate(r) if isinstance(c, str) and c.strip().startswith('Arancel Nacional')]
                if cand:
                    col = cand[0]
                continue
            if r and r[0] and len(re.sub(r'\D', '', str(r[0]))) == 8:
                items.append((re.sub(r'\D', '', str(r[0])), num(r[col])))
        out[nombre] = items
    return out


def version_en(fecha):
    """Última versión de la NCM con fecha (año, mes) menor o igual a la de la notificación."""
    a, m = int(fecha[:4]), int(fecha[5:7])
    cand = [v for v in ORDEN if (V[v]['anio'], V[v]['mes'] or 1) <= (a, m)]
    return cand[-1]


# mapeo: (código, versión) -> destinos en la última versión
DEST = {}
for g in C['agrupado']:
    for i in range(IDX[g['desde']], IDX[g['hasta']] + 1):
        DEST[(g['codigo'], ORDEN[i])] = (g['destino'], g['tipo'])


def traducir(c, v):
    """Destinos del código c (de la versión v). Si el código no está en esa versión, se busca la versión
    más cercana en la que exista."""
    if (c, v) in DEST:
        return DEST[(c, v)] + (v, '')
    otras = sorted((abs(IDX[w] - IDX[v]), w) for w in ORDEN if (c, w) in DEST)
    if otras:
        w = otras[0][1]
        return DEST[(c, w)] + (w, f'el código no está en {v}; se usó {w}')
    return ([], 'no existe', v, 'el código no existe en ninguna versión de la NCM 2002-2026')


filas = []
for et, fecha, pat in NOTIFS:
    f = uno(pat)
    data = leer_notif(f)
    for lista in ('BK', 'BIT', 'LNE'):
        vistos = {}
        for c, anv in data[lista]:
            vistos.setdefault(c, []).append(anv)
        for c, anvs in vistos.items():
            u = sorted({a for a in anvs if a is not None})
            filas.append({'lista': lista, 'notificacion': et, 'fecha': fecha, 'ncm': c,
                          'anv': u[0] if len(u) == 1 else ' / '.join(f'{a:g}' for a in u), 'archivo': nombre_archivo(f)})
for et, fecha, pat, hoja in RMP:
    f = uno(pat)
    ws = openpyxl.load_workbook(f, read_only=True, data_only=True)[hoja]
    cods = sorted({re.sub(r'\D', '', str(r[0])) for r in ws.iter_rows(values_only=True)
                   if r and r[0] and len(re.sub(r'\D', '', str(r[0]))) == 8})
    for c in cods:
        filas.append({'lista': 'RMP', 'notificacion': et, 'fecha': fecha, 'ncm': c, 'anv': 0.0, 'archivo': nombre_archivo(f)})

for x in filas:
    v = version_en(x['fecha'])
    dest, tipo, usada, aviso = traducir(x['ncm'], v)
    x.update(version_ncm=usada, tipo_cambio=tipo, destinos=dest, aviso=aviso)

# ---------- CSV ----------
os.makedirs(salida_csv, exist_ok=True)
with open(os.path.join(salida_csv, 'listas_notificadas.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['lista', 'notificacion', 'fecha', 'ncm', 'arancel_nacional_vigente', 'version_ncm', 'tipo_cambio',
                f'codigos_{FIN[4:].lower()}', 'aviso', 'archivo'])
    for x in filas:
        w.writerow([x['lista'], x['notificacion'], x['fecha'], x['ncm'], x['anv'], x['version_ncm'], x['tipo_cambio'],
                    ' '.join(x['destinos']), x['aviso'], x['archivo']])
resumen = {}
for x in filas:
    resumen.setdefault((x['lista'], x['notificacion'], x['fecha']), set()).add(x['ncm'])
with open(os.path.join(salida_csv, 'listas_resumen.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['lista', 'notificacion', 'fecha', 'codigos'])
    for (l, et, fe), cs in sorted(resumen.items()):
        w.writerow([l, et, fe, len(cs)])

# ---------- Excel ----------
A = 'Arial'
HF = Font(name=A, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='5E8F88')
B = Font(name=A, size=10); BB = Font(name=A, size=10, bold=True)
T = Font(name=A, size=14, bold=True, color='5E8F88'); SUB = Font(name=A, size=11, bold=True, color='774D78')


def cab(ws, cols, anchos):
    ws.append(cols)
    for c in ws[ws.max_row]:
        c.font, c.fill, c.alignment = HF, HFILL, Alignment(wrap_text=True, vertical='center', horizontal='center')
    for j, a in enumerate(anchos, 1):
        ws.column_dimensions[get_column_letter(j)].width = a


def desc_final(c):
    return V[FIN]['codigos'].get(c, [''])[0]


wb = openpyxl.Workbook()
wl = wb.active; wl.title = 'Leeme'
textos = [
    ('Listas de la nomenclatura', None),
    ('Qué es', 'Las listas de Paraguay notificadas al MERCOSUR, con el arancel nacional vigente de cada código, desde el primer semestre 2018 hasta enero 2026, y cada código traducido a la NCM vigente.'),
    ('BK', 'Bienes de capital. Máquinas y equipos para producir. Paraguay puede cobrarles un arancel distinto del AEC (régimen hasta 2030, Dec. CMC 08/21).'),
    ('BIT', 'Bienes de informática y telecomunicaciones. Computadoras, equipos de comunicación y sus partes. También con régimen propio hasta 2030.'),
    ('LNE', 'Lista nacional de excepciones al AEC. Códigos en los que Paraguay cobra un arancel distinto del común del MERCOSUR (649 códigos autorizados hasta 2030).'),
    ('RMP', 'Régimen de materias primas. Insumos que las industrias pueden importar con arancel 0 % dentro del régimen (la lista cambia cada año).'),
    ('Hojas', None),
    ('Resumen', 'Cuántos códigos tiene cada lista en cada notificación.'),
    ('BK, BIT, LNE', 'Una fila por código y una columna por notificación con el arancel nacional vigente (vacío: no estaba en la lista). Al final, el código en la NCM vigente.'),
    ('RMP', 'Una fila por código y una columna por año ("Sí" si estaba en la lista).'),
    ('Cómo se traduce', 'Cada notificación usa la NCM de su fecha (hasta 2022, la NCM 2017). El código se traduce a la NCM vigente con el mapeo de este repositorio. Si "se divide" o es "complejo", hay que mirar la descripción para saber a cuál de los destinos corresponde.'),
    ('Fuente', 'Notificaciones de Paraguay al MERCOSUR (Comisión de Comercio; POLCOM). Las fechas se tomaron del encabezado de cada archivo. No se usaron: el archivo "al 31.07.2026" (adentro dice 31/01/2026 y es idéntico al de enero 2026), la versión "copia" de julio 2022 y las listas de Uruguay.'),
]
wl['A1'] = 'Léeme'; wl['A1'].font = T
r = 3
for k, v in textos:
    if v is None:
        if r > 3: r += 1
        wl.cell(r, 1, k).font = SUB
    else:
        wl.cell(r, 1, k).font = BB; wl.cell(r, 2, v).font = B
        wl.cell(r, 1).alignment = wl.cell(r, 2).alignment = Alignment(wrap_text=True, vertical='top')
    r += 1
wl.column_dimensions['A'].width = 18; wl.column_dimensions['B'].width = 110

hojas = {}
for lista, etiquetas in (('BK', [n[0] for n in NOTIFS]), ('BIT', [n[0] for n in NOTIFS]), ('LNE', [n[0] for n in NOTIFS]),
                         ('RMP', [n[0] for n in RMP])):
    ws = wb.create_sheet(lista)
    cab(ws, ['NCM', 'Descripción (última notificación en que aparece)'] + etiquetas +
        ['Notificaciones en que aparece', f'Código(s) en la NCM vigente ({FIN[4:].replace("_", "-")})', 'Tipo de cambio', 'Aviso'],
        [11, 50] + [9] * len(etiquetas) + [13, 30, 14, 40])
    cods = sorted({x['ncm'] for x in filas if x['lista'] == lista})
    por = {(x['ncm'], x['notificacion']): x for x in filas if x['lista'] == lista}
    ultimo = {}
    for x in filas:
        if x['lista'] == lista:
            ultimo[x['ncm']] = x
    n0, n1 = 3, 2 + len(etiquetas)
    for i, c in enumerate(cods, start=2):
        u = ultimo[c]
        vals = [(('Sí' if lista == 'RMP' else por[(c, e)]['anv']) if (c, e) in por else None) for e in etiquetas]
        dsc = V[u['version_ncm']]['codigos'].get(c, [''])[0] if u['version_ncm'] in V else ''
        ws.append([c, dsc] + vals + [f'=COUNTA({get_column_letter(n0)}{i}:{get_column_letter(n1)}{i})',
                                     ' '.join(u['destinos']), u['tipo_cambio'], u['aviso']])
    for row in ws.iter_rows(min_row=2):
        for cl in row:
            cl.font = B
        for cl in row[n0 - 1:n1]:
            cl.alignment = Alignment(horizontal='center')
            if lista != 'RMP':
                cl.number_format = '0.0'
    ws.freeze_panes = 'C2'; ws.auto_filter.ref = f'A1:{get_column_letter(n1 + 4)}{len(cods) + 1}'
    ws.row_dimensions[1].height = 45
    hojas[lista] = (ws, etiquetas, len(cods))

wr = wb.create_sheet('Resumen', 1)
wr['A1'] = 'Cantidad de códigos en cada notificación'; wr['A1'].font = T
fila = 3
for lista in ('BK', 'BIT', 'LNE', 'RMP'):
    ws, etiquetas, n = hojas[lista]
    wr.cell(fila, 1, f'{lista}: {NOMBRE[lista]}').font = SUB
    fila += 1
    for j, h in enumerate(['Notificación', 'Códigos'], 1):
        c = wr.cell(fila, j, h); c.font, c.fill = HF, HFILL
    for k, e in enumerate(etiquetas):
        fila += 1
        col = get_column_letter(3 + k)
        wr.cell(fila, 1, e).font = B
        c = wr.cell(fila, 2, f"=COUNTA('{lista}'!{col}2:{col}{n + 1})"); c.font = B; c.number_format = '#,##0'
    fila += 2
wr.column_dimensions['A'].width = 48; wr.column_dimensions['B'].width = 12

wb.save(salida_xlsx)
print({l: len({x['ncm'] for x in filas if x['lista'] == l}) for l in ('BK', 'BIT', 'LNE', 'RMP')},
      '| filas', len(filas), '| avisos', sum(1 for x in filas if x['aviso']),
      '| sin traducir', sum(1 for x in filas if not x['destinos']))
