"""Gráfico de líneas: cantidad de códigos en cada lista de Paraguay (BK, BIT, LNE y materias primas), 2018–2026.

Uso (desde la raíz del repositorio): python3 python/grafico_listas.py
Lee datos/listas/listas_resumen.csv y guarda docs/img/listas_{light,dark}.png.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tipografia  # noqa: E402,F401  (Fraunces + Source Sans 3)
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
d = pd.read_csv(RAIZ / "datos" / "listas" / "listas_resumen.csv", parse_dates=["fecha"])
COL = {"BK": "#3f6b65", "BIT": "#774d78", "LNE": "#4f3050", "RMP": "#5e8f88"}
NOM = {"BK": "Bienes de capital (BK)", "BIT": "Informática y telecom. (BIT)", "LNE": "Excepciones (LNE)", "RMP": "Materias primas"}
for modo, bg, fg, gr in (("light", "#ffffff", "#222222", "#dddddd"), ("dark", "#17141a", "#eeeeee", "#333333")):
    f, a = plt.subplots(figsize=(11, 5), dpi=110)
    f.patch.set_facecolor(bg); a.set_facecolor(bg)
    for l, g in d.groupby("lista"):
        g = g.sort_values("fecha")
        a.plot(g["fecha"], g["codigos"], color=COL.get(l, fg), linewidth=2.4, marker="o", markersize=4, label=NOM.get(l, l))
        a.text(g["fecha"].iloc[-1] + pd.Timedelta(days=40), g["codigos"].iloc[-1], f"{g['codigos'].iloc[-1]:,}".replace(",", "."),
               color=COL.get(l, fg), fontsize=10, va="center", fontweight="bold")
    a.axhline(649, color=fg, linestyle="--", linewidth=1)
    a.text(d["fecha"].min(), 649 - 45, "Tope de la LNE de Paraguay: 649 códigos (Dec. CMC 11/21); desde 2025, hasta 50 más temporarios (Dec. CMC 01/25)",
           color=fg, fontsize=9)
    a.set_ylim(0, 1400)
    a.set_title("Cuántos códigos tuvo cada lista de Paraguay, 2018–2026", loc="left", color=fg, fontsize=15, fontweight="bold", pad=30)
    a.text(0, 1.02, "Códigos NCM de 8 dígitos en cada notificación al MERCOSUR. Faltan las de 2018 (2.º semestre), 2019 y 2024, y materias primas 2021–2022.",
           transform=a.transAxes, color=fg, fontsize=9.5)
    a.legend(frameon=False, labelcolor=fg, ncol=4, loc="upper left", bbox_to_anchor=(0, 0.99), fontsize=9.5)
    a.tick_params(colors=fg)
    for s in a.spines.values(): s.set_visible(False)
    a.yaxis.grid(True, color=gr); a.set_axisbelow(True)
    f.tight_layout()
    f.savefig(RAIZ / "docs" / "img" / f"listas_{modo}.png", facecolor=bg)
print("ok")
