import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
d=pd.read_csv("/home/user/nomenclaturas-y-correlaciones-del-mercosur/datos/cambios_por_paso_2002_2010.csv")
d["paso"]=d.version_nueva.str.replace("NCM_","").str.replace("_","-")
t=d.groupby(["paso","tipo_cambio"]).codigo_viejo.nunique().unstack(fill_value=0)
t=t.loc[sorted(t.index,key=lambda s:[int(x) for x in s.split("-")])]
cols=["#39B89A","#FF5883","#79D3BE","#FF91AD","#FEC9D7","#B9EEE1"]
for modo,bg,fg,gr in (("light","#ffffff","#222","#ddd"),("dark","#17141a","#eee","#333")):
    f,a=plt.subplots(figsize=(12,5.6),dpi=100); f.patch.set_facecolor(bg); a.set_facecolor(bg)
    b=None
    for i,c in enumerate(t.columns):
        a.bar(t.index,t[c],bottom=b,color=cols[i%6],label=c,width=.7); b=t[c] if b is None else b+t[c]
    a.set_title("Códigos NCM que cambian en cada nueva versión, 2002–2010",loc="left",color=fg,fontsize=17,fontweight="bold",pad=34)
    a.text(0,1.03,"Cantidad de códigos de 8 dígitos de la versión anterior, por tipo de cambio. Fuente: SAREM (MERCOSUR).",transform=a.transAxes,color=fg,fontsize=11)
    a.legend(frameon=False,labelcolor=fg,ncol=len(t.columns),loc="upper left",fontsize=11)
    a.annotate("IV Enmienda del\nSistema Armonizado",xy=(9.4,1250),xytext=(11,1100),color=fg,fontsize=11,arrowprops=dict(arrowstyle="->",color=fg))
    a.tick_params(colors=fg,labelsize=10); plt.setp(a.get_xticklabels(),rotation=45,ha="right")
    for s in a.spines.values(): s.set_visible(False)
    a.yaxis.grid(True,color=gr); a.set_axisbelow(True)
    f.tight_layout(); f.savefig(f"/home/user/nomenclaturas-y-correlaciones-del-mercosur/docs/img/cambios_ncm_{modo}.png",facecolor=bg)
print(t)
