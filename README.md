<div align="center">

# Nomenclatura Común del MERCOSUR: versiones y correlaciones

**¿A qué código de hoy corresponde un código NCM de otro año?**<br>
Las versiones de la NCM descargadas del sistema SAREM (2002–2026) y sus tablas de correlación,
encadenadas versión por versión, con el tipo de cambio de cada código y controles contra SAREM.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Datos](https://img.shields.io/badge/datos-SAREM%20·%20MERCOSUR-0b6e4f)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)

[Estado](#estado) · [Para qué sirve](#para-qué-sirve) · [Cómo leer el mapeo](#cómo-leer-el-mapeo) · [Inicio rápido](#inicio-rápido) · [Originales](originales/LEEME.md) · [Datos](datos/LEEME.md)

</div>

---

## Estado

| Tramo | Versiones | Correlaciones | Estado |
|---|---|---|---|
| 1. Enero 2002 – octubre 2006 | 11 | 10 tablas entre versiones seguidas | **Listo y controlado** |
| 2. Noviembre 2006 – enero 2010 (incluye la IV Enmienda del SA) | 9 | 9 tablas entre versiones seguidas | **Listo y controlado** |
| 3. Octubre 2010 – enero 2015 (incluye la V Enmienda del SA) | 10 | 10 tablas entre versiones seguidas | **Listo y controlado** |
| 4. Julio 2015 – 2026 | 33 versiones ya leídas | Tablas ya subidas | Pendiente |

## Para qué sirve

1. Llevar un código NCM de cualquier año a la versión que se necesite.
2. Comparar series de comercio de distintos años con la misma nomenclatura.
3. Traducir las listas de preferencias de los acuerdos comerciales, escritas en versiones viejas
   de la NCM, a la versión vigente.

## Cómo leer el mapeo

- **Válido desde / hasta.** Un mismo número de código puede llegar a destinos distintos según la
  fecha. Ejemplo: 0302.69.90 de 2002 se reparte en 15 códigos; el de 2003 en adelante sigue igual.
- **Tipo de cambio.** *Igual*: mismo código. *Renumerado*: cambia el número, 1 a 1. *Se divide*: un código viejo pasa a varios nuevos.
  *Se fusiona*: varios viejos van a uno nuevo. *Complejo*: las dos cosas a la vez.
- **Marca "ex" de SAREM.** Aparece solo cuando el código nuevo recibe mercadería de más de un código
  viejo. Las divisiones no llevan "ex" (comprobado en todas las tablas de versiones seguidas
  2002–2015, sin excepciones).
  Por eso el tipo de cambio se calcula con los datos y no con la marca.
- Si un código *se divide* o es *complejo*, la correspondencia es parcial: hay que mirar la
  descripción para saber a cuál de los destinos va cada producto. Las tablas de correlación ayudan,
  pero no tienen valor legal.

## Enero 2002 – enero 2015

Cantidad de códigos viejos según el tipo de cambio en cada paso.

| Paso | Igual | Renumerado | Se divide | Se fusiona | Complejo |
|---|---|---|---|---|---|
| ene 2002 → jul 2002 | 9.610 | 0 | 5 | 6 | 0 |
| jul 2002 → ene 2003 | 9.601 | 0 | 8 | 11 | 4 |
| ene 2003 → jul 2003 | 9.616 | 0 | 35 | 0 | 0 |
| jul 2003 → ene 2004 | 9.672 | 0 | 15 | 3 | 0 |
| ene 2004 → jul 2004 | 9.664 | 0 | 35 | 5 | 3 |
| jul 2004 → ene 2005 | 9.645 | 0 | 29 | 22 | 54 |
| ene 2005 → abr 2005 | 9.784 | 0 | 0 | 0 | 0 |
| abr 2005 → ene 2006 | 9.774 | 0 | 8 | 1 | 1 |
| ene 2006 → jul 2006 | 9.786 | 0 | 7 | 0 | 0 |
| jul 2006 → oct 2006 | 9.792 | 0 | 8 | 1 | 1 |
| oct 2006 → nov 2006 | 9.811 | 0 | 0 | 0 | 0 |
| **nov 2006 → ene 2007** | **8.397** | **498** | **73** | **515** | **328** |
| ene 2007 → jul 2007 | 9.705 | 0 | 7 | 1 | 1 |
| jul 2007 → ene 2008 | 9.654 | 8 | 21 | 5 | 33 |
| ene 2008 → jul 2008 | 9.757 | 1 | 3 | 3 | 1 |
| jul 2008 → ene 2009 | 9.730 | 7 | 7 | 10 | 13 |
| ene 2009 → abr 2009 | 9.758 | 1 | 18 | 4 | 4 |
| abr 2009 → oct 2009 | 9.805 | 0 | 4 | 0 | 0 |
| oct 2009 → ene 2010 | 9.796 | 0 | 10 | 4 | 4 |
| ene 2010 → oct 2010 | 9.816 | 0 | 17 | 0 | 2 |
| oct 2010 → ene 2011 | 9.868 | 0 | 1 | 0 | 0 |
| ene 2011 → abr 2011 | 9.869 | 0 | 1 | 0 | 0 |
| abr 2011 → oct 2011 | 9.855 | 3 | 9 | 4 | 0 |
| **oct 2011 → ene 2012** | **9.284** | **276** | **72** | **137** | **128** |
| ene 2012 → abr 2012 | 10.015 | 0 | 0 | 12 | 4 |
| abr 2012 → jul 2012 | 10.006 | 0 | 7 | 13 | 1 |
| jul 2012 → ene 2013 | 10.024 | 0 | 1 | 2 | 1 |
| ene 2013 → ene 2014 | 10.027 | 0 | 2 | 0 | 0 |
| ene 2014 → ene 2015 | 10.021 | 0 | 1 | 9 | 0 |

El paso a enero 2007 es la IV Enmienda del Sistema Armonizado (cambian 1.414 códigos) y el paso a
enero 2012, la V Enmienda (cambian 613).

**Controles.**
1. En las 29 tablas, cada código que desaparece tiene destino y cada código que aparece tiene origen.
2. La cadena armada paso a paso coincide exactamente con las 21 tablas directas de SAREM que cuadran
   con sus versiones: 7 desde enero 2002 (hasta enero 2003, julio 2003, enero 2004, julio 2004,
   enero 2007, julio 2008 y enero 2012) y 14 desde enero 2007 (hasta cada versión de enero 2008 a
   enero 2015). 0 diferencias en las 21.
3. **Decisión 2007:** la tabla de SAREM de noviembre 2006 a enero 2007 está incompleta (le faltan 9
   vínculos: pelo fino en los capítulos 61 y 62, y 8517.62.59). Se usa la tabla directa de octubre
   2006 a enero 2007, que tiene los mismos códigos de origen y coincide con las tablas largas.
4. **Decisión 2012:** a la tabla de octubre 2011 a enero 2012 le faltan 19 vínculos hacia la partida
   nueva 96.19 (compresas, tampones y pañales de cualquier materia), desde los capítulos 39, 61, 62 y
   63. Se agregan desde la tabla enero 2011 → enero 2012, y coinciden con las tablas largas.

## Inicio rápido

Se necesita Python 3.10+ con `openpyxl`. Primero se bajan los zip de las releases y se
descomprimen en `originales/` (ver [originales/LEEME.md](originales/LEEME.md)).

```bash
python python/leer_versiones.py originales/nomenclaturas datos/versiones.json
python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena.json
python python/exportar_csv.py datos/versiones.json datos/cadena.json datos
python python/excel_mapeo.py datos/versiones.json datos/cadena.json salidas/Mapeo_NCM_2002-2015.xlsx
```

| Carpeta | Contenido |
|---|---|
| [`originales/`](originales/LEEME.md) | Cómo bajar los archivos de SAREM (van como releases) |
| [`python/`](python/) | Programas |
| [`datos/`](datos/LEEME.md) | Resultados en CSV |
| [`salidas/`](salidas/) | Excel del mapeo |
| [`docs/`](docs/LEEME.md) | Futura página web |

## Fuente y aviso

**Fuente: Secretaría del MERCOSUR, sistema SAREM.** Este repositorio no está asociado a la
Secretaría del MERCOSUR ni cuenta con su participación o apoyo. Las correlaciones facilitan el
trabajo con distintas versiones de la NCM, pero **no tienen valor legal**: la clasificación de una
mercadería se rige por la nomenclatura y las normas vigentes.

Código bajo licencia MIT. Para citar el repositorio, ver [`CITATION.cff`](CITATION.cff).
