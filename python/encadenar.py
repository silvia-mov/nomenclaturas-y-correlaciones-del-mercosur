"""Encadena las correlaciones de SAREM entre versiones seguidas de la NCM.

Uso: python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena.json datos

La cadena va de la primera a la última versión de ORDEN. Cada paso usa la tabla de SAREM de una
versión a la siguiente. Como control, se compara la cadena con todas las tablas directas de SAREM
(versión A -> versión B, no seguidas) cuyos códigos coinciden con los de sus dos versiones.
"""
import json, sys, os, re, collections
import openpyxl

vers_path, carpeta, salida, oma_dir = sys.argv[1:5]
V = json.load(open(vers_path, encoding='utf-8'))
# tablas de la OMA leídas por leer_oma.py: datos/oma_2012_2017.json y datos/oma_2017_2022.json
# El origen de la OMA puede ser una subpartida (6 dígitos), una partida (4) o un capítulo (2).
W_ED = {}
for ed in ('2002_2007', '2007_2012', '2012_2017', '2017_2022'):
    oma = json.load(open(os.path.join(oma_dir, f'oma_{ed}.json'), encoding='utf-8'))
    W_ED[ed] = collections.defaultdict(set)
    for a, b6, _ in oma['tabla'] + oma['anexo44']:
        W_ED[ed][a].add(b6)


def oma_dest(ed, o6):
    """Destinos que la OMA admite para la subpartida o6 (incluye seguir en o6 si no cambia). Cada destino es
    una subpartida (6 dígitos) o, cuando la OMA escribe "subpartidas aplicables de...", una partida o capítulo."""
    W = W_ED[ed]
    base = set(W[o6]) if o6 in W else {o6}
    return base | W.get(o6[:4], set()) | W.get(o6[:2], set())


def soporta(ed, o, d):
    """¿La OMA admite pasar del código o al código d (8 dígitos)?"""
    return any(d.startswith(x) for x in oma_dest(ed, o[:6]))

# versión de la NCM -> número interno de SAREM (comprobado código por código).
# Tramo 1: enero 2002 - octubre 2006. Tramo 2: noviembre 2006 - enero 2010. Tramo 3: octubre 2010 - enero 2015.
# Tramo 4: julio 2015 - enero 2019 (agosto 2016 abre 14 códigos que setiembre 2016 vuelve a juntar).
# Tramo 5: marzo 2019 - enero 2022. Marzo 2019 no tiene versión descargada: sus códigos se arman con la
# tabla de SAREM desde enero 2019 (ver DERIVADAS). "NCM_2022" es la carpeta "49. 2022" (mismos códigos
# que setiembre 2021).
# Tramo 6: julio 2022 - noviembre 2026. La carpeta "62. FEBRERO 2023" es febrero 2026 (NCM_202250).
# Noviembre 2026 no tiene tabla de correlación: tiene los mismos códigos que octubre 2026 (ver SIN_TABLA).
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
         ('NCM_2018_7', 'NCM_201719'), ('NCM_2019_1', 'NCM_201725'),
         ('NCM_2019_3', 'NCM_201727'), ('NCM_2019_7', 'NCM_201731'), ('NCM_2020_1', 'NCM_201737'),
         ('NCM_2020_7', 'NCM_201743'), ('NCM_2021_1', 'NCM_201749'), ('NCM_2021_4', 'NCM_201752'),
         ('NCM_2021_7', 'NCM_201755'), ('NCM_2021_9', 'NCM_201757'), ('NCM_2022', 'NCM_201760'),
         ('NCM_2022_1', 'NCM_202201'), ('NCM_2022_7', 'NCM_202207'), ('NCM_2022_9', 'NCM_202209'),
         ('NCM_2023_1', 'NCM_202213'), ('NCM_2023_4', 'NCM_202216'), ('NCM_2023_7', 'NCM_202219'),
         ('NCM_2023_11', 'NCM_202223'), ('NCM_2024_4', 'NCM_202228'), ('NCM_2024_7', 'NCM_202231'),
         ('NCM_2025_1', 'NCM_202237'), ('NCM_2025_10', 'NCM_202246'), ('NCM_2026_1', 'NCM_202249'),
         ('NCM_2026_2', 'NCM_202250'), ('NCM_2026_10', 'NCM_202258'), ('NCM_2026_11', 'SIN_TABLA_202611')]
