import os
import pandas as pd
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

CSV_FILE = "concentradogeneral.csv"
TABLE = "delitos"
CHUNK_SIZE = 1000

def cargar_csv_en_supabase():
    df = pd.read_csv(CSV_FILE)

    columnas_esperadas = {
        "inegi_entidad", "entidad", "inegi_municipio", "municipio",
        "id_delito", "delito", "carpetas", "tasa", "fecha"
    }
    if not columnas_esperadas.issubset(set(df.columns)):
        raise Exception("Columnas incorrectas en el CSV.")

    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    url = f"{SUPABASE_URL}/rest/v1/{TABLE}"

    for i in range(0, len(df), CHUNK_SIZE):
        chunk = df.iloc[i:i + CHUNK_SIZE]
        json_data = chunk.to_dict(orient="records")
        response = requests.post(url, json=json_data, headers=headers)
        if not response.ok:
            raise Exception(f"Error en carga Supabase: {response.text}")
        print(f"Subidos {i + len(chunk)} registros...")

    print("✅ Carga completa a Supabase.")

if __name__ == "__main__":
    cargar_csv_en_supabase()
