<div align="center">

# Nomenclatura Común del MERCOSUR: versiones y correlaciones

**¿A qué código de hoy corresponde un código NCM de otro año?**<br>
Las versiones de la NCM descargadas del sistema SAREM (2002–2026) y sus tablas de correlación,
encadenadas versión por versión, con el tipo de cambio de cada código y controles contra SAREM.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Datos](https://img.shields.io/badge/datos-SAREM%20·%20MERCOSUR-0b6e4f)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)

[Listas de la nomenclatura (página)](https://silvia-mov.github.io/nomenclaturas-y-correlaciones-del-mercosur/listas.html) · [Estado](#estado) · [Para qué sirve](#para-qué-sirve) · [Cómo leer el mapeo](#cómo-leer-el-mapeo) · [Inicio rápido](#inicio-rápido) · [Originales](originales/LEEME.md) · [Datos](datos/LEEME.md)

</div>

---

## Estado

| Tramo | Versiones | Correlaciones | Estado |
|---|---|---|---|
| 1. Enero 2002 – octubre 2006 | 11 | 10 tablas entre versiones seguidas | **Listo y controlado** |
| 2. Noviembre 2006 – enero 2010 (incluye la IV Enmienda del SA) | 9 | 9 tablas entre versiones seguidas | **Listo y controlado** |
| 3. Octubre 2010 – enero 2015 (incluye la V Enmienda del SA) | 10 | 10 tablas entre versiones seguidas | **Listo y controlado** |
| 4. Julio 2015 – enero 2019 (incluye la VI Enmienda del SA) | 10 | 10 tablas entre versiones seguidas, revisadas con la OMA | **Listo y controlado** |
| 5. Marzo 2019 – enero 2022 (incluye la VII Enmienda del SA) | 10 (marzo 2019 sin archivo) | 10 tablas entre versiones seguidas, revisadas con la OMA | **Listo y controlado** |
| 6. Julio 2022 – noviembre 2026 | 14 | 13 tablas entre versiones seguidas (noviembre 2026 no tiene tabla: mismos códigos que octubre) | **Listo y controlado** |

**El mapeo está completo: cualquier código NCM de enero 2002 a noviembre 2026 llega a la NCM de
noviembre 2026.**

## Listas de la nomenclatura

Las listas de Paraguay notificadas al MERCOSUR: **bienes de capital (BK)**, **bienes de informática y
telecomunicaciones (BIT)**, **lista nacional de excepciones (LNE)** y **régimen de materias primas
(RMP)**, de 2018 a 2026, con el arancel nacional vigente de cada código y cada código traducido a la
NCM de hoy con el mapeo de este repositorio.

- Página con explicaciones, buscador y descargas: [`docs/listas.html`](docs/listas.html)
  (<https://silvia-mov.github.io/nomenclaturas-y-correlaciones-del-mercosur/listas.html>).
- Datos: [`datos/listas/`](datos/LEEME.md) y `salidas/Listas_BK_BIT_LNE_RMP.xlsx`.

```bash
python python/listas_notificadas.py <carpeta con los zip de las notificaciones> datos/versiones.json datos/cadena.json datos/listas salidas/Listas_BK_BIT_LNE_RMP.xlsx
python python/web_listas.py datos/listas/listas_notificadas.csv datos/versiones.json datos/cadena.json docs/datos datos/listas
```

Las notificaciones vienen de las releases `mercosur_listas` del repositorio `varios` (privado).

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
  2002–2022, sin excepciones).
  Por eso el tipo de cambio se calcula con los datos y no con la marca.
- Si un código *se divide* o es *complejo*, la correspondencia es parcial: hay que mirar la
  descripción para saber a cuál de los destinos va cada producto. Las tablas de correlación ayudan,
  pero no tienen valor legal.

## Enero 2002 – noviembre 2026

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
| **nov 2006 → ene 2007** | **8.190** | **373** | **66** | **552** | **630** |
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
| **oct 2011 → ene 2012** | **9.221** | **243** | **70** | **142** | **221** |
| ene 2012 → abr 2012 | 10.015 | 0 | 0 | 12 | 4 |
| abr 2012 → jul 2012 | 10.006 | 0 | 7 | 13 | 1 |
| jul 2012 → ene 2013 | 10.024 | 0 | 1 | 2 | 1 |
| ene 2013 → ene 2014 | 10.027 | 0 | 2 | 0 | 0 |
| ene 2014 → ene 2015 | 10.021 | 0 | 1 | 9 | 0 |
| ene 2015 → jul 2015 | 10.022 | 0 | 2 | 2 | 0 |
| jul 2015 → ene 2016 | 10.024 | 0 | 1 | 0 | 2 |
| ene 2016 → jul 2016 | 10.018 | 0 | 1 | 5 | 5 |
| jul 2016 → ago 2016 | 10.020 | 1 | 14 | 0 | 0 |
| ago 2016 → set 2016 | 10.020 | 1 | 0 | 55 | 0 |
| **set 2016 → ene 2017** | **9.298** | **209** | **88** | **81** | **359** |
| ene 2017 → jul 2017 | 10.216 | 0 | 6 | 4 | 0 |
| jul 2017 → ene 2018 | 10.227 | 0 | 10 | 1 | 1 |
| ene 2018 → jul 2018 | 10.246 | 0 | 7 | 1 | 1 |
| jul 2018 → ene 2019 | 10.257 | 0 | 5 | 3 | 1 |
| ene 2019 → mar 2019 | 10.270 | 0 | 0 | 0 | 0 |
| mar 2019 → jul 2019 | 10.267 | 0 | 3 | 0 | 0 |
| jul 2019 → ene 2020 | 10.241 | 2 | 14 | 7 | 9 |
| ene 2020 → jul 2020 | 10.297 | 3 | 0 | 0 | 0 |
| jul 2020 → ene 2021 | 10.299 | 0 | 1 | 0 | 0 |
| ene 2021 → abr 2021 | 10.300 | 0 | 1 | 0 | 0 |
| abr 2021 → jul 2021 | 10.277 | 0 | 23 | 1 | 1 |
| jul 2021 → set 2021 | 10.325 | 0 | 5 | 7 | 0 |
| set 2021 → "2022" | 10.337 | 0 | 0 | 0 | 0 |
| **"2022" → ene 2022** | **7.353** | **125** | **56** | **82** | **2.721** |
| ene 2022 → jul 2022 | 10.426 | 0 | 3 | 0 | 4 |
| jul 2022 → set 2022 | 10.434 | 0 | 3 | 0 | 0 |
| set 2022 → ene 2023 | 10.430 | 1 | 9 | 0 | 0 |
| ene 2023 → abr 2023 | 10.447 | 0 | 4 | 0 | 0 |
| abr 2023 → jul 2023 | 10.455 | 0 | 0 | 0 | 0 |
| jul 2023 → nov 2023 | 10.451 | 0 | 2 | 1 | 1 |
| nov 2023 → abr 2024 | 10.431 | 1 | 20 | 3 | 3 |
| abr 2024 → jul 2024 | 10.480 | 8 | 4 | 0 | 6 |
| jul 2024 → ene 2025 | 10.502 | 0 | 0 | 1 | 1 |
| ene 2025 → oct 2025 | 10.501 | 0 | 3 | 0 | 0 |
| oct 2025 → ene 2026 | 10.507 | 0 | 0 | 0 | 0 |
| ene 2026 → feb 2026 | 10.488 | 0 | 8 | 6 | 5 |
| feb 2026 → oct 2026 | 10.514 | 0 | 1 | 0 | 0 |
| oct 2026 → nov 2026 | 10.516 | 0 | 0 | 0 | 0 |

Los pasos a enero 2007, enero 2012, enero 2017 y enero 2022 son la IV, la V, la VI y la VII Enmienda
del Sistema Armonizado (cambian 1.621, 676, 737 y 2.984 códigos, ya revisados con la OMA). En 2022 hay tantos complejos porque
los residuos electrónicos (85.49) y los módulos de pantallas (85.24) pueden venir de casi cualquier
máquina o aparato, y la OMA lo registra así. Marzo 2019 no tiene versión descargada en SAREM: sus
códigos se arman desde enero 2019 con la tabla de correlación. "2022" es la carpeta "49. 2022" de
SAREM (mismos códigos que setiembre 2021). Agosto 2016 abre 14 códigos que setiembre 2016 vuelve
a juntar: julio y setiembre 2016 tienen los mismos códigos.

**Controles.**
1. En las 62 tablas, cada código que desaparece tiene destino y cada código que aparece tiene origen.
2. La cadena armada paso a paso se compara con 38 tablas directas de SAREM que cuadran con sus
   versiones: 28 completas y 10 que solo traen los códigos que cambian (control parcial; son las únicas
   que hay para 2019 – 2026). Las diferencias vienen todas de la decisión 5: vínculos agregados por la OMA, vínculos de
   SAREM que la OMA no registra, o tablas de SAREM que no coinciden entre sí en casos que la OMA admite
   en general. 0 diferencias sin explicar (ver la hoja *Resumen* del Excel).
3. **Decisión 2007:** la tabla de SAREM de noviembre 2006 a enero 2007 está incompleta (le faltan 9
   vínculos: pelo fino en los capítulos 61 y 62, y 8517.62.59). Se usa la tabla directa de octubre
   2006 a enero 2007, que tiene los mismos códigos de origen y coincide con las tablas largas.
4. **Decisión 2012:** a la tabla de octubre 2011 a enero 2012 le faltan 19 vínculos hacia la partida
   nueva 96.19 (compresas, tampones y pañales de cualquier materia), desde los capítulos 39, 61, 62 y
   63. Se agregan desde la tabla enero 2011 → enero 2012, y coinciden con las tablas largas.
5. **Las cuatro enmiendas, revisadas con la OMA:** los pasos de enero 2007, 2012, 2017 y 2022 se
   cruzaron con las tablas de correlación oficiales de la OMA (SA 2002 → 2007, 2007 → 2012, 2012 → 2017
   y 2017 → 2022, a 6 dígitos). La OMA da el origen y el destino por subpartida, o por partida o
   capítulo cuando escribe "subpartidas aplicables, en particular de las partidas o capítulos...". Regla:
   - cambios dentro de una misma subpartida de 6 dígitos: tal cual vienen de SAREM;
   - cambios entre subpartidas que la OMA registra y le faltan a SAREM: se agregan desde una tabla
     larga de SAREM, o para toda la subpartida si ninguna tabla los trae. Agregados: 2007, 1.088 (por
     ejemplo 84.86, máquinas para fabricar semiconductores, desde máquinas herramienta); 2012, 930;
     2017, 547 (despojos de pescado hacia 0302.99/0303.99 y circuitos integrados 85.42); 2022, 320;
   - vínculos de SAREM que la OMA no registra: en 2007, 2012 y 2017 se mantienen marcados (134, 36 y
     6); en 2022 no se usan (8, en `datos/vinculos_sarem_no_usados.csv`), salvo que un código quede sin
     destino o un destino sin origen (18, marcados).
   Cada vínculo agregado o marcado tiene su nota. "Para toda la subpartida" es lo menos preciso: el
   código puede quedar con varios destinos posibles y hay que mirar la descripción.

   Las diferencias entre SAREM y la OMA pueden ser decisiones del MERCOSUR (Comité Técnico N.° 1) y no
   errores. Si se consiguen las actas, las notas de esos vínculos se pueden ajustar.

## Inicio rápido

Se necesita Python 3.10+ con `openpyxl`, y `pdftotext` (poppler) para la tabla de la OMA. Primero
se bajan los zip de las releases y los PDF de la OMA, y se guardan en `originales/` (ver
[originales/LEEME.md](originales/LEEME.md)).

```bash
python python/leer_versiones.py originales/nomenclaturas datos/versiones.json
python python/leer_oma.py originales/oma datos
python python/encadenar.py datos/versiones.json originales/correlaciones datos/cadena.json datos
python python/exportar_csv.py datos/versiones.json datos/cadena.json datos
python python/excel_mapeo.py datos/versiones.json datos/cadena.json salidas/Mapeo_NCM_2002-2026.xlsx
```

| Carpeta | Contenido |
|---|---|
| [`originales/`](originales/LEEME.md) | Cómo bajar los archivos de SAREM (van como releases) |
| [`python/`](python/) | Programas |
| [`datos/`](datos/LEEME.md) | Resultados en CSV |
| [`salidas/`](salidas/) | Excel del mapeo |
| [`docs/`](docs/LEEME.md) | Páginas web (por ahora, la de listas de la nomenclatura) |

## Fuente y aviso

**Fuente: Secretaría del MERCOSUR, sistema SAREM.** Este repositorio no está asociado a la
Secretaría del MERCOSUR ni cuenta con su participación o apoyo. Las correlaciones facilitan el
trabajo con distintas versiones de la NCM, pero **no tienen valor legal**: la clasificación de una
mercadería se rige por la nomenclatura y las normas vigentes.

Código bajo licencia MIT. Para citar el repositorio, ver [`CITATION.cff`](CITATION.cff).
