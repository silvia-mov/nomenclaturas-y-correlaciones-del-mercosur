"""Exporta a CSV el resumen de versiones, el mapeo y los cambios por paso.

Uso: python python/exportar_csv.py datos/versiones.json datos/cadena.json datos
"""
import csv, json, os, sys

vers_path, cad_path, carpeta = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
V.update(C.get('versiones_extra', {}))   # versiones sin archivo de SAREM (armadas con las tablas)
desc = lambda v, c: V[v]['codigos'].get(c, [''])[0]

with open(os.path.join(carpeta, 'versiones.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version', 'anio', 'mes', 'codigos_8_digitos', 'titulo'])
    for v in sorted(V, key=lambda v: (V[v]['anio'], V[v]['mes'])):
        w.writerow([v, V[v]['anio'], V[v]['mes'], len(V[v]['codigos']), V[v]['titulo']])

orden = [v for v, _ in C['orden']]
FIN = C['fin']
RANGO = f"{V[orden[0]]['anio']}_{V[FIN]['anio']}"
# una fila por código, período y destino (sin textos largos, para que el archivo no pese demasiado)
with open(os.path.join(carpeta, f'mapeo_{RANGO}.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['codigo', 'valido_desde', 'valido_hasta', 'tipo_cambio', 'codigo_final', 'version_final', 'n_destinos', 'con_notas'])
    for g in sorted(C['agrupado'], key=lambda g: (g['codigo'], orden.index(g['desde']))):
        for d in g['destino']:
            w.writerow([g['codigo'], g['desde'], g['hasta'], g['tipo'], d, FIN, len(g['destino']), 'sí' if g.get('notas') else ''])

# una fila por código y período: descripción, camino y notas
with open(os.path.join(carpeta, f'caminos_{RANGO}.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['codigo', 'valido_desde', 'valido_hasta', 'descripcion', 'tipo_cambio', 'destinos', 'camino', 'notas'])
    for g in sorted(C['agrupado'], key=lambda g: (g['codigo'], orden.index(g['desde']))):
        if g['tipo'] == 'igual':
            continue
        w.writerow([g['codigo'], g['desde'], g['hasta'], desc(g['desde'], g['codigo']), g['tipo'], ' '.join(g['destino']),
                    ' | '.join(g['camino']), ' | '.join(g.get('notas', []))])

with open(os.path.join(carpeta, f'cambios_por_paso_{RANGO}.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version_vieja', 'version_nueva', 'codigo_viejo', 'marca_sarem', 'codigo_nuevo', 'tipo_cambio', 'nota'])
    for p in C['pasos']:
        for o, d, ex, t, *nota in p['filas']:
            w.writerow([p['de'], p['a'], o, 'ex' if ex else '', d, t, nota[0] if nota else ''])
with open(os.path.join(carpeta, 'vinculos_sarem_no_usados.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version_vieja', 'version_nueva', 'codigo_viejo', 'marca_sarem', 'codigo_nuevo', 'motivo'])
    for x in C.get('descartes', []):
        w.writerow([x['de'], x['a'], x['origen'], 'ex' if x['ex'] else '', x['destino'], x['motivo']])
print('ok')
