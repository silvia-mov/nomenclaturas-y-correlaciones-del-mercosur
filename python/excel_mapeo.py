"""Arma el Excel del mapeo de la NCM a partir de versiones.json y cadena.json.

Uso: python python/excel_mapeo.py datos/versiones.json datos/cadena.json salidas/Mapeo_NCM_2002-2019.xlsx
"""
import json, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

vers_path, cad_path, out = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
ORDEN = C['orden']; FIN = C['fin']; INI = ORDEN[0][0]
MESES = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 7: 'Julio', 8: 'Agosto', 9: 'Setiembre', 10: 'Octubre', 11: 'Noviembre'}
def fecha(v): return f"{MESES[V[v]['mes']]} {V[v]['anio']}" if V[v]['mes'] else str(V[v]['anio'])
def corto(v): return fecha(v)[:3].lower() + '-' + str(V[v]['anio'])
def fmt(c): return f'{c[:4]}.{c[4:6]}.{c[6:]}'
def desc(v, c): return V[v]['codigos'].get(c, [''])[0]
FINC = corto(FIN)

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
            if not (c.font and c.font.name == A and c.font.b):
                c.font = B


wb = openpyxl.Workbook()
orden = [v for v, _ in ORDEN]

# ---------- Mapeo ----------
wm = wb.active; wm.title = 'Mapeo'
header(wm, 1, ['Código', 'Código (formato)', 'Válido desde', 'Válido hasta', 'Descripción (en "válido desde")',
               f'Tipo de cambio hasta {FINC}', f'Código en {FINC}', f'Descripción en {FINC}',
               'Destinos de este código', 'Camino (paso: qué pasó)', 'Notas (vínculos agregados o sin respaldo de la OMA)'],
       [10, 12, 15, 15, 50, 16, 12, 50, 10, 90, 60])
for g in sorted(C['agrupado'], key=lambda g: (g['codigo'], orden.index(g['desde']))):
    for d in g['destino']:
        wm.append([g['codigo'], fmt(g['codigo']), fecha(g['desde']), fecha(g['hasta']), desc(g['desde'], g['codigo']),
                   g['tipo'], d, desc(FIN, d), len(g['destino']), ' | '.join(g['camino']), ' | '.join(g.get('notas', []))])
NM = wm.max_row
for k, col in COLOR.items():
    wm.conditional_formatting.add(f'F2:F{NM}', FormulaRule(formula=[f'$F2="{k}"'], fill=PatternFill('solid', fgColor=col)))
wm.freeze_panes = 'C2'; wm.auto_filter.ref = f'A1:K{NM}'; wm.row_dimensions[1].height = 32
body(wm, 2)

# ---------- Cambios por paso ----------
wc = wb.create_sheet('Cambios_por_paso')
header(wc, 1, ['Paso', 'Código viejo', 'Descripción vieja', 'Marca SAREM', 'Código nuevo', 'Descripción nueva', 'Tipo de cambio', 'Nota'],
       [26, 11, 50, 9, 11, 50, 14, 60])
for p in C['pasos']:
    nombre = f"{fecha(p['de'])} → {fecha(p['a'])}"
    for o, d, ex, t, *nota in p['filas']:
        wc.append([nombre, o, desc(p['de'], o), 'ex' if ex else '', d, desc(p['a'], d), t, nota[0] if nota else ''])
NC = wc.max_row
for k, col in COLOR.items():
    wc.conditional_formatting.add(f'G2:G{NC}', FormulaRule(formula=[f'$G2="{k}"'], fill=PatternFill('solid', fgColor=col)))
wc.freeze_panes = 'B2'; wc.auto_filter.ref = f'A1:H{NC}'
body(wc, 2)

# ---------- Versiones ----------
wv = wb.create_sheet('Versiones')
header(wv, 1, ['Versión', 'Número SAREM', 'Códigos de 8 dígitos', 'Aparecen', 'Desaparecen', 'Título en el archivo'],
       [16, 14, 12, 11, 12, 60])
prev = None
for v, sid in ORDEN:
    s = set(V[v]['codigos'])
    wv.append([fecha(v), sid, len(s), len(s - prev) if prev is not None else '', len(prev - s) if prev is not None else '', V[v]['titulo']])
    prev = s
body(wv, 2)

