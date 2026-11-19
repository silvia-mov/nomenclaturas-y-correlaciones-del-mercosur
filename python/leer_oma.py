"""Lee las tablas de correlación de la OMA (Tabla II, 6 dígitos) y las guarda como pares.

Los PDF se bajan de la página de la OMA y se guardan en originales/oma/ (no se publican aquí):
  SA 2012 -> 2017: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs_nomenclature_previous_editions/hs-nomenclature-2017-edition/correlation-tables-hs-2012-to-2017.aspx
    - table_ii_trp1217_en_rev1.pdf  (Tabla II, octubre 2016; ya incluye la corrección 2)
    - table_ii_a_trp1217_en.pdf     (anexo de la Tabla II, capítulo 44)
  SA 2017 -> 2022: https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs-nomenclature-2022-edition/correlation-tables-hs-2017-2022.aspx
    - table-ii_en.pdf               (Tabla II, noviembre 2020)

Uso: python python/leer_oma.py originales/oma datos
Crea datos/oma_2012_2017.json y datos/oma_2017_2022.json. Necesita pdftotext (poppler).
"""
import json, os, re, subprocess, sys

carpeta, salida = sys.argv[1:3]
EDICIONES = {
    '2012_2017': {'tabla': ['table_ii_trp1217_en_rev1.pdf'], 'anexo44': ['table_ii_a_trp1217_en.pdf'], 'minimo': 600},
    '2017_2022': {'tabla': ['table-ii_en.pdf'], 'anexo44': [], 'minimo': 600},
}


# Números de nota al pie pegados a un código en el PDF (se corrigen antes de leer).
# SA 2017 -> 2022: "28933.34" es la subpartida 2933.34 con la nota 2.
NOTAS_PEGADAS = {'28933.34': '2933.34'}


def leer(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    for mal, bien in NOTAS_PEGADAS.items():
        txt = txt.replace(mal, bien)
    pares, izq = [], None
    for line in txt.splitlines():
        cods = list(re.finditer(r'(ex\s?)?(\d{4})\.(\d{2})', line))
        if not cods:
            continue
        if len(cods) == 2:
            izq = cods[0].group(2) + cods[0].group(3)
            pares.append((izq, cods[1].group(2) + cods[1].group(3), bool(cods[1].group(1))))
        elif cods[0].start() < 60:          # columna izquierda: subpartida de la edición vieja
            izq = cods[0].group(2) + cods[0].group(3)
        elif izq:                           # columna derecha: subpartida de la edición nueva
            pares.append((izq, cods[0].group(2) + cods[0].group(3), bool(cods[0].group(1))))
    return pares


for ed, cfg in EDICIONES.items():
    tabla = [p for f in cfg['tabla'] for p in leer(os.path.join(carpeta, f))]
    anexo = [p for f in cfg['anexo44'] for p in leer(os.path.join(carpeta, f))]
    assert len(tabla) > cfg['minimo'], (ed, len(tabla))
    json.dump({'fuente': f'OMA, Tabla II SA {ed.replace("_", " -> ")}', 'tabla': tabla, 'anexo44': anexo},
              open(os.path.join(salida, f'oma_{ed}.json'), 'w'), ensure_ascii=False)
    print(f'SA {ed}: Tabla II {len(tabla)} pares | {len({a for a, _, _ in tabla})} subpartidas viejas | anexo {len(anexo)}')
