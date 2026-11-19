"""Lee las versiones de la NCM bajadas de SAREM y guarda, por versión, los códigos de 8 dígitos con descripción y AEC.

Uso: python python/leer_versiones.py originales/nomenclaturas datos/versiones.json
"""
import openpyxl, sys, glob, re, json, os
carpeta, salida = sys.argv[1], sys.argv[2]
def clave(f):
    m = re.search(r'NCM_(\d{4})(?:_(\d+))?\.xlsx$', f)
    return (int(m.group(1)), int(m.group(2) or 0))
out = {}
for f in sorted(glob.glob(os.path.join(carpeta, 'NCM_*.xlsx')), key=clave):
    a, mth = clave(f)
    ws = openpyxl.load_workbook(f, read_only=True).active
    rows = ws.iter_rows(values_only=True)
    titulo = next(rows)[0]; generado = next(rows)[0]; hdr = next(rows)
    iaec = next(i for i, h in enumerate(hdr) if h and str(h).startswith('AEC'))
    cod = {}
    for r in rows:
        if r and r[0] and re.fullmatch(r'\d{8}', str(r[0]).strip()):
            d = re.sub(r'<[^>]+>', '', str(r[1] or '')).replace('\t', ' ')
            cod[str(r[0]).strip()] = [re.sub(r'\s+', ' ', d).strip(), r[iaec]]
    nombre = os.path.basename(f)[:-5]
    out[nombre] = {'anio': a, 'mes': mth, 'titulo': titulo, 'generado': generado, 'codigos': cod}
    print(nombre, len(cod), '|', titulo[-40:])
json.dump(out, open(salida, 'w'), ensure_ascii=False)
