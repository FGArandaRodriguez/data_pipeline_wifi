import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from app.services.wifi_service import (
    get_all_wifi_points,
    get_wifi_points,
    get_wifi_points_by_colonia,
    get_wifi_points_near,
    get_wifi_point_by_id,
)

"""
Clase de pruebas unitarias por cada servicio. Sirve para ver el correcto funcionamiento de cada servicio creado
"""
# Datos de prueba ficticios que simulan la respuesta de MongoDB.
fake_wifi_points = [
    {
        "_id": {
            "$oid": "65d6b10e83e1abcb106772ba"
        },
        "alcaldia": "Iztapalapa",
        "colonia": "1A AMPLIACION SANTIAGO ACAHUALTEPEC",
        "fecha_instalacion": {
            "$numberDouble": "NaN"
        },
        "id": "1A AMPLIACION SANTIAGO ACAHUALTEPEC-02",
        "latitud": 19.35125116,
        "location": {
            "coordinates": [
                -99.00999147,
                19.35125116
            ],
            "type": "Point"
        },
        "longitud": -99.00999147,
        "programa": "Colonias_Periféricas"
    },
    {
        "_id": {
            "$oid": "65d6b10f83e1abcb1067d585"
        },
        "alcaldia": "Iztapalapa",
        "colonia": "SANTIAGO ACAHUALTEPEC 1RA AMPLIACION",
        "fecha_instalacion": {
            "$numberDouble": "NaN"
        },
        "id": "15639",
        "latitud": 19.35102,
        "location": {
            "coordinates": [
                -99.0108,
                19.35102
            ],
            "type": "Point"
        },
        "longitud": -99.0108,
        "programa": "Postes_C5"
    },
    {
        "_id": {
            "$oid": "65d6b10e83e1abcb106772b9"
        },
        "alcaldia": "Iztapalapa",
        "colonia": "1A AMPLIACION SANTIAGO ACAHUALTEPEC",
        "fecha_instalacion": {
            "$numberDouble": "NaN"
        },
        "id": "1A AMPLIACION SANTIAGO ACAHUALTEPEC-01",
        "latitud": 19.35254,
        "location": {
            "coordinates": [
                -99.01039,
                19.35254
            ],
            "type": "Point"
        },
        "longitud": -99.01039,
        "programa": "Colonias_Periféricas"
    }
]

# Prueba unitaria para get_all_wifi_points
def test_get_all_wifi_points():
    with patch('app.services.wifi_service.mongo_client') as mock_client:
        mock_collection = mock_client.get_db.return_value.get_collection.return_value
        mock_collection.find.return_value = fake_wifi_points

        result = get_all_wifi_points()
        assert result == fake_wifi_points, "Error al obtener todos los puntos WiFi"

# Prueba unitaria para get_wifi_points (paginación)
def test_get_wifi_points():
    with patch('app.services.wifi_service.mongo_client') as mock_client:
        mock_collection = mock_client.get_db.return_value.get_collection.return_value
        mock_collection.find.return_value = fake_wifi_points[:1]  # Simular respuesta paginada

        result = get_wifi_points(page=1, per_page=1)
        assert result == fake_wifi_points[:1], "Error en la paginación de los puntos WiFi"

# Prueba unitaria para get_wifi_points_by_colonia
def test_get_wifi_points_by_colonia():
    with patch('app.services.wifi_service.mongo_client') as mock_client:
        mock_collection = mock_client.get_db.return_value.get_collection.return_value
        mock_collection.find.return_value = fake_wifi_points[:1]  # Simular respuesta por colonia

        result = get_wifi_points_by_colonia("colonia_test", page=1, per_page=1)
        assert result == fake_wifi_points[:1], "Error al obtener puntos WiFi por colonia"

# Prueba unitaria para get_wifi_points_near
def test_get_wifi_points_near():
    with patch('app.services.wifi_service.mongo_client') as mock_client:
        mock_collection = mock_client.get_db.return_value.get_collection.return_value
        mock_collection.find.return_value = fake_wifi_points  # Simular respuesta de búsqueda por proximidad

        result = get_wifi_points_near(lat=19.4326, lng=-99.1332, page=1, per_page=2)
        assert result == fake_wifi_points, "Error en la búsqueda por proximidad de los puntos WiFi"

# Prueba unitaria para get_wifi_point_by_id
def test_get_wifi_point_by_id():
    with patch('app.services.wifi_service.mongo_client') as mock_client:
        mock_collection = mock_client.get_db.return_value.get_collection.return_value
        mock_collection.find_one.return_value = fake_wifi_points[0]  # Simular respuesta por ID

        result = get_wifi_point_by_id(fake_wifi_points[0]['_id'])
        assert result == fake_wifi_points[0], "Error al obtener un punto WiFi por ID"