SAREM = dict(ORDEN)
VERSION = {s: v for v, s in ORDEN}
IDX = {v: i for i, (v, _) in enumerate(ORDEN)}
S = {v: set(V[v]['codigos']) for v, _ in ORDEN if v in V}
# versiones sin archivo de SAREM: se arman desde la versión anterior con la tabla de correlación
DERIVADAS = {'NCM_2019_3': {'desde': 'NCM_2019_1', 'anio': 2019, 'mes': 3}}
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


VERSIONES_EXTRA = {}
for v, cfg in DERIVADAS.items():
    _, _, pares0, _ = leer(TABLAS[(SAREM[cfg['desde']], SAREM[v])])
    m0 = collections.defaultdict(set)
    for o, d in pares0:
        m0[o].add(d)
    S[v] = set().union(*(m0.get(c, {c}) for c in S[cfg['desde']]))
    VERSIONES_EXTRA[v] = {'anio': cfg['anio'], 'mes': cfg['mes'], 'codigos': {c: V[cfg['desde']]['codigos'].get(c, ['']) for c in S[v]},
                          'titulo': f'Sin archivo en SAREM: armada desde {cfg["desde"]} con la tabla de correlación'}


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
#  - vínculos de SAREM que la OMA no registra: se mantienen, marcados (modo 'marcar').
# "NCM_2022" -> enero 2022 (VII Enmienda del SA): de 24.028 vínculos entre subpartidas, 23.066 no los
# registra la OMA (sobre todo 85.49 residuos electrónicos y 85.24 módulos de pantallas, desde miles de
# códigos de máquinas y aparatos). Dejarlos daría destinos falsos a 1 de cada 4 códigos, así que en
# este paso NO se usan (modo 'descartar'): van a la lista de vínculos de SAREM no usados, con su motivo.
# Si un código se quedara sin destino, o un destino sin origen, sus vínculos se mantienen marcados.
# Noviembre 2006 -> enero 2007 (IV Enmienda) y octubre 2011 -> enero 2012 (V Enmienda): misma regla que
# 2017 (modo 'marcar'). En 2007 SAREM no tiene, por ejemplo, ningún vínculo hacia 84.86 (máquinas para
# fabricar semiconductores) desde las máquinas herramienta que indica la OMA.
VERIFICAR_OMA = {('NCM_2006_11', 'NCM_2007_1'): {'larga': ('NCM_200201', 'NCM_200701'), 'edicion': '2002_2007', 'modo': 'marcar'},
                 ('NCM_2011_10', 'NCM_2012_1'): {'larga': ('NCM_200749', 'NCM_201201'), 'edicion': '2007_2012', 'modo': 'marcar'},
                 ('NCM_2016_9', 'NCM_2017_1'): {'larga': ('NCM_201249', 'NCM_201701'), 'edicion': '2012_2017', 'modo': 'marcar'},
                 ('NCM_2022', 'NCM_2022_1'): {'larga': ('NCM_201757', 'NCM_202201'), 'edicion': '2017_2022', 'modo': 'descartar'}}

# Tablas que no sirven como control.
_HERMANOS = 'une códigos hermanos creados en julio 2007 (por ejemplo 8431.49.21 "Cabinas" -> 8431.49.22 "Orugas")'
NO_CONTROL = {('NCM_200707', 'NCM_201249'): _HERMANOS, ('NCM_200707', 'NCM_201701'): _HERMANOS}

# Pasos que solo se cruzan con la OMA, sin cambiar la cadena (para revisar antes de decidir).
INFORME_OMA = {}

# Pasos sin tabla de SAREM entre dos versiones con exactamente los mismos códigos: nada cambia.
SIN_TABLA = {('NCM_2026_10', 'NCM_2026_11')}

