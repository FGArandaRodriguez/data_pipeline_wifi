# Data Pipeline WiFi

## Descripción General
Este proyecto está diseñado para proporcionar una API robusta para la gestión de datos de puntos de acceso WiFi. 
Incluye un pipeline de datos para cargar los puntos de acceso en una base de datos MongoDB, una API Flask para 
interactuar con los datos e infraestructura de configuraciones para despliegue utilizando Docker y Kubernetes.

## Primeros Pasos

### Requisitos Previos
Debemos de tener instalado lo siguiente:
- Python 3.10+
- pip
- Docker (para ejecución con Docker)
- Un clúster de Kubernetes (para despliegue en Kubernetes)

### Configuración Inicial
1. **Crear un Entorno Virtual**:
```sh
   python -m venv .venv
```
1.- Activar el entorno virtual:
```sh
    En Windows: .venv\Scripts\activate
    En Unix o MacOS: source .venv/bin/activate
```
###Instalar Dependencias:
Después de activar el entorno virtual, instalamos los paquetes requeridos usando:
```sh
  pip install -r requirements.txt
```
2.- Variables de Entorno:
Crea un archivo .env en la raíz del proyecto basado en el archivo .env.example. Debe contener las siguientes variables:

```makefile
FLASK_APP=app/__init__.py
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
MONGO_URI=mongodb+srv://admin:admin@wifi.otc2thm.mongodb.net/
MONGO_DB_NAME=wifi_points_db
MONGO_COLLECTION_NAME=wifi_points
```
### Ejecución del Pipeline de Datos
Para cargar los datos en la base de datos, se puede hacer de dos maneras, MANUAL Y AUTOMÁTICA, si se desea hacer MANUAL
debemos ejecutar el script initialize_db.py:
```sh
python initialize_db.py
```

De otra forma cuando corramos la imagen de docker, se realizará automáticamente la instalación de bibliotecas y la ejecución de nuestro pipeline.

### Uso de la API
La API proporciona varios endpoints para interactuar con los datos de puntos de acceso WiFi:
    GET /wifi_points/all: Obtiene todos los puntos de acceso WiFi.
    GET /wifi_points/paginated: Lista los puntos de acceso WiFi de forma paginada.
    GET /wifi_points/colonia: Obtiene puntos de acceso WiFi por colonia con paginación.
    GET /wifi_points/proximity_search: Búsqueda de puntos de acceso por proximidad.
    GET /wifi_points/<point_id>: Obtiene un punto de acceso específico por su ID.

### Para ejecutar la aplicación Flask manualmente (sin docker), utilizaremos el siguiente comando:
```sh
flask run
```

### Ejecución en Docker

Para ejecutar la aplicación en un contenedor de Docker, utilizaremos:

```sh
docker-compose up --build
```
### Despliegue en Kubernetes

Despliega la aplicación en un clúster de Kubernetes usando:

```sh
kubectl apply -f k8s-deployment.yml
```

### Ejecución de Pruebas Unitarias

Las pruebas unitarias se encuentran en el directorio tests. Se pueden ejecutar entrando al directorio test, utilizando el siguiente comando:
```sh
pytest test_wifi_service.py
```
Este proyecto cuenta con documentación en código y por medio de Swagger. por lo que al ejecutar, podemos probar los endpoints a través de:

```sh
localhost:5000/swagger
```
![image](https://github.com/FGArandaRodriguez/data_pipeline_wifi/assets/37637850/54fd9166-75a0-479f-b436-097013a67f75)



