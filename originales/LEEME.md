# Originales de SAREM

Los archivos originales se descargan del **sistema SAREM** de la Secretaría del MERCOSUR y se
publican como **releases** de este repositorio (zip), no dentro del código.

**Fuente: Secretaría del MERCOSUR, SAREM.** Este repositorio no está asociado a la Secretaría del
MERCOSUR ni cuenta con su participación o apoyo.

## Qué hay que descargar

| Release | Zip | Contenido |
|---|---|---|
| `nomenclaturas` | `Sistema.de.descarga.de.nomenclaturas.zip` | Las versiones de la NCM, 2002–2026 (63 archivos `NCM_AAAA_M.xlsx`) |
| `correlaciones` | `1.ENERO.2002.-.JULIO.2006.zip` | Tablas de correlación de enero 2002 a julio 2006 |

Los tramos siguientes de correlaciones (desde 2007) se agregan como zip nuevos en la release
`correlaciones`.

## Formato

- **Versiones** (`NCM_AAAA_M.xlsx`): título, fecha de generación, y una fila por código (capítulo,
  partida, subpartida, ítem y código de 8 dígitos) con descripción en español y portugués, AEC y
  familia.
- **Correlaciones** (`NCM_XXXXXX_NCM_YYYYYY.xlsx`): tres columnas, código viejo, marca `ex` y código
  nuevo. Los números `NCM_XXXXXX` son internos de SAREM (por ejemplo `NCM_200213` = enero 2003).
  Algunas tablas traen todos los códigos y otras solo los que cambian.

## Cómo preparar la carpeta

```
originales/
├── nomenclaturas/   los 63 NCM_AAAA_M.xlsx (sin subcarpeta)
└── correlaciones/   las carpetas del zip tal cual ("1. ENERO 2002/", "2. JULIO 2002/", ...)
```

## Problemas encontrados en SAREM

- Las tablas `NCM_200213_NCM_200225` y la inversa dicen ser de enero 2004, pero sus códigos son los
  de **enero 2005**. No se usan.
- Las tablas de enero 2006 y de julio 2006 hacia enero 2007 parten en realidad de **octubre 2006** y
  tienen filas `suprimido` y `eliminado`.
