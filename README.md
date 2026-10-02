# CFDI Viáticos Parser

Herramienta modular en Python para automatizar la extracción de datos fiscales desde comprobantes digitales (CFDI 3.3 y 4.0 en formato XML) emitidos por el SAT y consolidarlos directamente en reportes tabulares de Excel (`.xlsx`).

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración de Variables de Entorno](#-configuración-de-variables-de-entorno)
- [Modo de Uso](#-modo-de-uso)
- [Procedimiento de Pruebas](#-procedimiento-de-pruebas)
- [Campos Extraídos](#-campos-extraídos)
- [Manejo de Errores Comunes](#-manejo-de-errores-comunes)
- [Licencia](#-licencia)

---

## 🚀 Características

- **Soporte Multi-Versión:** Compatible con comprobantes fiscales digitales por internet bajo los esquemas SAT CFDI 3.3 y CFDI 4.0.
- **Configuración desacoplada:** Administrado mediante variables de entorno (`.env`) sin exponer rutas ni credenciales.
- **Portabilidad y modularidad:** Separación de responsabilidades entre el orquestador (`main.py`), lógica de parsing (`parsers/`) y generación de reportes (`exporters/`).
- **Formateo automático:** Exportación a Excel con ajuste automático del ancho de columnas para lectura inmediata.
- **Apto para control de versiones:** Archivo `.gitignore` preconfigurado para evitar subir datos sensibles o archivos XML a repositorios públicos.

---

## 📂 Estructura del Proyecto

```text
viaticos-parser/
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Reglas de exclusión para Git
├── README.md                 # Documentación técnica
├── requirements.txt          # Dependencias del proyecto
├── config.py                 # Módulo centralizador de configuración
├── main.py                   # Script principal orquestador
├── parsers/
│   ├── __init__.py
│   └── cfdi_parser.py        # Extractor y resolución de namespaces SAT
├── exporters/
│   ├── __init__.py
│   └── excel_exporter.py     # Generador de reportes en Excel
├── input_xml/                # Directorio de entrada para comprobantes XML
└── output/                   # Directorio donde se guardan los reportes
```

---

## 🛠 Requisitos Previos

- **Python** `>= 3.9`
- Gestor de paquetes **pip**
- Herramienta de control de versiones **git**

---

## 💻 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/viaticos-parser.git
   cd viaticos-parser
   ```

2. **Crear y activar un entorno virtual (`venv`):**
   - En **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - En **Windows** (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

3. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuración de Variables de Entorno

El proyecto incluye una plantilla `.env.example`. Copia esta plantilla para crear tu propio archivo `.env` local:

```bash
cp .env.example .env
```

Edita `.env` para ajustar las rutas y nombres de archivo según tus necesidades:

```ini
# Directorio donde colocarás los comprobantes XML a procesar
INPUT_DIR=input_xml

# Directorio donde se depositará el archivo consolidado
OUTPUT_DIR=output

# Nombre del archivo Excel generado
OUTPUT_FILENAME=reporte_viaticos.xlsx
```

> **Nota:** Cualquier modificación en `.env` surtirá efecto inmediatamente en la siguiente ejecución del script sin necesidad de reiniciar la terminal.

---

## 🏃 Modo de Uso

1. **Depositar los archivos:**
   Copia todos los archivos XML correspondientes a tus viáticos dentro de la carpeta designada (por defecto `input_xml/`).

2. **Ejecutar el procesador:**
   ```bash
   python main.py
   ```

3. **Consultar resultados:**
   Una vez concluido el procesamiento, el reporte generado estará disponible en la carpeta de salida (por defecto `output/reporte_viaticos.xlsx`).

---

## 🧪 Procedimiento de Pruebas

Para verificar que el entorno y los componentes funcionan correctamente antes de procesar archivos de producción, sigue estos pasos:

### 1. Prueba de Verificación de Entorno
Comprueba que las librerías necesarias estén instaladas en el entorno virtual activo:

```bash
python -c "import pandas, openpyxl, dotenv; print('[OK] Todas las dependencias están disponibles')"
```

### 2. Prueba con XML Mock (Prueba Funcional)
Crea un archivo XML sintético de prueba para comprobar la extracción y generación del reporte:

```bash
cat << 'EOF' > input_xml/test_cfdi.xml
<?xml version="1.0" encoding="utf-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" Version="4.0" Serie="TEST" Folio="999" Fecha="2026-01-15T12:00:00" SubTotal="100.00" Total="116.00" Moneda="MXN">
  <cfdi:Emisor Rfc="AAA010101AAA" Nombre="EMPRESA DE PRUEBA SA DE CV" />
  <cfdi:Receptor Rfc="XAXX010101000" />
  <cfdi:Complemento>
    <tfd:TimbreFiscalDigital UUID="AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE" />
  </cfdi:Complemento>
</cfdi:Comprobante>
EOF
```

Ejecuta el script:
```bash
python main.py
```

**Resultado esperado en consola:**
```text
[*] Procesando 1 comprobantes XML...
[✓] Archivo generado exitosamente en: /tu-ruta/viaticos-parser/output/reporte_viaticos.xlsx
```

Al abrir `output/reporte_viaticos.xlsx`, valida que la fila contenga los datos del comprobante de prueba. Una vez finalizada la prueba, elimina el archivo temporal:
```bash
rm input_xml/test_cfdi.xml
```

---

## 📊 Campos Extraídos

El extractor procesa y mapea de manera estándar los siguientes datos por cada comprobante:

| Columna | Campo XML / SAT | Descripción |
| :--- | :--- | :--- |
| **Archivo** | Nombre del archivo | Nombre del fichero `.xml` de origen |
| **RFC Emisor** | `cfdi:Emisor/@Rfc` | Clave RFC del proveedor o establecimiento |
| **Nombre Emisor** | `cfdi:Emisor/@Nombre` | Razón social o nombre del emisor |
| **RFC Receptor** | `cfdi:Receptor/@Rfc` | RFC al que fue facturado el gasto |
| **Serie** | `cfdi:Comprobante/@Serie` | Serie interna de control |
| **Folio** | `cfdi:Comprobante/@Folio` | Número de folio asignado por el emisor |
| **Folio Fiscal (UUID)** | `tfd:TimbreFiscalDigital/@UUID` | Identificador fiscal universal (36 caracteres) |
| **Fecha** | `cfdi:Comprobante/@Fecha` | Fecha y hora de emisión del comprobante |
| **Moneda** | `cfdi:Comprobante/@Moneda` | Divisa (MXN, USD, EUR, etc.) |
| **SubTotal** | `cfdi:Comprobante/@SubTotal` | Monto antes de impuestos y descuentos |
| **Total** | `cfdi:Comprobante/@Total` | Importe total liquidado de la factura |

---

## ⚠️ Manejo de Errores Comunes

- **`[!] No se encontraron archivos XML en: ...`**: Verifica que colocaste los archivos directamente en la carpeta configurada en `INPUT_DIR` (por defecto `input_xml/`) y que tengan extensión `.xml` en minúsculas.
- **`[!] Error al parsear XML malformado`**: El archivo correspondiente está incompleto, corrupto o no cumple la sintaxis XML estándar. El script lo omitirá sin detener el procesamiento de los demás comprobantes.
- **Permiso denegado al escribir el archivo Excel**: Cierra el archivo `reporte_viaticos.xlsx` en Microsoft Excel o LibreOffice antes de volver a ejecutar el script, ya que los programas ofimáticos bloquean el archivo contra escritura.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
