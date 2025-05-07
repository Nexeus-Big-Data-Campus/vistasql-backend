FROM python:3.11-slim

WORKDIR /app

# Instalar netcat y dependencias de compilación para bcrypt
# netcat-openbsd: Proporciona la utilidad nc (netcat) para el script de espera.
# build-essential: Meta-paquete que incluye herramientas de compilación esenciales (gcc, make, etc.)
# libffi-dev: Necesaria para algunas librerías criptográficas como las que usa python-jose o passlib
RUN apt-get update && \
    apt-get install -y netcat-openbsd build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt e instalar las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Copiar el script de espera y darle permisos de ejecución
# Asegúrate de tener el archivo wait-for-it.sh en la raíz de tu proyecto backend
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Usar el script de espera para asegurarse de que la base de datos esté lista
# antes de iniciar la aplicación FastAPI con uvicorn.
# El script espera en el host 'db' (el nombre del servicio de base de datos en docker-compose)
# en el puerto 5432, y luego ejecuta el comando para iniciar la aplicación.
CMD ["/app/wait-for-it.sh", "db", "5432", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
