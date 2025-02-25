from flask import Blueprint, jsonify, current_app
from datetime import timedelta

config_bp = Blueprint("config", __name__)


@config_bp.route("/config", methods=["GET"])
def get_config():

    safe_config = {}

    for key, value in current_app.config.items():
        if isinstance(value, timedelta):
            safe_config[key] = str(value)  # 轉換為字串
        elif isinstance(value, dict):
            safe_config[key] = value
        elif isinstance(value, list):
            safe_config[key] = value
        elif isinstance(value, tuple):
            safe_config[key] = list(value)  # 轉換為可序列化格式
        elif isinstance(value, set):
            safe_config[key] = list(value)  # 轉換為可序列化格式
        elif isinstance(value, bytes):
            safe_config[key] = value.decode("utf-8", errors="ignore")  # 轉換為字串
        elif isinstance(value, type):
            safe_config[key] = str(value)  # 類型名稱轉換
        elif isinstance(value, object) and hasattr(value, '__dict__'):
            safe_config[key] = str(value)  # 物件轉換為字串
        elif isinstance(value, (int, float, str, bool, type(None))):
            safe_config[key] = value
        else:
            safe_config[key] = repr(value)  # 其他型態轉換為字串表示

    return jsonify(safe_config), 200
