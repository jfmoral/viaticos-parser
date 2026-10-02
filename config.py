import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / os.getenv("INPUT_DIR", "input_xml")
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "resumen_viaticos.xlsx")

# Asegurar que las carpetas existan en tiempo de ejecución
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
