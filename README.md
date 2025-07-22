# Flujo: Exportar datos de Supabase a Dropbox

Este flujo exporta todos los datos de la tabla `delitos` de Supabase a un archivo CSV y lo sube a Dropbox. También guarda una copia de respaldo con la fecha.

## Requisitos

1. Variables de entorno en GitHub:
   - `SUPABASE_URL`
   - `SUPABASE_API_KEY`
   - `DROPBOX_ACCESS_TOKEN`

2. Agrega este flujo a tu repositorio GitHub en `.github/workflows/dropbox_export.yml`.

3. Se ejecuta automáticamente el **día 25 de cada mes**.

---

## Archivos

- `exportar_supabase_a_dropbox.py`: Script principal de exportación.
- `utils_supabase.py`: Funciones auxiliares para Supabase.
- `requirements_dropbox.txt`: Dependencias del flujo.
- `.github/workflows/dropbox_export.yml`: Configuración de GitHub Actions.