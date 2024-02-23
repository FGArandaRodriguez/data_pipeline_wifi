# Establece la imagen base
FROM python:3.9-slim
ENV FLASK_APP app/__init__.py
ENV FLASK_RUN_HOST 0.0.0.0

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .


# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación Flask al directorio de trabajo
COPY . .

# Expone el puerto que Flask utilizará
EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]

