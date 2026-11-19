"""Encadena las correlaciones de SAREM entre versiones seguidas de la NCM.

Uso: python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena.json

La cadena va de la primera a la última versión de ORDEN. Cada paso usa la tabla de SAREM de una
versión a la siguiente. Como control, se compara la cadena con todas las tablas directas de SAREM
(versión A -> versión B, no seguidas) cuyos códigos coinciden con los de sus dos versiones.
"""
import json, sys, os, re, collections
import openpyxl

vers_path, carpeta, salida = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))

# versión de la NCM -> número interno de SAREM (comprobado código por código).
# Tramo 1: enero 2002 - octubre 2006. Tramo 2: noviembre 2006 - enero 2010.
ORDEN = [('NCM_2002_1', 'NCM_200201'), ('NCM_2002_7', 'NCM_200207'), ('NCM_2003_1', 'NCM_200213'),
         ('NCM_2003_7', 'NCM_200219'), ('NCM_2004_1', 'NCM_200225'), ('NCM_2004_7', 'NCM_200231'),
         ('NCM_2005_1', 'NCM_200237'), ('NCM_2005_4', 'NCM_200240'), ('NCM_2006_1', 'NCM_200249'),
         ('NCM_2006_7', 'NCM_200255'), ('NCM_2006_10', 'NCM_200258'),
         ('NCM_2006_11', 'NCM_200259'), ('NCM_2007_1', 'NCM_200701'), ('NCM_2007_7', 'NCM_200707'),
         ('NCM_2008_1', 'NCM_200713'), ('NCM_2008_7', 'NCM_200719'), ('NCM_2009_1', 'NCM_200725'),
         ('NCM_2009_4', 'NCM_200728'), ('NCM_2009_10', 'NCM_200734'), ('NCM_2010_1', 'NCM_200737')]
SAREM = dict(ORDEN)
VERSION = {s: v for v, s in ORDEN}
IDX = {v: i for i, (v, _) in enumerate(ORDEN)}
S = {v: set(V[v]['codigos']) for v, _ in ORDEN}
FIN = ORDEN[-1][0]

TABLAS = {}
for root, _, fs in os.walk(carpeta):
    for f in fs:
        m = re.fullmatch(r'(NCM_\d+)_(NCM_\d+)\.xlsx', f)
        if m and m.group(1) in VERSION and m.group(2) in VERSION:  # la primera tabla con ese nombre
            TABLAS.setdefault((m.group(1), m.group(2)), os.path.join(root, f))


def leer(path):
    rows = list(openpyxl.load_workbook(path, read_only=True).active.iter_rows(values_only=True))
    pares, ex = [], set()
    for r in rows[3:]:
        if r and r[0]:
            o, d = str(r[0]).strip(), str(r[2]).strip()
            pares.append((o, d))
            if r[1] == 'ex':
                ex.add((o, d))
    return rows[2][0], rows[2][2], pares, ex


def relacion(va, vb, pares):
    """Relación código viejo -> códigos nuevos. Si la tabla solo trae cambios, el resto sigue igual."""
    m = collections.defaultdict(set)
    for o, d in pares:
        m[o].add(d)
    for c in S[va]:
        if c not in m:
            m[c] = {c}
    return dict(m)


def tipo(rel):
    """Clasifica cada código de origen: igual, renumerado, se divide, se fusiona, complejo."""
    inv = collections.defaultdict(set)
    for o, ds in rel.items():
        for d in ds:
            inv[d].add(o)
    out = {}
    for o, ds in rel.items():
        varios_dest = len(ds) > 1
        dest_compartido = any(len(inv[d]) > 1 for d in ds)
        if not varios_dest and not dest_compartido:
            out[o] = 'igual' if ds == {o} else 'renumerado'
        elif varios_dest and not dest_compartido:
            out[o] = 'se divide'
        elif not varios_dest:
            out[o] = 'se fusiona'
        else:
            out[o] = 'complejo'
    return out


# Tablas que reemplazan a la de versiones seguidas. Noviembre 2006 -> enero 2007 está incompleta en
# SAREM: le faltan 9 vínculos (pelo fino en los caps. 61 y 62, y 8517.62.59) que sí están en la tabla
# directa octubre 2006 -> enero 2007 y en las tablas desde enero 2002. Octubre y noviembre 2006 tienen
# los mismos códigos, así que se usa la tabla de octubre.
REEMPLAZO = {('NCM_2006_11', 'NCM_2007_1'): ('NCM_200258', 'NCM_200701')}

