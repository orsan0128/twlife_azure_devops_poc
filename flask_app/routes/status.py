"""
This module provides system status for the application.
"""

import os
import platform
import psutil
from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def system_status():
    """Return system status information for the Flask application."""
    return jsonify({
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture(),
        "cpu_count": psutil.cpu_count(),
        "memory": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "disk_usage": (
            f"{round(psutil.disk_usage('/').used / (1024 ** 3), 2)} GB / "
            f"{round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB"
        ),
        "process_id": os.getpid()
    }), 200
