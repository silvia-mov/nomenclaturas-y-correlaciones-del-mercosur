# Datos

Resultados generados con los programas de [`python/`](../python/). Fuente: SAREM (MERCOSUR).

| Archivo | Contenido |
|---|---|
| `versiones.csv` | Las 63 versiones de la NCM, 2002–2026: año, mes y cantidad de códigos de 8 dígitos |
| `mapeo_2002_2022.csv` | Para cada código y período de validez, su código (o códigos) en la NCM de enero 2022 |
| `cambios_por_paso_2002_2022.csv` | Solo los códigos que cambiaron en cada paso entre versiones seguidas |
| `vinculos_sarem_no_usados.csv` | Vínculos de las tablas de SAREM que no se usan en la cadena, con su motivo |

## Columnas de `mapeo_2002_2022.csv`

| Columna | Qué es |
|---|---|
| `codigo` | Código NCM de 8 dígitos, sin puntos |
| `valido_desde`, `valido_hasta` | Versiones (por ejemplo `NCM_2002_1` = enero 2002) entre las que el código llega a los mismos destinos |
| `descripcion` | Descripción en la versión `valido_desde` |
| `tipo_cambio` | igual, renumerado, se divide, se fusiona, complejo |
| `codigo_final` | Código de destino en la última versión de la cadena (una fila por destino) |
| `descripcion_final` | Descripción del destino |
| `version_final` | Última versión de la cadena (hoy `NCM_2022_1`, enero 2022) |
| `n_destinos` | Cuántos destinos tiene el código |
| `camino` | En qué paso cambió y cómo |
| `notas` | Vínculos del camino que se agregaron o que la OMA no respalda (ver el README, decisiones 4 y 5) |

Los archivos `datos/*.json` son intermedios y no se publican: se regeneran con los programas. Entre
ellos, `oma_2012_2017.json` y `oma_2017_2022.json` (las tablas de la OMA leídas por `python/leer_oma.py`).
