# Prueba Técnica - Desarrollador ETL/Data Engineer

## Descripción de la Solución
Este proyecto es una solución ETL (Extraer, Transformar, Cargar) automatizada para la prueba técnica de Blautech. El script realiza las siguientes funciones:
1.  **Web Scraping:** Extrae datos de contactos empresariales desde la URL proporcionada: http://52.0.216.22:7080.
2.  **Filtrado:** Procesa solo las empresas cuyo nombre contiene la palabra "Tech".
3.  **Almacenamiento:** Inserta los datos filtrados en la base de datos MongoDB especificada.
4.  **Registro:** Reporta el éxito del proceso ETL a la API de seguimiento.
La solución está completamente containerizada usando Docker para una fácil ejecución y portabilidad.

## Requisitos Previos
-   [Docker](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
-   [Git](https://git-scm.com/downloads) instalado.

## Instrucciones de Uso
1.  Clona o descarga este repositorio.
2.  Abre una terminal y navega a la carpeta raíz del proyecto.
3.  Construye la imagen de Docker con el siguiente comando:
    ```bash
    docker build -t etl-scraper .
    ```
4.  Ejecuta el contenedor. Las variables de entorno ya están configuradas en el Dockerfile, pero se pueden sobrescribir al ejecutar el comando `docker run`.
    ```bash
    docker run --rm etl-scraper
    ```
5.  Al finalizar, el contenedor se detendrá y habrás completado el proceso.

## Variables de Entorno (Configurables)
-   `WEB_URL`: URL de la página web a scrapear.
-   `MONGODB_URI`: Cadena de conexión a la base de datos MongoDB.
-   `API_BASE_URL`: URL base para la API de registro de procesos.
-   `PROCESO_DESCRIPCION`: Descripción del proceso ETL para el registro.