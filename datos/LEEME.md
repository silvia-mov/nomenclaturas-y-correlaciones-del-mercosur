# Datos

Resultados generados con los programas de [`python/`](../python/). Fuente: SAREM (MERCOSUR).

| Archivo | Contenido |
|---|---|
| `versiones.csv` | Las 63 versiones de la NCM, 2002–2026: año, mes y cantidad de códigos de 8 dígitos |
| `mapeo_2002_2026.csv` | Para cada código y período de validez, su código (o códigos) en la NCM de noviembre 2026. Una fila por destino |
| `caminos_2002_2026.csv` | Para cada código y período que cambia: descripción, destinos, camino y notas |
| `cambios_por_paso_2002_2026.csv` | Solo los códigos que cambiaron en cada paso entre versiones seguidas |
| `vinculos_sarem_no_usados.csv` | Vínculos de las tablas de SAREM que no se usan en la cadena, con su motivo |

## Listas de la nomenclatura (`datos/listas/`)

| Archivo | Contenido |
|---|---|
| `listas_notificadas.csv` | Una fila por lista (BK, BIT, LNE, RMP), notificación y código: arancel nacional vigente, versión de la NCM de esa fecha, tipo de cambio y códigos en la NCM vigente |
| `listas_resumen.csv` | Cantidad de códigos de cada lista en cada notificación |
| `ncm_2026_11.csv` | La NCM vigente (noviembre 2026): código, descripción y AEC |

En `listas_notificadas.csv`, la columna `aviso` indica cuando el código no existe en la versión de la NCM
de la fecha de la notificación (por ejemplo, la de enero 2022 todavía usa códigos de la NCM 2017): en
ese caso se tradujo desde la versión más cercana en la que existe. En el régimen de materias primas el
arancel es 0 % dentro del régimen.

## Columnas de `mapeo_2002_2026.csv`

| Columna | Qué es |
|---|---|
| `codigo` | Código NCM de 8 dígitos, sin puntos |
| `valido_desde`, `valido_hasta` | Versiones (por ejemplo `NCM_2002_1` = enero 2002) entre las que el código llega a los mismos destinos |
| `tipo_cambio` | igual, renumerado, se divide, se fusiona, complejo |
| `codigo_final` | Código de destino en la última versión de la cadena (una fila por destino) |
| `version_final` | Última versión de la cadena (hoy `NCM_2026_11`, noviembre 2026) |
| `n_destinos` | Cuántos destinos tiene el código |
| `con_notas` | "sí" si el camino usa vínculos agregados o sin respaldo de la OMA (el detalle está en `caminos_2002_2026.csv`) |

`caminos_2002_2026.csv` repite `codigo`, `valido_desde`, `valido_hasta` y `tipo_cambio`, y agrega la
descripción, los destinos, el camino (en qué paso cambió y cómo) y las notas. Solo trae los códigos que
cambian.

Los archivos `datos/*.json` son intermedios y no se publican: se regeneran con los programas. Entre
ellos, `oma_2012_2017.json` y `oma_2017_2022.json` (las tablas de la OMA leídas por `python/leer_oma.py`).
