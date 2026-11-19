"""Encadena las correlaciones de SAREM entre versiones seguidas de la NCM.

Uso: python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena.json datos/oma_2012_2017.json

La cadena va de la primera a la última versión de ORDEN. Cada paso usa la tabla de SAREM de una
versión a la siguiente. Como control, se compara la cadena con todas las tablas directas de SAREM
(versión A -> versión B, no seguidas) cuyos códigos coinciden con los de sus dos versiones.
"""
import json, sys, os, re, collections
import openpyxl

vers_path, carpeta, salida, oma_path = sys.argv[1:5]
V = json.load(open(vers_path, encoding='utf-8'))
OMA = json.load(open(oma_path, encoding='utf-8'))

# versión de la NCM -> número interno de SAREM (comprobado código por código).
# Tramo 1: enero 2002 - octubre 2006. Tramo 2: noviembre 2006 - enero 2010. Tramo 3: octubre 2010 - enero 2015.
# Tramo 4: julio 2015 - enero 2019 (agosto 2016 abre 14 códigos que setiembre 2016 vuelve a juntar).
ORDEN = [('NCM_2002_1', 'NCM_200201'), ('NCM_2002_7', 'NCM_200207'), ('NCM_2003_1', 'NCM_200213'),
         ('NCM_2003_7', 'NCM_200219'), ('NCM_2004_1', 'NCM_200225'), ('NCM_2004_7', 'NCM_200231'),
         ('NCM_2005_1', 'NCM_200237'), ('NCM_2005_4', 'NCM_200240'), ('NCM_2006_1', 'NCM_200249'),
         ('NCM_2006_7', 'NCM_200255'), ('NCM_2006_10', 'NCM_200258'),
         ('NCM_2006_11', 'NCM_200259'), ('NCM_2007_1', 'NCM_200701'), ('NCM_2007_7', 'NCM_200707'),
         ('NCM_2008_1', 'NCM_200713'), ('NCM_2008_7', 'NCM_200719'), ('NCM_2009_1', 'NCM_200725'),
         ('NCM_2009_4', 'NCM_200728'), ('NCM_2009_10', 'NCM_200734'), ('NCM_2010_1', 'NCM_200737'),
         ('NCM_2010_10', 'NCM_200746'), ('NCM_2011_1', 'NCM_200749'), ('NCM_2011_4', 'NCM_200752'),
         ('NCM_2011_10', 'NCM_200758'), ('NCM_2012_1', 'NCM_201201'), ('NCM_2012_4', 'NCM_201204'),
         ('NCM_2012_7', 'NCM_201207'), ('NCM_2013_1', 'NCM_201213'), ('NCM_2014_1', 'NCM_201225'),
         ('NCM_2015_1', 'NCM_201237'), ('NCM_2015_7', 'NCM_201243'), ('NCM_2016_1', 'NCM_201249'),
         ('NCM_2016_7', 'NCM_201255'), ('NCM_2016_8', 'NCM_201256'), ('NCM_2016_9', 'NCM_201257'),
         ('NCM_2017_1', 'NCM_201701'), ('NCM_2017_7', 'NCM_201707'), ('NCM_2018_1', 'NCM_201713'),
         ('NCM_2018_7', 'NCM_201719'), ('NCM_2019_1', 'NCM_201725')]
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


# Errores de tipeo en tablas de SAREM: las tablas largas entre enero 2002 y julio 2018 dicen
# 01012101 (no existe en ninguna versión) en lugar de 01012100 (caballos reproductores de raza pura).
CORREGIR = {'NCM_200201_NCM_201719.xlsx': {'01012101': '01012100'},
            'NCM_201719_NCM_200201.xlsx': {'01012101': '01012100'}}


def leer(path):
    rows = list(openpyxl.load_workbook(path, read_only=True).active.iter_rows(values_only=True))
    fix = CORREGIR.get(os.path.basename(path), {})
    pares, ex = [], set()
    for r in rows[3:]:
        if r and r[0]:
            o, d = str(r[0]).strip(), str(r[2]).strip()
            o, d = fix.get(o, o), fix.get(d, d)
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

# Vínculos que faltan en una tabla de versiones seguidas y se agregan desde otra tabla de SAREM.
# Octubre 2011 -> enero 2012 (V Enmienda del SA): la partida nueva 96.19 (compresas, tampones y
# pañales de cualquier materia) solo recibe de 48.18 y 56.01; faltan 19 códigos de los caps. 39, 61,
# 62 y 63 que sí van "ex 9619.00.00" en la tabla enero 2011 -> enero 2012 y en las tablas largas
# desde enero 2002 y enero 2007. Se agregan desde NCM_200749_NCM_201201.
AGREGAR = {('NCM_2011_10', 'NCM_2012_1'): {'tabla': ('NCM_200749', 'NCM_201201'), 'destino': '96190000'}}

