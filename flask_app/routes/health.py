from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """健康檢查 API，回傳 200 OK"""
    return jsonify({
        "status": "ok",
        "message": "Service is healthy",
        "http_code": 200
    }), 200