# ---------- Resumen (fórmulas sobre Cambios_por_paso) ----------
wr = wb.create_sheet('Resumen')
wr['A1'] = f'Mapeo de la NCM, {fecha(INI).lower()} – {fecha(FIN).lower()}'; wr['A1'].font = T
wr['A2'] = 'Cantidad de códigos viejos según el tipo de cambio en cada paso (fuente: correlaciones de SAREM).'
wr['A2'].font = Font(name=A, size=10, italic=True)
cols = ['Paso', 'Códigos en la versión vieja', 'Igual', 'Renumerado', 'Se divide', 'Se fusiona', 'Complejo']
for j, h in enumerate(cols, 1):
    c = wr.cell(4, j, h); c.font = HF; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
rng = f'Cambios_por_paso!$A$2:$A${NC}'; rngt = f'Cambios_por_paso!$G$2:$G${NC}'; rngo = f'Cambios_por_paso!$B$2:$B${NC}'
for i, p in enumerate(C['pasos']):
    rr = 5 + i
    wr.cell(rr, 1, f"{fecha(p['de'])} → {fecha(p['a'])}")
    wr.cell(rr, 2, len(V[p['de']]['codigos']))
    for j, t in zip(range(4, 8), ['renumerado', 'se divide', 'se fusiona', 'complejo']):
        # cada fila de Cambios_por_paso es un par: se cuentan códigos viejos distintos
        wr.cell(rr, j, f'=SUMPRODUCT(({rng}=$A{rr})*({rngt}="{t}")/COUNTIFS({rng},{rng}&"",{rngo},{rngo}&""))')
    wr.cell(rr, 3, f'=B{rr}-SUM(D{rr}:G{rr})')
last = 4 + len(C['pasos'])
for row in wr.iter_rows(min_row=5, max_row=last):
    for c in row:
        c.font = B
    for c in row[1:]:
        c.number_format = '#,##0'
for col, w in zip('ABCDEFG', [32, 14, 10, 11, 10, 10, 10]):
    wr.column_dimensions[col].width = w
r0 = last + 2
wr.cell(r0, 1, 'Control: la cadena armada paso a paso contra las tablas directas de SAREM').font = SUB
for j, h in enumerate(['Desde', 'Hasta', 'Pares en la cadena', 'Pares en SAREM', 'Solo en la cadena', 'Solo en SAREM',
                       'Sin explicar (cadena)', 'Sin explicar (SAREM)'], 1):
    c = wr.cell(r0 + 1, j, h); c.font = HF; c.fill = HFILL; c.alignment = Alignment(wrap_text=True)
for i, k in enumerate(C['controles']):
    rr = r0 + 2 + i
    for j, v in enumerate([fecha(k['de']), fecha(k['a']), k['pares_cadena'], k['pares_sarem'],
                           len(k['solo_cadena']), len(k['solo_sarem']),
                           len(k.get('solo_cadena_sin_explicar', k['solo_cadena'])),
                           len(k.get('solo_sarem_sin_explicar', k['solo_sarem']))], 1):
        c = wr.cell(rr, j, v); c.font = B
        if j >= 3: c.number_format = '#,##0'
rn = r0 + 3 + len(C['controles'])
wr.cell(rn, 1, 'Las diferencias "explicadas" vienen de las decisiones del paso a enero 2017 (ver Leeme): vínculos agregados o marcados '
               'en la cadena, y vínculos de SAREM que la OMA no registra (circuitos integrados 85.42 y 3004.60).').font = Font(name=A, size=9, italic=True)
for k2, dsc in enumerate(C.get('descartadas', [])):
    if 'hermanos' in dsc['motivo']:
        wr.cell(rn + 1 + k2, 1, f"No usada como control: {dsc['tabla']} ({fecha(dsc['de'])} → {fecha(dsc['a'])}): {dsc['motivo']}.").font = Font(name=A, size=9, italic=True)