# ---------- pasos entre versiones seguidas ----------
pasos, descartes, informes = [], [], []
for (va, sa), (vb, sb) in zip(ORDEN, ORDEN[1:]):
    ta, tb = REEMPLAZO.get((va, vb), (sa, sb))
    if (ta, tb) != (sa, sb):
        assert S[VERSION[ta]] == S[va]
    if (va, vb) in SIN_TABLA:
        assert S[va] == S[vb], (va, vb)
        pares, ex = [], set()
    else:
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
        ed = cfg['edicion']; W_OMA = W_ED[ed]
        sin = [(o, d) for o, d in pares if o[:6] != d[:6] and not soporta(ed, o, d)]
        if cfg['modo'] == 'descartar':
            quedan = [par for par in pares if par not in set(sin)]
            orig_ok = {o for o, _ in quedan}; dest_ok = {d for _, d in quedan}
            # se mantienen (marcados) los vínculos sin respaldo que dejarían un código sin destino o un destino sin origen
            necesarios = {(o, d) for o, d in sin if (o not in orig_ok and o not in S[vb]) or (d not in dest_ok and d not in S[va])}
            for o, d in sin:
                if (o, d) in necesarios:
                    notas[(o, d)] = 'sin respaldo de la OMA (se mantiene: si no, el código queda sin destino o el destino sin origen)'
                else:
                    descartes.append({'de': va, 'a': vb, 'origen': o, 'destino': d, 'ex': (o, d) in ex,
                                      'motivo': f'la OMA (SA {cfg["edicion"].replace("_", " -> ")}) no registra {o[:4]}.{o[4:6]} -> {d[:4]}.{d[4:6]}'})
            pares = [par for par in pares if par not in set(sin) or par in necesarios]
        else:
            for o, d in sin:
                notas[(o, d)] = 'sin respaldo de la OMA (se mantiene)'
        r6 = collections.defaultdict(set)
        for o, d in pares:
            r6[o[:6]].add(d[:6])
        _, _, larga, _ = leer(TABLAS[cfg['larga']])
        ya = set(pares)
        nota_l = f'agregado: lo registra la OMA (8 dígitos de la tabla SAREM {cfg["larga"][0]}_{cfg["larga"][1]})'
        nota_s = 'agregado: lo registra la OMA (todos los códigos de las dos subpartidas)'
        # 1) vínculos de la tabla larga que la OMA confirma a 6 dígitos y faltan en la tabla corta
        nuevos = sorted({(o, d) for o, d in larga if o in S[va] and d in S[vb] and o[:6] != d[:6]
                         and soporta(ed, o, d) and (o, d) not in ya})
        for par in nuevos:
            notas[par] = nota_l
            r6[par[0][:6]].add(par[1][:6])
        # 2) cambios de la OMA dados por subpartida (6 dígitos) que siguen sin ningún vínculo: toda la
        #    subpartida. Los dados por partida o capítulo ("subpartidas aplicables...") no se completan así.
        for a6 in sorted({c[:6] for c in S[va]}):
            for b6 in sorted(x for x in (W_OMA.get(a6, set()) if a6 in W_OMA else set()) if len(x) == 6):
                if b6 != a6 and b6 not in r6.get(a6, set()):
                    cand = [(o, d) for o in sorted(S[va]) if o[:6] == a6 for d in sorted(S[vb]) if d[:6] == b6]
                    for par in cand:
                        notas[par] = nota_s
                    nuevos += cand
        # un código que en la tabla corta seguía igual conserva su destino propio
        base = {o for o, _ in pares}
        nuevos += [(o, o) for o, _ in nuevos if o not in base and o in S[vb]]
        if cfg['modo'] == 'descartar':
            # un código que quedó sin vínculos al descartar y existe en la versión nueva sigue igual
            base = {o for o, _ in pares} | {o for o, _ in nuevos}
            con_descarte = {x['origen'] for x in descartes if x['de'] == va}
            nuevos += [(o, o) for o in S[va] if o not in base and o in S[vb] and o in con_descarte]
        nuevos = sorted(set(nuevos) - set(pares))
        pares = pares + nuevos
        ex = ex | set(nuevos)
        agregados += nuevos
        print(f'{va} -> {vb}: OMA ({cfg["modo"]}): se agregan {len(nuevos)} vínculos, se marcan '
              f'{sum(1 for n in notas.values() if n.startswith("sin respaldo"))} sin respaldo y se descartan '
              f'{sum(1 for x in descartes if x["de"] == va)}')
    if (va, vb) in INFORME_OMA:
        ed = INFORME_OMA[(va, vb)]
        entre = [(o, d) for o, d in pares if o[:6] != d[:6]]
        sin = [(o, d) for o, d in entre if not soporta(ed, o, d)]
        r6 = collections.defaultdict(set)
        for o, d in pares:
            r6[o[:6]].add(d[:6])
        faltan = [(a6, b6) for a6 in sorted({c[:6] for c in S[va]}) for b6 in sorted(W_ED[ed].get(a6, set()))
                  if len(b6) == 6 and b6 != a6 and b6 not in r6.get(a6, set())]
        informes.append({'de': va, 'a': vb, 'edicion': ed, 'pares': len(pares), 'entre_subpartidas': len(entre),
                         'sin_respaldo': sin, 'faltan_6': faltan})
        print(f'{va} -> {vb}: cruce con OMA {ed}: {len(entre)} vínculos entre subpartidas, {len(sin)} sin respaldo, '
              f'{len(faltan)} cambios de la OMA (6 díg) sin ningún vínculo en SAREM')
    rel = relacion(va, vb, pares)
    assert set(rel) == S[va] and set().union(*rel.values()) == S[vb], (va, vb)
    # relación solo con SAREM (sin los vínculos agregados), para explicar las diferencias de los controles
    quitar = set(agregados)
    rel_sarem = relacion(va, vb, [par for par in pares if par not in quitar])
    pasos.append({'de': va, 'a': vb, 'rel': rel, 'rel_sarem': rel_sarem, 'ex': ex, 'tipo': tipo(rel), 'agregados': agregados, 'notas': notas})


