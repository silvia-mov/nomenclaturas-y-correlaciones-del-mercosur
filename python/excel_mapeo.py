"""Arma el Excel del mapeo NCM 2002-2006 a partir de versiones.json y cadena_2002_2006.json.

Uso: python python/excel_mapeo.py datos/versiones.json datos/cadena_2002_2006.json salidas/Mapeo_NCM_2002-2006.xlsx
"""
import json, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

vers_path, cad_path, out = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
ORDEN = C['orden']
MESES = {1: 'Enero', 4: 'Abril', 7: 'Julio', 9: 'Setiembre', 10: 'Octubre', 11: 'Noviembre'}
def fecha(v): return f"{MESES[V[v]['mes']]} {V[v]['anio']}"
def fmt(c): return f'{c[:4]}.{c[4:6]}.{c[6:]}'
def desc(v, c): return V[v]['codigos'].get(c, [''])[0]

A = 'Arial'
HF = Font(name=A, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='39B89A')
B = Font(name=A, size=10); BB = Font(name=A, size=10, bold=True)
T = Font(name=A, size=14, bold=True, color='39B89A'); SUB = Font(name=A, size=11, bold=True, color='FF5883')
COLOR = {'se divide': 'B9EEE1', 'se fusiona': 'FEC9D7', 'complejo': 'FF91AD', 'renumerado': '79D3BE'}

def header(ws, row, cols, widths=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row, j, h); c.font = HF; c.fill = HFILL
        c.alignment = Alignment(wrap_text=True, vertical='center')
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w

def body(ws, r0):
    for row in ws.iter_rows(min_row=r0):
        for c in row:
            if c.font is None or c.font.name != A or not c.font.b:
                c.font = B

wb = openpyxl.Workbook()

# ---------- Mapeo ----------
wm = wb.active; wm.title = 'Mapeo_a_oct2006'
header(wm, 1, ['Código', 'Código (formato)', 'Válido desde', 'Válido hasta', 'Descripción (en "válido desde")',
               'Tipo de cambio hasta oct-2006', 'Código en oct-2006', 'Descripción en oct-2006',
               'Destinos de este código', 'Camino (paso: qué pasó)'],
       [10, 12, 14, 14, 50, 16, 12, 50, 10, 90])
r = 2
for g in sorted(C['agrupado'], key=lambda g: (g['codigo'], [o for o, _ in ORDEN].index(g['desde']))):
    for d in g['destino']:
        wm.append([g['codigo'], fmt(g['codigo']), fecha(g['desde']), fecha(g['hasta']), desc(g['desde'], g['codigo']),
                   g['tipo'], d, desc('NCM_2006_10', d), len(g['destino']), ' | '.join(g['camino'])])
        r += 1
NM = r - 1
for k, col in COLOR.items():
    wm.conditional_formatting.add(f'F2:F{NM}', FormulaRule(formula=[f'$F2="{k}"'], fill=PatternFill('solid', fgColor=col)))
wm.freeze_panes = 'C2'; wm.auto_filter.ref = f'A1:J{NM}'; wm.row_dimensions[1].height = 32
body(wm, 2)

# ---------- Cambios por paso ----------
wc = wb.create_sheet('Cambios_por_paso')
header(wc, 1, ['Paso', 'Código viejo', 'Descripción vieja', 'Marca SAREM', 'Código nuevo', 'Descripción nueva', 'Tipo de cambio'],
       [24, 11, 50, 9, 11, 50, 14])
for p in C['pasos']:
    nombre = f"{fecha(p['de'])} → {fecha(p['a'])}"
    for o, d, ex, t in p['filas']:
        wc.append([nombre, o, desc(p['de'], o), 'ex' if ex else '', d, desc(p['a'], d), t])
NC = wc.max_row
for k, col in COLOR.items():
    wc.conditional_formatting.add(f'G2:G{NC}', FormulaRule(formula=[f'$G2="{k}"'], fill=PatternFill('solid', fgColor=col)))
wc.freeze_panes = 'B2'; wc.auto_filter.ref = f'A1:G{NC}'
body(wc, 2)

# ---------- Versiones ----------
wv = wb.create_sheet('Versiones', 0)
header(wv, 1, ['Versión', 'Número SAREM', 'Códigos de 8 dígitos', 'Aparecen', 'Desaparecen', 'Título en el archivo'],
       [16, 14, 12, 11, 12, 60])
prev = None
for v, sid in ORDEN + [('NCM_2006_11', '(sin tabla)')]:
    s = set(V[v]['codigos'])
    wv.append([fecha(v), sid, len(s), len(s - prev) if prev is not None else '', len(prev - s) if prev is not None else '', V[v]['titulo']])
    prev = s
body(wv, 2)

# ---------- Resumen por paso (fórmulas sobre Cambios_por_paso) ----------
wr = wb.create_sheet('Resumen', 0)
wr['A1'] = 'Mapeo de la NCM, tramo enero 2002 – octubre 2006'; wr['A1'].font = T
wr['A2'] = 'Cantidad de códigos viejos según el tipo de cambio en cada paso (fuente: correlaciones de SAREM entre versiones seguidas).'
wr['A2'].font = Font(name=A, size=10, italic=True)
cols = ['Paso', 'Códigos en la versión vieja', 'Igual', 'Se divide', 'Se fusiona', 'Complejo', 'Renumerado']
for j, h in enumerate(cols, 1):
    c = wr.cell(4, j, h); c.font = HF; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
