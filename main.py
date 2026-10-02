from config import INPUT_DIR, OUTPUT_DIR, OUTPUT_FILENAME
from parsers.cfdi_parser import CFDIParser
from exporters.excel_exporter import ExcelExporter

def run() -> None:
    xml_files = list(INPUT_DIR.glob("*.xml"))
    if not xml_files:
        print(f"[!] No se encontraron archivos XML en: {INPUT_DIR}")
        return

    print(f"[*] Procesando {len(xml_files)} comprobantes XML...")
    parsed_records = []

    for xml_file in xml_files:
        record = CFDIParser.parse(xml_file)
        if record:
            parsed_records.append(record)

    output_path = OUTPUT_DIR / OUTPUT_FILENAME
    ExcelExporter.export(parsed_records, output_path)

if __name__ == "__main__":
    run()
