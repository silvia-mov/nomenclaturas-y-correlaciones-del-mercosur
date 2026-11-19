"""Encadena las correlaciones de SAREM entre versiones seguidas de la NCM (tramo 2002-2006).

Uso: python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena_2002_2006.json
"""
import json, sys, os, collections
import openpyxl

vers_path, carpeta, salida = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))

# versión de la NCM -> número interno de SAREM (comprobado en el paso 1)
# Se toma la primera tabla que aparezca con cada nombre. Las tablas entre enero 2003 y enero 2004
# (NCM_200213_NCM_200225 y la inversa) tienen códigos de enero 2005: no se usan.
ORDEN = [('NCM_2002_1', 'NCM_200201'), ('NCM_2002_7', 'NCM_200207'), ('NCM_2003_1', 'NCM_200213'),
         ('NCM_2003_7', 'NCM_200219'), ('NCM_2004_1', 'NCM_200225'), ('NCM_2004_7', 'NCM_200231'),
         ('NCM_2005_1', 'NCM_200237'), ('NCM_2005_4', 'NCM_200240'), ('NCM_2006_1', 'NCM_200249'),
         ('NCM_2006_7', 'NCM_200255'), ('NCM_2006_10', 'NCM_200258')]
SAREM = dict(ORDEN)
S = {v: set(V[v]['codigos']) for v, _ in ORDEN}


def buscar(ida, idb):
    for root, _, fs in os.walk(carpeta):
        for f in fs:
            if f == f'{ida}_{idb}.xlsx':
                return os.path.join(root, f)
    raise FileNotFoundError(f'{ida}_{idb}')


def leer_tabla(va, vb):
    """Relación código viejo -> códigos nuevos. Si la tabla solo trae cambios, el resto sigue igual."""
    ws = openpyxl.load_workbook(buscar(SAREM[va], SAREM[vb]), read_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    assert rows[2][0] == SAREM[va] and rows[2][2] == SAREM[vb]
    m = collections.defaultdict(set)
    ex = set()
    for r in rows[3:]:
        if r and r[0]:
            o, d = str(r[0]).strip(), str(r[2]).strip()
            m[o].add(d)
            if r[1] == 'ex':
                ex.add((o, d))
    for c in S[va]:
        if c not in m:
            assert c in S[vb], (va, vb, c)
            m[c] = {c}
    assert set(m) == S[va] and set().union(*m.values()) == S[vb]
    return dict(m), ex


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


def componer(r1, r2):
    return {o: set().union(*(r2[d] for d in ds)) for o, ds in r1.items()}


pasos = []
for (va, _), (vb, _) in zip(ORDEN, ORDEN[1:]):
    rel, ex = leer_tabla(va, vb)
    pasos.append({'de': va, 'a': vb, 'rel': rel, 'ex': ex, 'tipo': tipo(rel)})

# controles: composición de pasos contra las tablas directas de SAREM desde enero 2002
controles = []
acum = {c: {c} for c in S['NCM_2002_1']}
for i, p in enumerate(pasos):
    acum = componer(acum, p['rel'])
    if i == 0:
        continue  # la tabla directa es la misma del paso: no es un control
    try:
        directa, _ = leer_tabla('NCM_2002_1', p['a'])
    except FileNotFoundError:
        continue
    pares_c = {(o, d) for o, ds in acum.items() for d in ds}
    pares_d = {(o, d) for o, ds in directa.items() for d in ds}
    controles.append({'hasta': p['a'], 'pares_cadena': len(pares_c), 'pares_sarem': len(pares_d),
                      'solo_cadena': sorted(pares_c - pares_d), 'solo_sarem': sorted(pares_d - pares_c)})

# camino de cada (código, versión) hasta octubre 2006, agrupando versiones con el mismo resultado
FIN = ORDEN[-1][0]
filas = []
for i, (v, _) in enumerate(ORDEN):
    for c in sorted(S[v]):
        dest = {c}
        camino = []
        for p in pasos[i:]:
            nuevo = set().union(*(p['rel'][d] for d in dest))
            cambios = [(d, p['tipo'][d], sorted(p['rel'][d])) for d in sorted(dest) if p['tipo'][d] != 'igual']
            for d, t, ds in cambios:
                camino.append(f"{p['a'][4:].replace('_', '-')}: {d} {t} -> {', '.join(ds)}")
            dest = nuevo
        filas.append({'codigo': c, 'version': v, 'destino': sorted(dest), 'camino': camino})

# tipo de la relación compuesta, para cada versión de origen
compuesta_tipo = {}
for i, (v, _) in enumerate(ORDEN):
    rel = {f['codigo']: set(f['destino']) for f in filas if f['version'] == v}
    for c, t in tipo(rel).items():
        compuesta_tipo[(c, v)] = t
for f in filas:
    f['tipo'] = compuesta_tipo[(f['codigo'], f['version'])]

# agrupar versiones seguidas en que el código da el mismo resultado
agrup = []
por_codigo = collections.defaultdict(list)
for f in filas:
    por_codigo[f['codigo']].append(f)
idx = {v: i for i, (v, _) in enumerate(ORDEN)}
for c, fs in por_codigo.items():
    fs.sort(key=lambda f: idx[f['version']])
    grupo = None
    for f in fs:
        clave = (tuple(f['destino']), f['tipo'], tuple(f['camino']))
        if grupo and grupo['clave'] == clave and idx[f['version']] == idx[grupo['hasta']] + 1:
            grupo['hasta'] = f['version']
        else:
            grupo = {'codigo': c, 'desde': f['version'], 'hasta': f['version'], 'destino': f['destino'],
                     'tipo': f['tipo'], 'camino': f['camino'], 'clave': clave}
            agrup.append(grupo)
for g in agrup:
    g.pop('clave')

json.dump({'orden': ORDEN, 'controles': controles, 'agrupado': agrup,
           'pasos': [{'de': p['de'], 'a': p['a'],
                      'filas': [(o, d, (o, d) in p['ex'], p['tipo'][o]) for o in sorted(p['rel']) for d in sorted(p['rel'][o]) if p['tipo'][o] != 'igual']}
                     for p in pasos]},
          open(salida, 'w'), ensure_ascii=False)

for k in controles:
    print(f"Control hasta {k['hasta']}: cadena {k['pares_cadena']} pares, SAREM {k['pares_sarem']} | solo en la cadena {len(k['solo_cadena'])} {k['solo_cadena'][:5]} | solo en SAREM {len(k['solo_sarem'])} {k['solo_sarem'][:5]}")
print('filas agrupadas', len(agrup), collections.Counter(g['tipo'] for g in agrup))
