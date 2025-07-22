import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

def fetch_supabase_data():
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    all_data = []
    page = 0
    page_size = 10000
    while True:
        from_record = page * page_size
        url = f"{SUPABASE_URL}/rest/v1/delitos?select=*&offset={from_record}&limit={page_size}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error al obtener datos: {response.text}")
            break
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        page += 1
    return all_data