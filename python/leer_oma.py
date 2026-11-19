"""Lee la Tabla II de la OMA (Sistema Armonizado 2012 -> 2017, 6 dígitos) y la guarda como pares.

Los PDF se bajan de la página de la OMA y se guardan en originales/oma/ (no se publican aquí):
  https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs_nomenclature_previous_editions/hs-nomenclature-2017-edition/correlation-tables-hs-2012-to-2017.aspx
  - table_ii_trp1217_en_rev1.pdf  (Tabla II, octubre 2016)
  - table_ii_a_trp1217_en.pdf     (Anexo de la Tabla II, capítulo 44)
La corrección 2 (subpartida 4401.39) ya está incluida en la Tabla II de octubre 2016; la corrección 1
es solo de la Tabla I.

Uso: python python/leer_oma.py originales/oma datos/oma_2012_2017.json
Necesita pdftotext (poppler).
"""
import json, os, re, subprocess, sys

carpeta, salida = sys.argv[1:3]


def leer(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    pares, izq = [], None
    for line in txt.splitlines():
        cods = list(re.finditer(r'(ex)?(\d{4})\.(\d{2})', line))
        if not cods:
            continue
        if len(cods) == 2:
            izq = cods[0].group(2) + cods[0].group(3)
            pares.append((izq, cods[1].group(2) + cods[1].group(3), bool(cods[1].group(1))))
        elif cods[0].start() < 60:          # columna izquierda: subpartida SA 2012
            izq = cods[0].group(2) + cods[0].group(3)
        elif izq:                           # columna derecha: subpartida SA 2017
            pares.append((izq, cods[0].group(2) + cods[0].group(3), bool(cods[0].group(1))))
    return pares


tabla = leer(os.path.join(carpeta, 'table_ii_trp1217_en_rev1.pdf'))
anexo = leer(os.path.join(carpeta, 'table_ii_a_trp1217_en.pdf'))
assert len(tabla) > 600 and len(anexo) > 20
json.dump({'fuente': 'OMA, Tabla II SA 2012 -> SA 2017 (octubre 2016) y su anexo del capítulo 44',
           'tabla': tabla, 'anexo44': anexo}, open(salida, 'w'), ensure_ascii=False)
print('Tabla II:', len(tabla), 'pares |', len({a for a, _, _ in tabla}), 'subpartidas SA 2012 | anexo cap. 44:', len(anexo))
