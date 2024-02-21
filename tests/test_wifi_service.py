import pytest
from app.services.wifi_service import get_all_wifi_points

def test_get_all_wifi_points():
    # Mock de la DB o datos de prueba
    wifi_points = get_all_wifi_points()
    assert wifi_points is not None  # Asegúrate de ajustar esta aserción a tu caso de prueba específico
