import os
import csv
import requests
import datetime
from utils_supabase import fetch_supabase_data
import dropbox

DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_PATH_MAIN = "/delitos.csv"
DROPBOX_PATH_BACKUP_FOLDER = "/backup"

def export_to_csv(data, csv_path):
    if not data:
        print("No hay datos para exportar.")
        return

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def upload_to_dropbox(local_file_path, dbx_path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open(local_file_path, "rb") as f:
        dbx.files_upload(f.read(), dbx_path, mode=dropbox.files.WriteMode("overwrite"))

def run():
    if datetime.datetime.now().day != 25:
        print("Hoy no es día 25, no se ejecuta.")
        return

    data = fetch_supabase_data()
    if not data:
        print("No se encontraron datos.")
        return

    local_file = "delitos.csv"
    export_to_csv(data, local_file)

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_path = f"{DROPBOX_PATH_BACKUP_FOLDER}/delitos_{today_str}.csv"

    print("Subiendo respaldo a Dropbox...")
    upload_to_dropbox(local_file, backup_path)

    print("Sobrescribiendo archivo principal en Dropbox...")
    upload_to_dropbox(local_file, DROPBOX_PATH_MAIN)

    print("Proceso completado.")

if __name__ == "__main__":
    run()