# ---------- Léeme ----------
wl = wb.create_sheet('Leeme')
notas = [
    ('Qué es', None),
    ('1.', f'El mapeo de la NCM entre {fecha(INI).lower()} y {fecha(FIN).lower()}: para cada código, a qué código (o códigos) de la NCM de {fecha(FIN).lower()} corresponde.'),
    ('2.', 'Fuente: sistema SAREM del MERCOSUR (versiones de la NCM y tablas de correlación). Ver originales/LEEME.md del repositorio nomenclaturas.'),
    ('3.', 'Se encadenaron las tablas de SAREM entre versiones seguidas.'),
    ('Hojas', None),
    ('Resumen', 'Tipos de cambio en cada paso y controles contra SAREM.'),
    ('Mapeo', f'La hoja principal. Una fila por código, período de validez y código de destino en {fecha(FIN).lower()}.'),
    ('Cambios_por_paso', 'Solo los códigos que cambiaron en cada paso, con la marca "ex" de SAREM.'),
    ('Versiones', 'Las versiones de la NCM y su número interno en SAREM.'),
    ('Cómo leer el mapeo', None),
    ('Válido desde / hasta', 'Un mismo número de código puede llegar a destinos distintos según la fecha. Ejemplo: 0302.69.90 de 2002 se reparte en 15 códigos; el de 2003 en adelante no.'),
    ('Tipo de cambio', 'Igual: mismo código. Renumerado: cambia el número, 1 a 1. Se divide: un código viejo pasa a varios nuevos. Se fusiona: varios viejos van a uno nuevo. Complejo: las dos cosas a la vez.'),
    ('Marca "ex" de SAREM', 'En SAREM, "ex" aparece solo cuando el código nuevo recibe mercadería de más de un código viejo. Las divisiones NO llevan "ex". Comprobado en todas las tablas de versiones seguidas, sin excepciones.'),
    ('Para usarlo', 'Si un código "se divide" o es "complejo", la correspondencia es parcial: hay que mirar la descripción para saber a cuál de los destinos va cada producto. Las correlaciones no tienen valor legal.'),
    ('Controles', None),
    ('Tablas completas', 'En cada tabla de versiones seguidas, todos los códigos viejos existen en la versión vieja y todos los nuevos en la nueva. Cada código que desaparece tiene destino y cada código que aparece tiene origen.'),
    ('Contra SAREM', 'La cadena se compara con todas las tablas directas de SAREM entre versiones no seguidas cuyos códigos coinciden con sus versiones (ver Resumen).'),
    ('Decisiones y problemas de SAREM', None),
    ('Noviembre 2006 → enero 2007', 'La tabla de SAREM está incompleta: le faltan 9 vínculos (pelo fino en los capítulos 61 y 62, y 8517.62.59). Se usó la tabla directa de octubre 2006 a enero 2007, que tiene los mismos códigos de origen.'),
    ('Octubre 2011 → enero 2012', 'A la tabla de SAREM le faltan 19 vínculos hacia la partida nueva 96.19 (compresas, tampones y pañales de cualquier materia), desde los capítulos 39, 61, 62 y 63. Se agregaron desde la tabla enero 2011 → enero 2012, y coinciden con las tablas largas desde 2002 y 2007.'),
    ('Setiembre 2016 → enero 2017', 'VI Enmienda del SA. Se revisó contra la tabla de la OMA (SA 2012 → 2017). Cambios dentro de la misma subpartida de 6 dígitos: de SAREM. Cambios entre subpartidas que la OMA registra y faltaban: se agregaron (116 desde la tabla SAREM enero 2016 → enero 2017, sobre todo despojos de pescado hacia 0302.99 y 0303.99; 62 para toda la subpartida: 2939.99 → 2939.80 y 3808.92 → 3808.59). Vínculos de SAREM que la OMA no registra: se mantienen marcados (42: 29.33/29.34 → 2939.80, 29.22 → 2922.19, 03.05 → 0305.32). Los vínculos de las tablas largas hacia circuitos integrados (85.42) y 3004.60 no se usaron: la OMA no los registra.'),
    ('Enero 2002 ↔ julio 2018', 'Las tablas largas dicen 0101.21.01 (no existe) en lugar de 0101.21.00. Se corrigió al leerlas.'),
    ('Julio 2007 → enero 2016 y enero 2017', 'Las tablas largas desde julio 2007 unen entre sí códigos hermanos creados en julio 2007 (por ejemplo 8431.49.21 "Cabinas" con 8431.49.22 "Orugas"). No se usaron como control.'),
    ('Agosto 2016', 'Abre 14 códigos en 55 que setiembre 2016 vuelve a juntar: julio y setiembre 2016 tienen los mismos códigos.'),
    ('Enero 2003 ↔ enero 2004', 'Las tablas NCM_200213_NCM_200225 y la inversa dicen ser de enero 2004, pero sus códigos son los de enero 2005. No se usaron.'),
    ('Hacia y desde enero 2007', 'Las tablas de enero 2006 y julio 2006 hacia enero 2007 parten en realidad de octubre 2006, y las de enero 2007 hacia 2006 usan códigos de julio 2007; tienen filas "suprimido" y "eliminado". No se usaron.'),
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
wl.column_dimensions['A'].width = 30; wl.column_dimensions['B'].width = 110

wb._sheets = [wb[n] for n in ['Leeme', 'Resumen', 'Mapeo', 'Cambios_por_paso', 'Versiones']]
wb.active = 0
wb.save(out)
print('ok', NM - 1, 'filas de mapeo', NC - 1, 'filas de cambios')
