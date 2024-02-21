from flask import Blueprint, jsonify, request
from ..services.wifi_service import (get_all_wifi_points, get_wifi_points, get_wifi_point_by_id, 
get_wifi_points_by_colonia, get_wifi_points_near)


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/all_wifi_points', methods=['GET'])
def get_wifi():
    """
    Endpoint para obtener todos los puntos de acceso WiFi.
    Retorna una lista de puntos de acceso WiFi en formato JSON.
    """
    try:
        wifi_points = get_all_wifi_points()
        return jsonify(wifi_points), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_blueprint.route('/all_wifi_points_paginate', methods=['GET'])
def list_wifi_points():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        wifi_points = get_wifi_points(page, per_page)
        return jsonify(wifi_points), 200
    except Exception as e: 
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/wifi/<point_id>', methods=['GET'])
def wifi_point(point_id):
    try:
        wifi_point = get_wifi_point_by_id(point_id)
        if wifi_point:
            return jsonify(wifi_point),200
        return jsonify({'message': 'WiFi point not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/wifi/colonia', methods=['GET'])
def wifi_points_by_colonia():
    colonia = request.args.get('colonia', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    if colonia:
        wifi_points = get_wifi_points_by_colonia(colonia, page, per_page)
        return jsonify(wifi_points)
    return jsonify({'message': 'Colonia is required'}), 400

@api_blueprint.route('/wifi/near', methods=['GET'])
def wifi_points_near():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    if lat is not None and lng is not None:
        wifi_points = get_wifi_points_near(lat, lng, page, per_page)
        return jsonify(wifi_points)
    return jsonify({'message': 'Lat and Lng are required'}), 400
