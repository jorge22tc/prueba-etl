import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import json
import uuid

# --- 1. Obtener las variables de entorno ---
# Las variables de entorno son la forma en que Docker configurará tu script
# Obtienen los valores que te dieron en el correo
WEB_URL = os.environ.get("WEB_URL", "http://52.0.216.22:7080")
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://etl_user:etl_pass123@52.0.216.22:27017/etl_tracker")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://52.0.216.22:7300/api")
PROCESO_DESCRIPCION = os.environ.get("PROCESO_DESCRIPCION", "Extracción contactos empresariales - Empresas Tech")

# Generamos un ID único para este proceso
procesoId = str(uuid.uuid4())

print(f"Iniciando proceso ETL con ID: {procesoId}")
print("--- Extrayendo datos de la página web ---")

# --- 2. Web Scraping (Extracción de datos) ---
try:
    response = requests.get(WEB_URL)
    response.raise_for_status()  # Lanza un error si la petición falla
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        raise ValueError("No se encontró la tabla en la página.")
        
    rows = table.find_all('tr')[1:] # Ignoramos la primera fila (encabezados)
    
    contactos_filtrados = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 6:
            empresa = cols[0].text.strip()
            nombre = cols[1].text.strip()
            apellido = cols[2].text.strip()
            puesto = cols[3].text.strip()
            email = cols[4].text.strip()
            primer_contacto_str = cols[5].text.strip()
            
            # Criterio de filtrado: El nombre de la empresa debe contener "Tech"
            if "Tech" in empresa:
                contacto = {
                    "empresa": empresa,
                    "contacto": {
                        "nombre": nombre,
                        "apellido": apellido,
                        "puesto": puesto,
                        "email": email
                    },
                    "fechaPrimerContacto": datetime.strptime(primer_contacto_str, "%Y-%m-%d"),
                    "fechaInsercion": datetime.now(),
                    "procesoId": procesoId
                }
                contactos_filtrados.append(contacto)

    print(f"Se encontraron {len(contactos_filtrados)} contactos que cumplen el criterio.")
    
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la página web: {e}")
    exit(1)
except Exception as e:
    print(f"Ocurrió un error durante el scraping: {e}")
    exit(1)

# --- 3. Almacenamiento en MongoDB (Carga de datos) ---
try:
    if contactos_filtrados:
        print("--- Conectando a MongoDB para la carga de datos ---")
        client = MongoClient(MONGODB_URI)
        db_name = MONGODB_URI.split('/')[-1] # Extrae el nombre de la base de datos de la URI
        db = client[db_name]
        collection = db.contactos_empresariales
        
        # Inserta los documentos en la colección
        result = collection.insert_many(contactos_filtrados)
        cantidad_insertada = len(result.inserted_ids)
        print(f"Se insertaron {cantidad_insertada} registros en MongoDB.")
    else:
        cantidad_insertada = 0
        print("No hay datos para insertar en MongoDB.")

except Exception as e:
    print(f"Error al insertar en MongoDB: {e}")
    cantidad_insertada = 0
    
finally:
    if 'client' in locals():
        client.close()

# --- 4. Registro en la API (Tracking) ---
print("--- Registrando el proceso ETL en la API ---")
api_url = f"{API_BASE_URL}/etl"
fecha_ejecucion = datetime.now().isoformat()
data_api = {
    "cantidadDatos": cantidad_insertada,
    "fechaEjecucion": fecha_ejecucion,
    "descripcion": PROCESO_DESCRIPCION
}

try:
    headers = {"Content-Type": "application/json"}
    response_api = requests.post(api_url, data=json.dumps(data_api), headers=headers)
    
    if response_api.status_code == 201:
        print("Proceso ETL registrado exitosamente.")
        print("Respuesta de la API:", response_api.json())
    else:
        print(f"Error al registrar en la API. Código de estado: {response_api.status_code}")
        print("Respuesta:", response_api.text)
        
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado al registrar en la API: {e}")

print("Proceso ETL completado.")