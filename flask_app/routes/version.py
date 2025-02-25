from flask import Blueprint, jsonify

version_bp = Blueprint("version", __name__)


@version_bp.route("/version", methods=["GET"])
def get_version():
    """回傳應用程式的版本資訊"""
    version_info = {
        "app_name": "Flask API Service",
        "version": "1.0.0",
        "description": "這是一個 Flask API 服務",
        "author": "Your Name"
    }
    return jsonify(version_info), 200
