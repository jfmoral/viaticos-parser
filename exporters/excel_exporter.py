import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class ExcelExporter:
    @staticmethod
    def export(data: List[Dict[str, Any]], destination_path: Path) -> None:
        if not data:
            print("[!] No se extrajeron datos para exportar.")
            return

        df = pd.DataFrame(data)

        with pd.ExcelWriter(destination_path, engine="openpyxl") as writer:
            sheet_name = "Comprobacion"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Formato y auto-ajuste de columnas
            worksheet = writer.sheets[sheet_name]
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

        print(f"[✓] Archivo generado exitosamente en: {destination_path}")
