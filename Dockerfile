# Usa una imagen oficial de Python como base
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instala las librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script principal al contenedor
COPY main.py .

# Define las variables de entorno para que se puedan configurar
ENV WEB_URL="http://52.0.216.22:7080"
ENV MONGODB_URI="mongodb://etl_user:etl_pass123@52.0.216.22:27017/etl_tracker"
ENV API_BASE_URL="http://52.0.216.22:7300/api"
ENV PROCESO_DESCRIPCION="Extracción contactos empresariales - Empresas Tech"

# Comando que se ejecutará al iniciar el contenedor
CMD ["python", "main.py"]