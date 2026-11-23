import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
d=pd.read_csv("/home/user/nomenclaturas-y-correlaciones-del-mercosur/datos/cambios_por_paso_2002_2026.csv")
d["paso"]=d.version_nueva.str.replace("NCM_","").str.replace("_","-")
t=d.groupby(["paso","tipo_cambio"]).codigo_viejo.nunique().unstack(fill_value=0)
t=t.loc[sorted(t.index,key=lambda s:[int(x) for x in s.split("-")])]
# Por año (las versiones de un mismo año se suman) y todos los años 2002–2026, aunque no tengan cambios
paso_anio={p:int(p.split("-")[0]) for p in t.index}
ty=t.groupby(paso_anio).sum().reindex(range(2003,2027),fill_value=0)
# colores bien distintos en claridad (se distinguen también con daltonismo): oscuro, medio, claro, oscuro rosado
COL={"complejo":"#1f6f5c","renumerado":"#ff5883","se divide":"#b9eee1","se fusiona":"#7a1f3d"}
v=pd.read_csv("/home/user/nomenclaturas-y-correlaciones-del-mercosur/datos/versiones.csv"); N=dict(zip(v.version,v.codigos_8_digitos))
for modo,bg,fg,gr in (("light","#ffffff","#1d1a1c","#f3dde4"),("dark","#201b1d","#f5eef1","#3a2f33")):
    f,a=plt.subplots(figsize=(12,5.2),dpi=150); f.patch.set_facecolor(bg); a.set_facecolor(bg)
    b=None
    for i,c in enumerate(ty.columns):
        a.bar(ty.index,ty[c],bottom=b,color=COL[c],label=c,width=.72,edgecolor=bg,linewidth=.8); b=ty[c] if b is None else b+ty[c]
    a.set_title("Códigos NCM que cambian en cada nueva versión, 2002–2026",loc="left",color=fg,fontsize=17,fontweight="bold",pad=34); a.set_ylim(0,3400)
    a.text(0,1.03,"Cantidad de códigos de 8 dígitos de la versión anterior, por tipo de cambio. Fuente: SAREM (MERCOSUR).",transform=a.transAxes,color=fg,fontsize=11)
    a.legend(frameon=False,labelcolor=fg,ncol=len(ty.columns),loc="upper left",fontsize=11,handlelength=1,handleheight=1)
    tot=t.sum(axis=1); toty=ty.sum(axis=1)
    for k,(p,e) in enumerate([("2007-1","IV"),("2012-1","V"),("2017-1","VI"),("2022-1","VII")]):
        if p in tot.index:
            vv=d[d.paso==p].version_vieja.iloc[0]; pct=d[d.paso==p].codigo_viejo.nunique()/N[vv]*100
            a.text(int(p.split("-")[0]),toty[int(p.split("-")[0])]+60,e+f" Enmienda del SA\n{pct:.1f} % de los códigos".replace(".",",",1),ha="center",color=fg,fontsize=10)
    a.tick_params(colors=fg,labelsize=10,length=0); a.set_xticks(range(2003,2027,2)); a.set_xlim(2002.3,2026.7)
    a.text(0,-0.1,"Versiones del mismo año sumadas. Sin las enmiendas, los cambios son pocos y menores.",transform=a.transAxes,color=fg,fontsize=9.5,alpha=.75)
    for s in a.spines.values(): s.set_visible(False)
    a.yaxis.grid(True,color=gr,linewidth=.8); a.set_axisbelow(True)
    f.tight_layout(); f.savefig(f"/home/user/nomenclaturas-y-correlaciones-del-mercosur/docs/img/cambios_ncm_{modo}.png",facecolor=bg)
print(t)