# Pasos que se revisan contra la tabla de correlación de la OMA (6 dígitos). Septiembre 2016 -> enero
# 2017 (VI Enmienda del SA): la tabla corta de SAREM no tiene 70 cambios que la OMA registra (sobre
# todo despojos de pescado hacia 0302.99 y 0303.99) y tiene 42 vínculos entre subpartidas que la OMA
# no registra (29.33/29.34 -> 2939.80, 29.22 -> 2922.19, 03.05 -> 0305.32). Regla:
#  - cambios dentro de la misma subpartida de 6 dígitos: tal cual vienen de SAREM;
#  - cambios de la OMA que faltan: se agregan con los códigos de 8 dígitos de la tabla larga de SAREM
#    indicada; si no hay ninguno, con todos los códigos de 8 dígitos de las dos subpartidas;
#  - vínculos de SAREM que la OMA no registra: se mantienen, marcados.
VERIFICAR_OMA = {('NCM_2016_9', 'NCM_2017_1'): {'larga': ('NCM_201249', 'NCM_201701')}}
W_OMA = collections.defaultdict(set)
for a6, b6, _ in OMA['tabla'] + OMA['anexo44']:
    W_OMA[a6].add(b6)

# Tablas que no sirven como control.
_HERMANOS = 'une códigos hermanos creados en julio 2007 (por ejemplo 8431.49.21 "Cabinas" -> 8431.49.22 "Orugas")'
NO_CONTROL = {('NCM_200707', 'NCM_201249'): _HERMANOS, ('NCM_200707', 'NCM_201701'): _HERMANOS}

# ---------- pasos entre versiones seguidas ----------
pasos = []
for (va, sa), (vb, sb) in zip(ORDEN, ORDEN[1:]):
    ta, tb = REEMPLAZO.get((va, vb), (sa, sb))
    if (ta, tb) != (sa, sb):
        assert S[VERSION[ta]] == S[va]
    a, b, pares, ex = leer(TABLAS[(ta, tb)])
    assert (a, b) == (ta, tb)
    agregados, notas = [], {}
    if (va, vb) in AGREGAR:
        cfg = AGREGAR[(va, vb)]
        _, _, otros, _ = leer(TABLAS[cfg['tabla']])
        ya = set(pares)
        agregados = sorted({(o, d) for o, d in otros if d == cfg['destino'] and o in S[va] and (o, d) not in ya})
        base = {o for o, _ in pares}
        agregados += [(o, o) for o, _ in agregados if o not in base and o in S[vb]]
        pares = pares + agregados
        ex = ex | set(agregados)
        for par in agregados:
            notas[par] = f'agregado desde la tabla SAREM {cfg["tabla"][0]}_{cfg["tabla"][1]}'
        print(f'{va} -> {vb}: se agregan {len(agregados)} vínculos a {cfg["destino"]} desde {cfg["tabla"][0]}_{cfg["tabla"][1]}')
    if (va, vb) in VERIFICAR_OMA:
        cfg = VERIFICAR_OMA[(va, vb)]
        r6 = collections.defaultdict(set)
        for o, d in pares:
            r6[o[:6]].add(d[:6])
        for o, d in pares:
            if o[:6] != d[:6] and d[:6] not in W_OMA.get(o[:6], {o[:6]}):
                notas[(o, d)] = 'sin respaldo de la OMA (se mantiene)'
        _, _, larga, _ = leer(TABLAS[cfg['larga']])
        ya = set(pares)
        nota_l = f'agregado: lo registra la OMA (8 dígitos de la tabla SAREM {cfg["larga"][0]}_{cfg["larga"][1]})'
        nota_s = 'agregado: lo registra la OMA (todos los códigos de las dos subpartidas)'
        # 1) vínculos de la tabla larga que la OMA confirma a 6 dígitos y faltan en la tabla corta
        nuevos = sorted({(o, d) for o, d in larga if o in S[va] and d in S[vb] and o[:6] != d[:6]
                         and d[:6] in W_OMA.get(o[:6], set()) and (o, d) not in ya})
        for par in nuevos:
            notas[par] = nota_l
            r6[par[0][:6]].add(par[1][:6])
        # 2) cambios de la OMA (6 dígitos) que siguen sin ningún vínculo: toda la subpartida
        for a6 in sorted({c[:6] for c in S[va]}):
            for b6 in sorted(W_OMA.get(a6, set())):
                if b6 != a6 and b6 not in r6.get(a6, set()):
                    cand = [(o, d) for o in sorted(S[va]) if o[:6] == a6 for d in sorted(S[vb]) if d[:6] == b6]
                    for par in cand:
                        notas[par] = nota_s
                    nuevos += cand
        # un código que en la tabla corta seguía igual conserva su destino propio
        base = {o for o, _ in pares}
        nuevos += [(o, o) for o, _ in nuevos if o not in base and o in S[vb]]
        nuevos = sorted(set(nuevos) - set(pares))
        pares = pares + nuevos
        ex = ex | set(nuevos)
        agregados += nuevos
        print(f'{va} -> {vb}: OMA: se agregan {len(nuevos)} vínculos y se marcan '
              f'{sum(1 for n in notas.values() if n.startswith("sin respaldo"))} sin respaldo')
    rel = relacion(va, vb, pares)
    assert set(rel) == S[va] and set().union(*rel.values()) == S[vb], (va, vb)
    pasos.append({'de': va, 'a': vb, 'rel': rel, 'ex': ex, 'tipo': tipo(rel), 'agregados': agregados, 'notas': notas})


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
    if (sa, sb) in NO_CONTROL:
        descartadas.append({'tabla': f'{sa}_{sb}', 'de': va, 'a': vb, 'motivo': NO_CONTROL[(sa, sb)]})
        continue
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

