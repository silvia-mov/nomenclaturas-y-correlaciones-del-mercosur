"""Imagen de la tarjeta de la página "Listas de la nomenclatura" (versión clara y oscura).

Uso: python python/grafico_tarjeta_listas.py
Lee datos/listas/listas_resumen.csv y crea docs/img/tarjeta_listas_light.png y tarjeta_listas_dark.png.
"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

d = pd.read_csv("datos/listas/listas_resumen.csv", parse_dates=["fecha"])
COL = {"BK": "#FF5883", "BIT": "#39B89A", "LNE": "#FF91AD", "RMP": "#79D3BE"}
NOM = {"BK": "Bienes de capital (BK)", "BIT": "Informática y telecomunicaciones (BIT)",
       "LNE": "Lista nacional de excepciones (LNE)", "RMP": "Materias primas (RMP)"}
for modo, bg, fg, gr in (("light", "#ffffff", "#222", "#ddd"), ("dark", "#17141a", "#eee", "#333")):
    f, a = plt.subplots(figsize=(12, 5.6), dpi=100); f.patch.set_facecolor(bg); a.set_facecolor(bg)
    for l, c in COL.items():
        s = d[d.lista == l].sort_values("fecha")
        a.plot(s.fecha, s.codigos, color=c, lw=3.5, marker="o", ms=7, label=NOM[l])
    a.set_title("Códigos NCM en las listas de Paraguay, 2018–2026", loc="left", color=fg, fontsize=17, fontweight="bold", pad=34)
    a.text(0, 1.03, "Cantidad de códigos de 8 dígitos en cada notificación al MERCOSUR. RMP: por año.",
           transform=a.transAxes, color=fg, fontsize=11)
    a.legend(frameon=False, labelcolor=fg, ncol=2, loc="upper left", fontsize=11, bbox_to_anchor=(0, .99))
    a.set_ylim(0, d.codigos.max() * 1.3)
    a.tick_params(colors=fg, labelsize=11)
    for s in a.spines.values(): s.set_visible(False)
    a.yaxis.grid(True, color=gr); a.set_axisbelow(True)
    f.tight_layout(); f.savefig(f"docs/img/tarjeta_listas_{modo}.png", facecolor=bg)
print(d.groupby("lista").codigos.agg(["min", "max"]))
