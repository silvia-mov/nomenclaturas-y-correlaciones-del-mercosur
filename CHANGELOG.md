# Versiones

## Sin publicar

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
