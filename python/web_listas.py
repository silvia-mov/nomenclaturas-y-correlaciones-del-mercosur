"""Arma los datos de la página de listas (docs/datos/) y la NCM vigente en CSV.

Uso: python python/web_listas.py datos/listas/listas_notificadas.csv datos/versiones.json datos/cadena.json docs/datos datos/listas
"""
import csv, json, os, sys

lst_path, vers_path, cad_path, salida_web, salida_csv = sys.argv[1:6]
V = json.load(open(vers_path, encoding='utf-8'))
C = json.load(open(cad_path, encoding='utf-8'))
FIN = C['fin']
os.makedirs(salida_web, exist_ok=True)

# NCM vigente: código, descripción y AEC
ncm = V[FIN]['codigos']
with open(os.path.join(salida_csv, f'ncm_{FIN[4:].lower()}.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['ncm', 'descripcion', 'aec'])
    for c in sorted(ncm):
        w.writerow([c, ncm[c][0], ncm[c][1]])

# buscador: por código, en qué listas y notificaciones estuvo, con su arancel, y su código vigente
datos, notifs = {}, {}
for x in csv.DictReader(open(lst_path, encoding='utf-8')):
    c = x['ncm']
    e = datos.setdefault(c, {'l': {}, 'v': x[f'codigos_{FIN[4:].lower()}'].split(), 't': x['tipo_cambio'], 'd': ''})
    e['l'].setdefault(x['lista'], {})[x['notificacion']] = None if x['lista'] == 'RMP' else x['arancel_nacional_vigente']
    notifs.setdefault(x['lista'], [])
    if x['notificacion'] not in notifs[x['lista']]:
        notifs[x['lista']].append(x['notificacion'])
    e['v'] = x[f'codigos_{FIN[4:].lower()}'].split()       # destinos según la notificación más reciente
    e['t'] = x['tipo_cambio']
# descripciones una sola vez: de la NCM vigente, o de la última versión en que existió el código
ultima = {}
for v in [v for v, _ in C['orden'] if v in V]:
    for c, d in V[v]['codigos'].items():
        ultima[c] = d[0]
desc = {}
for c, e in datos.items():
    del e['d']
    for k in [c] + e['v']:
        desc[k] = ncm.get(k, [ultima.get(k, '')])[0]
json.dump({'version': FIN, 'notificaciones': notifs, 'codigos': datos, 'desc': desc},
          open(os.path.join(salida_web, 'listas.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(datos), 'códigos en el buscador |', os.path.getsize(os.path.join(salida_web, 'listas.json')) // 1024, 'KB')
