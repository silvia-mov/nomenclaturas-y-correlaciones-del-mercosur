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
| 1. Enero 2002 – octubre 2006 | 12 | 10 tablas entre versiones seguidas | **Listo y controlado** |
| 2. 2006 – 2007 (IV Enmienda del SA) | | | Pendiente |
| 3. 2007 – 2026 | 51 versiones ya leídas | Falta subir las tablas | Pendiente |

## Para qué sirve

1. Llevar un código NCM de cualquier año a la versión que se necesite.
2. Comparar series de comercio de distintos años con la misma nomenclatura.
3. Traducir las listas de preferencias de los acuerdos comerciales, escritas en versiones viejas
   de la NCM, a la versión vigente.

## Cómo leer el mapeo

- **Válido desde / hasta.** Un mismo número de código puede llegar a destinos distintos según la
  fecha. Ejemplo: 0302.69.90 de 2002 se reparte en 15 códigos; el de 2003 en adelante sigue igual.
- **Tipo de cambio.** *Igual*: mismo código. *Se divide*: un código viejo pasa a varios nuevos.
  *Se fusiona*: varios viejos van a uno nuevo. *Complejo*: las dos cosas a la vez.
- **Marca "ex" de SAREM.** Aparece solo cuando el código nuevo recibe mercadería de más de un código
  viejo. Las divisiones no llevan "ex" (comprobado en las 19.853 filas del tramo 1, sin excepciones).
  Por eso el tipo de cambio se calcula con los datos y no con la marca.
- Si un código *se divide* o es *complejo*, la correspondencia es parcial: hay que mirar la
  descripción para saber a cuál de los destinos va cada producto. Las tablas de correlación ayudan,
  pero no tienen valor legal.

## Tramo 1: enero 2002 – octubre 2006

| Paso | Igual | Se divide | Se fusiona | Complejo |
|---|---|---|---|---|
| ene 2002 → jul 2002 | 9.610 | 5 | 6 | 0 |
| jul 2002 → ene 2003 | 9.601 | 8 | 11 | 4 |
| ene 2003 → jul 2003 | 9.616 | 35 | 0 | 0 |
| jul 2003 → ene 2004 | 9.672 | 15 | 3 | 0 |
| ene 2004 → jul 2004 | 9.664 | 35 | 5 | 3 |
| jul 2004 → ene 2005 | 9.645 | 29 | 22 | 54 |
| ene 2005 → abr 2005 | 9.784 | 0 | 0 | 0 |
| abr 2005 → ene 2006 | 9.774 | 8 | 1 | 1 |
| ene 2006 → jul 2006 | 9.786 | 7 | 0 | 0 |
| jul 2006 → oct 2006 | 9.792 | 8 | 1 | 1 |

**Controles.**
1. En las 10 tablas, cada código que desaparece tiene destino y cada código que aparece tiene origen.
2. La cadena armada paso a paso coincide exactamente con las tablas directas de SAREM desde enero
   2002 hasta enero 2003, julio 2003, enero 2004 y julio 2004 (0 diferencias en los cuatro).

## Inicio rápido

Se necesita Python 3.10+ con `openpyxl`. Primero se bajan los zip de las releases y se
descomprimen en `originales/` (ver [originales/LEEME.md](originales/LEEME.md)).

```bash
python python/leer_versiones.py originales/nomenclaturas datos/versiones.json
python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena_2002_2006.json
python python/exportar_csv.py datos/versiones.json datos/cadena_2002_2006.json datos
python python/excel_mapeo.py datos/versiones.json datos/cadena_2002_2006.json salidas/Mapeo_NCM_2002-2006.xlsx
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