# Diferencias de los controles que se explican por las decisiones de VERIFICAR_OMA: vínculos de la
# cadena que llegan a un destino agregado o marcado, y vínculos de SAREM hacia un destino al que la
# OMA no manda nada desde esa subpartida.
destinos_nota = {d for p in pasos for (_, d) in p['notas']}
for k in controles:
    cruza = any(IDX[k['de']] <= IDX[va] and IDX[vb] <= IDX[k['a']] for va, vb in VERIFICAR_OMA)
    def sin_oma(o, d):
        return o[:6] != d[:6] and d[:6] not in W_OMA.get(o[:6], {o[:6]})
    def con_oma(o, d):
        return o[:6] != d[:6] and d[:6] in W_OMA.get(o[:6], set())
    # en la cadena: destino agregado o marcado, o un cambio que la OMA registra y le falta a la tabla larga
    k['solo_cadena_sin_explicar'] = [par for par in k['solo_cadena'] if not (cruza and (par[1] in destinos_nota or con_oma(*par)))]
    k['solo_sarem_sin_explicar'] = [par for par in k['solo_sarem'] if not (cruza and sin_oma(*par))]

# ---------- camino de cada (código, versión) hasta la última versión ----------
filas = []
for i, (v, _) in enumerate(ORDEN):
    for c in sorted(S[v]):
        dest, camino, nts = {c}, [], []
        for p in pasos[i:]:
            for d in sorted(dest):
                if p['tipo'][d] != 'igual':
                    camino.append(f"{p['a'][4:].replace('_', '-')}: {d} {p['tipo'][d]} -> {', '.join(sorted(p['rel'][d]))}")
                for x in sorted(p['rel'][d]):
                    if (d, x) in p['notas']:
                        nts.append(f"{p['a'][4:].replace('_', '-')}: {d} -> {x}: {p['notas'][(d, x)]}")
            dest = set().union(*(p['rel'][d] for d in dest))
        filas.append({'codigo': c, 'version': v, 'destino': sorted(dest), 'camino': camino, 'notas': nts})

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
        clave = (tuple(f['destino']), f['tipo'], tuple(f['camino']), tuple(f['notas']))
        if g and g['clave'] == clave and IDX[f['version']] == IDX[g['hasta']] + 1:
            g['hasta'] = f['version']
        else:
            g = {'codigo': c, 'desde': f['version'], 'hasta': f['version'], 'destino': f['destino'],
                 'tipo': f['tipo'], 'camino': f['camino'], 'notas': f['notas'], 'clave': clave}
            agrup.append(g)
for g in agrup:
    g.pop('clave')

json.dump({'orden': ORDEN, 'fin': FIN, 'controles': controles, 'descartadas': descartadas, 'agrupado': agrup,
           'pasos': [{'de': p['de'], 'a': p['a'],
                      'filas': [(o, d, (o, d) in p['ex'], p['tipo'][o], p['notas'].get((o, d), '')) for o in sorted(p['rel'])
                                for d in sorted(p['rel'][o]) if p['tipo'][o] != 'igual'],
                      'agregados': p['agregados']}
                     for p in pasos]},
          open(salida, 'w'), ensure_ascii=False)

for k in controles:
    print(f"Control {k['de']} -> {k['a']}: cadena {k['pares_cadena']}, SAREM {k['pares_sarem']} | "
          f"solo cadena {len(k['solo_cadena'])} (sin explicar {len(k['solo_cadena_sin_explicar'])} {k['solo_cadena_sin_explicar'][:3]}) | "
          f"solo SAREM {len(k['solo_sarem'])} (sin explicar {len(k['solo_sarem_sin_explicar'])} {k['solo_sarem_sin_explicar'][:3]})")
for k in descartadas:
    print(f"No usada como control: {k['tabla']} ({k['de']} -> {k['a']}): {k['motivo']}")
print('filas agrupadas', len(agrup), collections.Counter(g['tipo'] for g in agrup))
