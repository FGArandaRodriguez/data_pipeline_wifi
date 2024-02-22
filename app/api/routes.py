from flask import Blueprint, jsonify, request
import logging
from ..services.wifi_service import (
    get_all_wifi_points, 
    get_wifi_points, 
    get_wifi_point_by_id, 
    get_wifi_points_by_colonia, 
    get_wifi_points_near
)

# Configura el logging
logging.basicConfig(level=logging.INFO)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/wifi_points/all', methods=['GET'])
def get_wifi():
    """Endpoint para obtener todos los puntos de acceso WiFi."""
    try:
        wifi_points = get_all_wifi_points()
        return jsonify(wifi_points), 200
    except Exception as e:
        logging.error(f"Error al obtener todos los puntos WiFi: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
@api_blueprint.route('/wifi_points/paginated', methods=['GET'])
def list_wifi_points():
    """Endpoint para listar puntos de acceso WiFi de forma paginada."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        wifi_points = get_wifi_points(page, per_page)
        return jsonify(wifi_points), 200
    except Exception as e:
        logging.error(f"Error en la lista paginada de puntos WiFi: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@api_blueprint.route('/wifi_points/colonia', methods=['GET'])
def wifi_points_by_colonia():
    """Endpoint para obtener puntos de acceso WiFi por colonia con paginación."""
    try:
        colonia = request.args.get('colonia')
        if not colonia:
            return jsonify({'message': 'Parámetro colonia es requerido'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        wifi_points = get_wifi_points_by_colonia(colonia, page, per_page)
        return jsonify(wifi_points)
    except Exception as e:
        logging.error(f"Error al obtener puntos WiFi por colonia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@api_blueprint.route('/wifi_points/proximity_search', methods=['GET'])
def wifi_points_near():
    """Endpoint para búsqueda de puntos de acceso por proximidad."""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        if lat is None or lng is None:
            return jsonify({'message': 'Los parámetros Lat y Lng son requeridos'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        wifi_points = get_wifi_points_near(lat, lng, page, per_page)
        return jsonify(wifi_points)
    except Exception as e:
        logging.error(f"Error en la búsqueda por proximidad: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@api_blueprint.route('/wifi_points/<point_id>', methods=['GET'])
def wifi_point(point_id):
    """Endpoint para obtener un punto de acceso específico por su ID."""
    try:
        wifi_point = get_wifi_point_by_id(point_id)
        if wifi_point:
            return jsonify(wifi_point), 200
        return jsonify({'message': 'Punto WiFi no encontrado'}), 404
    except Exception as e:
        logging.error(f"Error al obtener punto WiFi por ID: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
