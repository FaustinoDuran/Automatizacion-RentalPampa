import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta

# Configuración fija
RUTA_CREDENCIALES = 'alertaservicepampa-171625693505.json'
SHEET_ID = '1lAoXqdCzGE0OQlh9zfuPgwhn7fZptkLGPKJJaksTN84'

# Autenticación (solo una vez)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(RUTA_CREDENCIALES, scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_ID)

def cargar_hoja(nombre_hoja, columnas_deseadas=None):
    """
    Carga una hoja específica del Google Sheet y devuelve un DataFrame limpio.
    - nombre_hoja: nombre de la pestaña (hoja) dentro del archivo.
    - columnas_deseadas: lista de columnas que querés mostrar (opcional).
    """
    worksheet = spreadsheet.worksheet(nombre_hoja)
    values = worksheet.get_all_values()

    # Encabezados reales están en la fila 3 (índice 2)
    headers_raw = values[2]
    headers = []
    for h in headers_raw:
        h_clean = h.strip()
        while h_clean in headers:
            h_clean += "_1"
        headers.append(h_clean)

    # Filas de datos desde la fila 4 en adelante
    rows = values[3:]

    # Filtrar filas vacías
    filtered_rows = [row for row in rows if any(cell.strip() != '' for cell in row)]

    # Crear DataFrame
    df = pd.DataFrame(filtered_rows, columns=headers)

    # Mostrar columnas deseadas si existen
    if columnas_deseadas:
        columnas_existentes = [col for col in columnas_deseadas if col in df.columns]
        
        print("\n")
        return df[columnas_existentes]
    else:
        return df.head()

    


def obtener_registro_alertas():
    try:
        hoja_registro = spreadsheet.worksheet("REGISTRO_ALERTAS")
        datos = hoja_registro.get_all_records()
        return datos  # como lista de dicts
    except gspread.exceptions.WorksheetNotFound:
        spreadsheet.add_worksheet(title="REGISTRO_ALERTAS", rows=1000, cols=5)  #AUMENTAR EN UN FUTURO PORQUE SE VA A COLAPSAR
        return []

def registrar_alerta(tipo, identificador, detalle_extra=""):
    hoja = spreadsheet.worksheet("REGISTRO_ALERTAS")
    hoy = datetime.today().strftime('%Y-%m-%d')
    hoja.append_row([hoy, tipo, identificador, detalle_extra])


def alerta_ya_enviada(registro, tipo, identificador):
    for fila in registro:
        if fila['TIPO ALERTA'] == tipo and fila['IDENTIFICADOR'] == identificador:
            return True
    return False




