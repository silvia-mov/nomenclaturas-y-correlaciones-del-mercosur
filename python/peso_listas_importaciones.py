"""Peso de cada lista de Paraguay (BK, BIT, LNE, materias primas) en las importaciones, por año, con los despachos
de la DNIT (archivos anuales del proyecto comercio-exterior-paraguay-acuerdos / repo dnit-datos-anuales).

Para cada año se usa la última notificación de esa lista hasta el 31 de diciembre (la de materias primas, la del año).
Importado en la lista = CIF (FOB + flete + seguro) de los despachos que se cuentan (SE_CUENTA = SI) cuyo código NCM
de 8 dígitos está en la lista. "Sin acuerdo" = lo que no usó una preferencia: ahí es donde la lista cambia el arancel.
Uso: python3 python/peso_listas_importaciones.py <carpeta con DNIT_<año>_importacion.xlsx>
Salida: datos/listas/peso_listas_importaciones.csv
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
carpeta = Path(sys.argv[1])
L = pd.read_csv(RAIZ / "datos" / "listas" / "listas_notificadas.csv", dtype=str, keep_default_na=False)
L["fecha"] = pd.to_datetime(L["fecha"])
filas = []
for a in range(2018, 2026):
    ruta = carpeta / f"DNIT_{a}_importacion.xlsx"
    if not ruta.exists():
        continue
    d = pd.read_excel(ruta, sheet_name="Datos", engine="calamine",
                      usecols=["SE_CUENTA", "POSICION", "ACUERDO", "FOB DOLAR", "FLETE DOLAR", "SEGURO DOLAR", "DERECHO"])
    d = d[d["SE_CUENTA"] == "SI"]
    ncm = d["POSICION"].astype(str).str.replace(".", "", regex=False).str[:8]
    cif = d["FOB DOLAR"] + d["FLETE DOLAR"] + d["SEGURO DOLAR"]
    sin = d["ACUERDO"].astype(str).str.upper().isin(["SIN ACUERDO", "OMC", "NAN", ""])
    tot = cif.sum()
    for lista in ("BK", "BIT", "LNE", "RMP"):
        g = L[(L["lista"] == lista) & (L["fecha"] <= f"{a}-12-31")]
        if g.empty:
            continue
        ult = g[g["fecha"] == g["fecha"].max()]
        en = ncm.isin(set(ult["ncm"]))
        filas.append({"AÑO": a, "LISTA": lista, "NOTIFICACION_USADA": ult["notificacion"].iloc[0],
                      "IMPORTADO_TOTAL_USD": tot, "IMPORTADO_EN_LISTA_USD": cif[en].sum(),
                      "PCT_DEL_TOTAL": cif[en].sum() / tot * 100,
                      "EN_LISTA_SIN_ACUERDO_USD": cif[en & sin].sum(),
                      "EN_LISTA_SIN_ACUERDO_ARANCEL_0_USD": cif[en & sin & (d["DERECHO"] == 0)].sum()})
    print(a, "listo", flush=True)
r = pd.DataFrame(filas)
r.round(2).to_csv(RAIZ / "datos" / "listas" / "peso_listas_importaciones.csv", index=False, encoding="utf-8-sig")
print(r.pivot(index="AÑO", columns="LISTA", values="PCT_DEL_TOTAL").round(1).to_string())
print((r[r.AÑO == r.AÑO.max()].set_index("LISTA")[["IMPORTADO_EN_LISTA_USD", "EN_LISTA_SIN_ACUERDO_USD", "EN_LISTA_SIN_ACUERDO_ARANCEL_0_USD"]] / 1e6).round(0).to_string())
