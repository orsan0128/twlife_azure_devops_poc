import os
import psutil
import platform
from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def system_status():
    """回傳 Flask 應用運行的系統資訊"""
    return jsonify({
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture(),
        "cpu_count": psutil.cpu_count(),
        "memory": f"{round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)} GB",
        "disk_usage": f"{round(psutil.disk_usage('/').used / (1024 * 1024 * 1024), 2)} GB / {round(psutil.disk_usage('/').total / (1024 * 1024 * 1024), 2)} GB",
        "process_id": os.getpid()
    }), 200
