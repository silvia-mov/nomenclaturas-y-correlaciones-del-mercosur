"""Exporta a CSV el resumen de versiones, el mapeo y los cambios por paso.

Uso: python python/exportar_csv.py datos/versiones.json datos/cadena_2002_2006.json datos
"""
import csv, json, os, sys

vers_path, cad_path, carpeta = sys.argv[1:4]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
desc = lambda v, c: V[v]['codigos'].get(c, [''])[0]

with open(os.path.join(carpeta, 'versiones.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version', 'anio', 'mes', 'codigos_8_digitos', 'titulo'])
    for v in sorted(V, key=lambda v: (V[v]['anio'], V[v]['mes'])):
        w.writerow([v, V[v]['anio'], V[v]['mes'], len(V[v]['codigos']), V[v]['titulo']])

orden = [v for v, _ in C['orden']]
with open(os.path.join(carpeta, 'mapeo_2002_2006.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['codigo', 'valido_desde', 'valido_hasta', 'descripcion', 'tipo_cambio', 'codigo_oct2006', 'descripcion_oct2006', 'n_destinos', 'camino'])
    for g in sorted(C['agrupado'], key=lambda g: (g['codigo'], orden.index(g['desde']))):
        for d in g['destino']:
            w.writerow([g['codigo'], g['desde'], g['hasta'], desc(g['desde'], g['codigo']), g['tipo'], d,
                        desc('NCM_2006_10', d), len(g['destino']), ' | '.join(g['camino'])])

with open(os.path.join(carpeta, 'cambios_por_paso_2002_2006.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['version_vieja', 'version_nueva', 'codigo_viejo', 'marca_sarem', 'codigo_nuevo', 'tipo_cambio'])
    for p in C['pasos']:
        for o, d, ex, t in p['filas']:
            w.writerow([p['de'], p['a'], o, 'ex' if ex else '', d, t])
print('ok')
