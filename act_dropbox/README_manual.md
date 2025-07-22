# Exportación manual de Supabase a Dropbox

Este flujo permite ejecutar manualmente la exportación completa de la base de datos Supabase a un archivo CSV en Dropbox sin importar la fecha.

## Archivos
- `exportar_supabase_a_dropbox_manual.py`: Script principal de exportación.
- `utils_supabase.py`: Función para extraer datos de Supabase (ya existente).
- `requirements_dropbox.txt`: Dependencias necesarias (ya existente).
- `manual_dropbox_export.yml`: Flujo de GitHub Actions para ejecución manual.