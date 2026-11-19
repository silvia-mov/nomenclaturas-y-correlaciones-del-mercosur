# Datos

Resultados generados con los programas de [`python/`](../python/). Fuente: SAREM (MERCOSUR).

| Archivo | Contenido |
|---|---|
| `versiones.csv` | Las 63 versiones de la NCM, 2002–2026: año, mes y cantidad de códigos de 8 dígitos |
| `mapeo_2002_2010.csv` | Para cada código y período de validez, su código (o códigos) en la NCM de enero 2010 |
| `cambios_por_paso_2002_2010.csv` | Solo los códigos que cambiaron en cada paso entre versiones seguidas |

## Columnas de `mapeo_2002_2010.csv`

| Columna | Qué es |
|---|---|
| `codigo` | Código NCM de 8 dígitos, sin puntos |
| `valido_desde`, `valido_hasta` | Versiones (por ejemplo `NCM_2002_1` = enero 2002) entre las que el código llega a los mismos destinos |
| `descripcion` | Descripción en la versión `valido_desde` |
| `tipo_cambio` | igual, renumerado, se divide, se fusiona, complejo |
| `codigo_final` | Código de destino en la última versión de la cadena (una fila por destino) |
| `descripcion_final` | Descripción del destino |
| `version_final` | Última versión de la cadena (hoy `NCM_2010_1`, enero 2010) |
| `n_destinos` | Cuántos destinos tiene el código |
| `camino` | En qué paso cambió y cómo |

Los archivos `datos/*.json` son intermedios grandes y no se publican: se regeneran con los programas.
