# Originales de SAREM

Los archivos originales se descargan del **sistema SAREM** de la Secretaría del MERCOSUR y se
publican como **releases** de este repositorio (zip), no dentro del código.

**Fuente: Secretaría del MERCOSUR, SAREM.** Este repositorio no está asociado a la Secretaría del
MERCOSUR ni cuenta con su participación o apoyo.

## Qué hay que descargar

| Release | Zip | Contenido |
|---|---|---|
| `nomenclaturas` | `Sistema.de.descarga.de.nomenclaturas.zip` | Las versiones de la NCM, 2002–2026 (63 archivos `NCM_AAAA_M.xlsx`) |
| `correlaciones` | `1.ENERO.2002.-.JULIO.2006.zip` | Tablas de enero 2002 a julio 2006 (36 tablas) |
| `correlaciones` | `2.OCTUBRE.2006.-.ENERO.2010.zip` | Octubre 2006 a enero 2010 (57 tablas) |
| `correlaciones` | `3.OCTUBRE.2010.-.ENERO.2015.zip` | Octubre 2010 a enero 2015 (38 tablas) |
| `correlaciones` | `4.JULIO.2015.-.ENERO.2019.zip` | Julio 2015 a enero 2019 (33 tablas) |
| `correlaciones` | `5.MARZO.2019.-.ENERO.2022.zip` | Marzo 2019 a enero 2022 (24 tablas) |
| `correlaciones` | `6.JULIO.2022.-.OCTUBRE.2025.zip` | Julio 2022 a octubre 2025 (21 tablas) |
| `correlaciones` | `7.ENERO.2026.-.OCTUBRE.2026.zip` | Enero 2026 a octubre 2026 (6 tablas) |

Las correlaciones vienen en 63 carpetas, una por versión de la NCM. En cada carpeta hay una tabla
hacia la versión siguiente: la cadena está completa de enero 2002 a octubre 2026. Dos nombres de
carpeta no coinciden con la fecha: "49. 2022" es la versión `NCM_2022` (SAREM `NCM_201760`) y
"62. FEBRERO 2023" es en realidad **febrero 2026** (`NCM_2026_2`, SAREM `NCM_202250`).

## Tabla de correlación de la OMA

Para el paso a enero 2017 (VI Enmienda del SA) se usa la tabla oficial de la Organización Mundial de
Aduanas, **SA 2012 → SA 2017** (Tabla II de octubre 2016 y su anexo del capítulo 44). No se publica
aquí: se baja de la página de la OMA (*Correlation Tables HS 2012 – 2017*) y se guarda en
`originales/oma/`:

```
originales/oma/
├── table_ii_trp1217_en_rev1.pdf
└── table_ii_a_trp1217_en.pdf
```

Según la propia OMA, estas tablas son una guía y no tienen valor legal.

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
- Las tablas de enero 2007 hacia enero 2006 y julio 2006 usan del lado de 2007 los códigos de
  **julio 2007** (11 códigos que no existían en enero 2007) y tienen filas `suprimido` y `eliminado`.
- La tabla `NCM_200259_NCM_200701` (noviembre 2006 → enero 2007) está **incompleta**: le faltan 9
  vínculos que sí están en `NCM_200258_NCM_200701` (octubre 2006 → enero 2007) y en las tablas desde
  enero 2002. Se usa la de octubre.
- La tabla `NCM_200758_NCM_201201` (octubre 2011 → enero 2012) está **incompleta**: le faltan 19
  vínculos hacia `96190000` (capítulos 39, 61, 62 y 63) que sí están en `NCM_200749_NCM_201201`
  (enero 2011 → enero 2012) y en las tablas largas. Se agregan desde esa tabla.
- Las tablas largas entre enero 2002 y julio 2018 (`NCM_200201_NCM_201719` y la inversa) dicen
  `01012101`, que no existe, en lugar de `01012100`. Se corrige al leerlas.
- Las tablas largas desde julio 2007 (`NCM_200707_NCM_201249` y `NCM_200707_NCM_201701`) unen entre sí
  códigos hermanos creados en julio 2007 (por ejemplo 8431.49.21 "Cabinas" con 8431.49.22 "Orugas").
  No se usan como control.
- Para la VI Enmienda (setiembre 2016 → enero 2017), la tabla corta y las tablas largas no coinciden
  entre sí, y ninguna coincide del todo con la OMA. Ver el README, decisión 5.