rng = f'Cambios_por_paso!$A$2:$A${NC}'; rngt = f'Cambios_por_paso!$G$2:$G${NC}'; rngo = f'Cambios_por_paso!$B$2:$B${NC}'
for i, p in enumerate(C['pasos']):
    rr = 5 + i
    wr.cell(rr, 1, f"{fecha(p['de'])} → {fecha(p['a'])}")
    wr.cell(rr, 2, len(V[p['de']]['codigos']))
    for j, t in zip(range(4, 8), ['se divide', 'se fusiona', 'complejo', 'renumerado']):
        # códigos viejos distintos: cada fila es un par, se cuentan códigos con SUMPRODUCT/COUNTIFS
        wr.cell(rr, j, f'=SUMPRODUCT(({rng}=$A{rr})*({rngt}="{t}")/COUNTIFS({rng},{rng}&"",{rngo},{rngo}&""))')
    wr.cell(rr, 3, f'=B{rr}-SUM(D{rr}:G{rr})')
last = 4 + len(C['pasos'])
for row in wr.iter_rows(min_row=5, max_row=last):
    for c in row:
        c.font = B
    for c in row[1:]:
        c.number_format = '#,##0'
for col, w in zip('ABCDEFG', [30, 14, 10, 10, 10, 10, 11]):
    wr.column_dimensions[col].width = w
r0 = last + 2
wr.cell(r0, 1, 'Control: la cadena armada paso a paso contra las tablas directas de SAREM desde enero 2002').font = SUB
for j, h in enumerate(['Hasta', 'Pares en la cadena', 'Pares en SAREM', 'Solo en la cadena', 'Solo en SAREM'], 1):
    c = wr.cell(r0 + 1, j, h); c.font = HF; c.fill = HFILL
for i, k in enumerate(C['controles']):
    rr = r0 + 2 + i
    vals = [fecha(k['hasta']), k['pares_cadena'], k['pares_sarem'], len(k['solo_cadena']), len(k['solo_sarem'])]
    for j, v in enumerate(vals, 1):
        c = wr.cell(rr, j, v); c.font = B

# ---------- Leeme ----------
wl = wb.create_sheet('Leeme', 0)
notas = [
    ('Qué es', None),
    ('1.', 'El mapeo de la NCM entre enero 2002 y octubre 2006: para cada código, a qué código (o códigos) de la NCM de octubre 2006 corresponde.'),
    ('2.', 'Fuente: sistema SAREM del MERCOSUR (versiones de la NCM y tablas de correlación). Ver originales/LEEME.md del repositorio nomenclaturas.'),
    ('3.', 'Se usaron solo las 10 tablas de SAREM entre versiones seguidas, y se encadenaron.'),
    ('Hojas', None),
    ('Resumen', 'Tipos de cambio en cada paso y control contra SAREM.'),
    ('Mapeo_a_oct2006', 'La hoja principal. Una fila por código, período de validez y código de destino en octubre 2006.'),
    ('Cambios_por_paso', 'Solo los códigos que cambiaron en cada paso, con la marca "ex" de SAREM.'),
    ('Versiones', 'Las 12 versiones de la NCM del tramo y su número interno en SAREM.'),
    ('Cómo leer el mapeo', None),
    ('Válido desde / hasta', 'Un mismo número de código puede llegar a destinos distintos según la fecha. Ejemplo: 0302.69.90 de 2002 se reparte en 15 códigos; el de 2003 en adelante sigue igual.'),
    ('Tipo de cambio', 'Igual: mismo código. Se divide: un código viejo pasa a varios nuevos. Se fusiona: varios viejos van a uno nuevo. Complejo: las dos cosas a la vez. Renumerado: cambia el número, 1 a 1 (no hubo casos en este tramo).'),
    ('Marca "ex" de SAREM', 'En SAREM, "ex" aparece solo cuando el código nuevo recibe mercadería de más de un código viejo. Las divisiones NO llevan "ex". Comprobado en las 19.853 filas de las 10 tablas, sin excepciones.'),
    ('Para usarlo', 'Si un código "se divide" o es "complejo", la correspondencia es parcial: hay que mirar la descripción para saber a cuál de los destinos va cada producto.'),
    ('Controles', None),
    ('Tablas completas', 'En las 10 tablas, todos los códigos viejos existen en la versión vieja y todos los nuevos en la nueva. Cada código que desaparece tiene destino y cada código que aparece tiene origen.'),
    ('Contra SAREM', 'La cadena da exactamente los mismos pares que las tablas directas de SAREM desde enero 2002 hasta enero 2003, julio 2003, enero 2004 y julio 2004.'),
    ('Problemas de SAREM', None),
    ('Enero 2003 ↔ enero 2004', 'Las tablas NCM_200213_NCM_200225 y la inversa dicen ser de enero 2004, pero sus códigos son los de enero 2005 (109 códigos que no existían en enero 2004). No se usaron.'),
    ('2006 → enero 2007', 'Las tablas desde enero 2006 y desde julio 2006 hacia enero 2007 parten en realidad de octubre 2006 y tienen filas "suprimido" y "eliminado". Quedan para el tramo siguiente.'),
]
wl['A1'] = 'Léeme'; wl['A1'].font = T
r = 3
for k, v in notas:
    if v is None:
        if r > 3: r += 1
        wl.cell(r, 1, k).font = SUB
    else:
        wl.cell(r, 1, k).font = BB; wl.cell(r, 2, v).font = B
        wl.cell(r, 1).alignment = wl.cell(r, 2).alignment = Alignment(wrap_text=True, vertical='top')
    r += 1
wl.column_dimensions['A'].width = 26; wl.column_dimensions['B'].width = 110

wb._sheets = [wb[n] for n in ['Leeme', 'Resumen', 'Mapeo_a_oct2006', 'Cambios_por_paso', 'Versiones']]
wb.active = 0
wb.save(out)
print('ok', NM - 1, 'filas de mapeo', NC - 1, 'filas de cambios')