# ---------- pasos entre versiones seguidas ----------
pasos = []
for (va, sa), (vb, sb) in zip(ORDEN, ORDEN[1:]):
    ta, tb = REEMPLAZO.get((va, vb), (sa, sb))
    if (ta, tb) != (sa, sb):
        assert S[VERSION[ta]] == S[va]
    a, b, pares, ex = leer(TABLAS[(ta, tb)])
    assert (a, b) == (ta, tb)
    rel = relacion(va, vb, pares)
    assert set(rel) == S[va] and set().union(*rel.values()) == S[vb], (va, vb)
    pasos.append({'de': va, 'a': vb, 'rel': rel, 'ex': ex, 'tipo': tipo(rel)})


def cadena(desde, hasta):
    acum = {c: {c} for c in S[desde]}
    for p in pasos[IDX[desde]:IDX[hasta]]:
        acum = {o: set().union(*(p['rel'][d] for d in ds)) for o, ds in acum.items()}
    return acum


# ---------- controles contra las tablas directas de SAREM ----------
controles, descartadas = [], []
for (sa, sb), path in sorted(TABLAS.items()):
    va, vb = VERSION[sa], VERSION[sb]
    if IDX[vb] <= IDX[va] + 1 or (sa, sb) in REEMPLAZO.values():
        continue  # hacia atrás, o la misma tabla usada en un paso
    _, _, pares, _ = leer(path)
    origen = {o for o, _ in pares}
    destino = {d for _, d in pares}
    completa = origen == S[va]
    if not completa or not destino <= S[vb]:
        descartadas.append({'tabla': f'{sa}_{sb}', 'de': va, 'a': vb, 'motivo':
                            'solo trae cambios' if len(origen) < len(S[va]) and origen <= S[va] and destino <= S[vb]
                            else 'sus códigos no coinciden con las versiones'})
        continue
    directa = {(o, d) for o, d in pares}
    calc = {(o, d) for o, ds in cadena(va, vb).items() for d in ds}
    controles.append({'de': va, 'a': vb, 'tabla': f'{sa}_{sb}', 'pares_cadena': len(calc), 'pares_sarem': len(directa),
                      'solo_cadena': sorted(calc - directa), 'solo_sarem': sorted(directa - calc)})

# ---------- camino de cada (código, versión) hasta la última versión ----------
filas = []
for i, (v, _) in enumerate(ORDEN):
    for c in sorted(S[v]):
        dest, camino = {c}, []
        for p in pasos[i:]:
            for d in sorted(dest):
                if p['tipo'][d] != 'igual':
                    camino.append(f"{p['a'][4:].replace('_', '-')}: {d} {p['tipo'][d]} -> {', '.join(sorted(p['rel'][d]))}")
            dest = set().union(*(p['rel'][d] for d in dest))
        filas.append({'codigo': c, 'version': v, 'destino': sorted(dest), 'camino': camino})

compuesta = {}
for v, _ in ORDEN:
    rel = {f['codigo']: set(f['destino']) for f in filas if f['version'] == v}
    for c, t in tipo(rel).items():
        compuesta[(c, v)] = t
for f in filas:
    f['tipo'] = compuesta[(f['codigo'], f['version'])]

# agrupar versiones seguidas en que el código llega a lo mismo
agrup = []
por_codigo = collections.defaultdict(list)
for f in filas:
    por_codigo[f['codigo']].append(f)
for c, fs in por_codigo.items():
    fs.sort(key=lambda f: IDX[f['version']])
    g = None
    for f in fs:
        clave = (tuple(f['destino']), f['tipo'], tuple(f['camino']))
        if g and g['clave'] == clave and IDX[f['version']] == IDX[g['hasta']] + 1:
            g['hasta'] = f['version']
        else:
            g = {'codigo': c, 'desde': f['version'], 'hasta': f['version'], 'destino': f['destino'],
                 'tipo': f['tipo'], 'camino': f['camino'], 'clave': clave}
            agrup.append(g)
for g in agrup:
    g.pop('clave')

json.dump({'orden': ORDEN, 'fin': FIN, 'controles': controles, 'descartadas': descartadas, 'agrupado': agrup,
           'pasos': [{'de': p['de'], 'a': p['a'],
                      'filas': [(o, d, (o, d) in p['ex'], p['tipo'][o]) for o in sorted(p['rel'])
                                for d in sorted(p['rel'][o]) if p['tipo'][o] != 'igual']}
                     for p in pasos]},
          open(salida, 'w'), ensure_ascii=False)

for k in controles:
    print(f"Control {k['de']} -> {k['a']}: cadena {k['pares_cadena']}, SAREM {k['pares_sarem']} | "
          f"solo cadena {len(k['solo_cadena'])} {k['solo_cadena'][:3]} | solo SAREM {len(k['solo_sarem'])} {k['solo_sarem'][:3]}")
for k in descartadas:
    print(f"No usada como control: {k['tabla']} ({k['de']} -> {k['a']}): {k['motivo']}")
print('filas agrupadas', len(agrup), collections.Counter(g['tipo'] for g in agrup))
