import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, Optional

class CFDIParser:
    NAMESPACES = {
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "cfdi33": "http://www.sat.gob.mx/cfd/3",
        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
    }

    @staticmethod
    def parse(file_path: Path) -> Optional[Dict[str, Any]]:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Atributos generales del comprobante
            total = float(root.attrib.get("Total", 0.0))
            subtotal = float(root.attrib.get("SubTotal", 0.0))
            folio = root.attrib.get("Folio", "S/F")
            serie = root.attrib.get("Serie", "")
            fecha = root.attrib.get("Fecha", "")
            moneda = root.attrib.get("Moneda", "MXN")

            # Emisor
            emisor = root.find("cfdi:Emisor", CFDIParser.NAMESPACES)
            if emisor is None:
                emisor = root.find("cfdi33:Emisor", CFDIParser.NAMESPACES)
            
            rfc_emisor = emisor.attrib.get("Rfc", "N/A") if emisor is not None else "N/A"
            nombre_emisor = emisor.attrib.get("Nombre", "N/A") if emisor is not None else "N/A"

            # Receptor
            receptor = root.find("cfdi:Receptor", CFDIParser.NAMESPACES)
            if receptor is None:
                receptor = root.find("cfdi33:Receptor", CFDIParser.NAMESPACES)
            
            rfc_receptor = receptor.attrib.get("Rfc", "N/A") if receptor is not None else "N/A"

            # UUID (Timbre Fiscal Digital en Complemento)
            uuid = "N/A"
            tfd = root.find(".//tfd:TimbreFiscalDigital", CFDIParser.NAMESPACES)
            if tfd is not None:
                uuid = tfd.attrib.get("UUID", "N/A")

            return {
                "Archivo": file_path.name,
                "RFC Emisor": rfc_emisor,
                "Nombre Emisor": nombre_emisor,
                "RFC Receptor": rfc_receptor,
                "Serie": serie,
                "Folio": folio,
                "Folio Fiscal (UUID)": uuid,
                "Fecha": fecha,
                "Moneda": moneda,
                "SubTotal": subtotal,
                "Total": total
            }
        except ET.ParseError:
            print(f"[!] Error al parsear XML malformado: {file_path.name}")
            return None
        except Exception as e:
            print(f"[!] Error inesperado en {file_path.name}: {e}")
            return None