def cadena(desde, hasta, clave='rel'):
    acum = {c: {c} for c in S[desde]}
    for p in pasos[IDX[desde]:IDX[hasta]]:
        acum = {o: set().union(*(p[clave].get(d, set()) for d in ds)) for o, ds in acum.items()}
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
    validos = origen <= S[va] and destino <= S[vb]
    parcial = validos and not completa
    if not validos:
        descartadas.append({'tabla': f'{sa}_{sb}', 'de': va, 'a': vb, 'motivo': 'sus códigos no coinciden con las versiones'})
        continue
    directa = {(o, d) for o, d in pares}
    # control parcial: la tabla solo trae los códigos que cambian; se comparan solo esos códigos de origen
    calc = {(o, d) for o, ds in cadena(va, vb).items() for d in ds if completa or o in origen}
    controles.append({'de': va, 'a': vb, 'tabla': f'{sa}_{sb}', 'parcial': parcial,
                      'pares_cadena': len(calc), 'pares_sarem': len(directa),
                      'solo_cadena': sorted(calc - directa), 'solo_sarem': sorted(directa - calc)})

# Diferencias de los controles que se explican por las decisiones de VERIFICAR_OMA: vínculos de la
# cadena que llegan a un destino agregado o marcado, y vínculos de SAREM hacia un destino al que la
# OMA no manda nada desde esa subpartida.
for k in controles:
    eds = [cfg['edicion'] for (va, vb), cfg in VERIFICAR_OMA.items() if IDX[k['de']] <= IDX[va] and IDX[vb] <= IDX[k['a']]]
    cruza = bool(eds)
    def sin_oma(o, d):
        return o[:6] != d[:6] and not any(soporta(e, o, d) for e in eds)
    def con_oma(o, d):
        return o[:6] != d[:6] and any(soporta(e, o, d) for e in eds)
    def por_texto(o, d):
        # la OMA lo admite solo en general ("subpartidas aplicables de las partidas o capítulos..."), sin decir
        # qué códigos: las tablas de SAREM pueden no coincidir entre sí en cuáles códigos de 8 dígitos entran
        return o[:6] != d[:6] and any(any(d.startswith(x) for x in (W_ED[e].get(o[:4], set()) | W_ED[e].get(o[:2], set())
                                                                         | {y for y in W_ED[e].get(o[:6], set()) if len(y) < 6}))
                                      for e in eds)
    # en la cadena: solo existe gracias a un vínculo agregado (no aparece al encadenar solo con SAREM)
    solo_sarem_cadena = {(o, d) for o, ds in cadena(k['de'], k['a'], 'rel_sarem').items() for d in ds}
    # o la OMA lo registra (por subpartida o en general) y la tabla larga de SAREM no lo tiene
    k['solo_cadena_sin_explicar'] = [par for par in k['solo_cadena'] if par in solo_sarem_cadena
                                   and not (cruza and (por_texto(*par) or con_oma(*par)))]
    k['solo_sarem_sin_explicar'] = [par for par in k['solo_sarem'] if not (cruza and (sin_oma(*par) or por_texto(*par)))]

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
           'versiones_extra': VERSIONES_EXTRA, 'descartes': descartes, 'informes_oma': informes,
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
