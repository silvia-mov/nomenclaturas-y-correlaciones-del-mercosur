import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
d=pd.read_csv("/home/user/nomenclaturas-y-correlaciones-del-mercosur/datos/cambios_por_paso_2002_2026.csv")
d["paso"]=d.version_nueva.str.replace("NCM_","").str.replace("_","-")
t=d.groupby(["paso","tipo_cambio"]).codigo_viejo.nunique().unstack(fill_value=0)
t=t.loc[sorted(t.index,key=lambda s:[int(x) for x in s.split("-")])]
# colores bien distintos en claridad (se distinguen también con daltonismo): oscuro, medio, claro, oscuro rosado
COL={"complejo":"#1f6f5c","renumerado":"#ff5883","se divide":"#b9eee1","se fusiona":"#7a1f3d"}
v=pd.read_csv("/home/user/nomenclaturas-y-correlaciones-del-mercosur/datos/versiones.csv"); N=dict(zip(v.version,v.codigos_8_digitos))
for modo,bg,fg,gr in (("light","#ffffff","#222","#ddd"),("dark","#17141a","#eee","#333")):
    f,a=plt.subplots(figsize=(14,5.6),dpi=100); f.patch.set_facecolor(bg); a.set_facecolor(bg)
    b=None
    for i,c in enumerate(t.columns):
        a.bar(t.index,t[c],bottom=b,color=COL[c],label=c,width=.7,edgecolor=bg,linewidth=.6); b=t[c] if b is None else b+t[c]
    a.set_title("Códigos NCM que cambian en cada nueva versión, 2002–2026",loc="left",color=fg,fontsize=17,fontweight="bold",pad=34); a.set_ylim(0,3400)
    a.text(0,1.03,"Cantidad de códigos de 8 dígitos de la versión anterior, por tipo de cambio. Fuente: SAREM (MERCOSUR).",transform=a.transAxes,color=fg,fontsize=11)
    a.legend(frameon=False,labelcolor=fg,ncol=len(t.columns),loc="upper left",fontsize=11)
    tot=t.sum(axis=1)
    for k,(p,e) in enumerate([("2007-1","IV"),("2012-1","V"),("2017-1","VI"),("2022-1","VII")]):
        if p in tot.index:
            vv=d[d.paso==p].version_vieja.iloc[0]; pct=d[d.paso==p].codigo_viejo.nunique()/N[vv]*100
            a.text(list(t.index).index(p),tot[p]+40,e+f" Enmienda del SA\n{pct:.1f} % de los códigos".replace(".",",",1),ha="center",color=fg,fontsize=10)
    a.tick_params(colors=fg,labelsize=10); plt.setp(a.get_xticklabels(),rotation=45,ha="right")
    for s in a.spines.values(): s.set_visible(False)
    a.yaxis.grid(True,color=gr); a.set_axisbelow(True)
    f.tight_layout(); f.savefig(f"/home/user/nomenclaturas-y-correlaciones-del-mercosur/docs/img/cambios_ncm_{modo}.png",facecolor=bg)
print(t)
