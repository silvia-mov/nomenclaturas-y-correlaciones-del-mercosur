# Versiones

## Sin publicar

- **Enmiendas 2007 y 2012 revisadas con la OMA:** `leer_oma.py` lee también las tablas SA 2002 → 2007
  y 2007 → 2012, y el texto "subpartidas aplicables de..." del lado del destino. Se aplica la misma
  regla que en 2017: se agregan los cambios que la OMA registra y le faltan a SAREM (1.088 en 2007,
  930 en 2012) y se marcan los vínculos de SAREM sin respaldo (134 y 36).
- Los controles explican cada diferencia con la cadena armada solo con SAREM (0 sin explicar).
- `mapeo_2002_2022.csv` se divide en dos archivos (`mapeo_` y `caminos_`) para que no pese 47 MB.
- **Tramo 5, marzo 2019 – enero 2022** (incluye la VII Enmienda del SA): la cadena llega a enero 2022
  (`datos/mapeo_2002_2022.csv`, `salidas/Mapeo_NCM_2002-2022.xlsx`). Marzo 2019 se arma con la tabla de
  SAREM porque no tiene versión descargada. El paso a enero 2022 se revisa con la OMA (SA 2017 → 2022):
  los vínculos que la OMA no registra no se usan y van a `datos/vinculos_sarem_no_usados.csv`.
- **Corrección:** `leer_oma.py` ahora lee las entradas de la OMA escritas en texto ("subpartidas
  aplicables, en particular de las partidas o capítulos..."). Con eso cambia el paso a enero 2017: los
  vínculos hacia circuitos integrados (85.42) y desde 29.33/29.34 hacia 2939.80 sí tienen respaldo de
  la OMA (sin respaldo quedan 6, antes 42).
- **Tramo 4, julio 2015 – enero 2019** (incluye la VI Enmienda del SA): la cadena llega a enero 2019
  (`datos/mapeo_2002_2019.csv`, `salidas/Mapeo_NCM_2002-2019.xlsx`). El paso a enero 2017 se revisa
  contra la tabla de correlación de la OMA (`python/leer_oma.py`): se agregan los cambios que la OMA
  registra y faltaban, y se marcan los vínculos de SAREM que la OMA no respalda. Nueva columna de
  notas. Los controles separan las diferencias explicadas de las sin explicar (0 sin explicar).
- **Tramo 3, octubre 2010 – enero 2015** (incluye la V Enmienda del SA): la cadena llega a enero 2015
  (`datos/mapeo_2002_2015.csv`, `salidas/Mapeo_NCM_2002-2015.xlsx`). A octubre 2011 → enero 2012 se
  le agregan 19 vínculos hacia 9619.00.00 que faltan en SAREM. 21 controles, 0 diferencias.
- **Tramo 2, noviembre 2006 – enero 2010** (incluye la IV Enmienda del SA): la cadena llega ahora a
  enero 2010 (`datos/mapeo_2002_2010.csv`, `salidas/Mapeo_NCM_2002-2010.xlsx`). Aparece el tipo
  *renumerado*. Controles contra 12 tablas directas de SAREM, 0 diferencias. Para noviembre 2006 →
  enero 2007 se usa la tabla de octubre 2006, porque la de noviembre está incompleta.
- `python/encadenar.py` toma la versión final de la cadena y encuentra solo las tablas de SAREM que sirven de control.
- **Tramo 1, enero 2002 – octubre 2006** (`python/encadenar.py`, `datos/mapeo_2002_2006.csv`,
  `salidas/Mapeo_NCM_2002-2006.xlsx`): 12 versiones de la NCM y 10 tablas de correlación de SAREM
  entre versiones seguidas, encadenadas hasta octubre 2006. Control: la cadena coincide exactamente
  con las tablas directas de SAREM desde enero 2002 hasta enero 2003, julio 2003, enero 2004 y
  julio 2004.
- **Lectura de las 63 versiones de la NCM, 2002–2026** (`python/leer_versiones.py`,
  `datos/versiones.csv`).
