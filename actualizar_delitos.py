import os
import pandas as pd
import requests
from io import StringIO
from datetime import datetime
from supabase import create_client

# Supabase credentials
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

# Obtener fecha actual
today = datetime.now()

# Validar si es día 23 o posterior
if today.day < 23:
    print("⏳ Aún no es 23 del mes. El script se detiene sin actualizar.")
    exit()

# Calcular el mes anterior
if today.month == 1:
    year = today.year - 1
    period = 12
else:
    year = today.year
    period = today.month - 1

# Construir URL del CSV
CSV_URL = (
    f"https://delitosmexico.onc.org.mx/v1.0/export/csv?"
    f"delito=0&year={year}&period={period}&inegiEntidad=0&inegiMunicipality=0&group=month&search="
)

print(f"📥 Descargando CSV del año {year}, mes {period}...")

# Descargar datos
response = requests.get(CSV_URL)
response.raise_for_status()

# Leer CSV en DataFrame
df = pd.read_csv(StringIO(response.text))
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Convertir columna 'fecha' a datetime
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
df = df.dropna(subset=['fecha'])

# Conectar a Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Eliminar registros existentes de las fechas nuevas
fechas = df['fecha'].dropna().dt.normalize().unique()
print(f"🧹 Eliminando fechas duplicadas: {fechas}")

for f in fechas:
    supabase.table("delitos").delete().eq("fecha", f.isoformat()).execute()

# Preparar e insertar nuevos datos
print("🆕 Insertando nuevos registros...")
data = df.copy()
data["fecha"] = data["fecha"].dt.strftime("%Y-%m-%dT%H:%M:%S")  # JSON serializable
data = data.to_dict(orient="records")

for i in range(0, len(data), 1000):
    supabase.table("delitos").insert(data[i:i + 1000]).execute()

print("✅ Base Supabase actualizada correctamente.")

