"""
This module handles configuration for the application.
"""

from datetime import timedelta
from flask import Blueprint, jsonify, current_app

config_bp = Blueprint("config", __name__)


@config_bp.route("/config", methods=["GET"])
def get_config():
    """
    Retrieve the application's configuration in a JSON-serializable format.

    This function iterates over the current app's configuration and converts
    non-serializable values (such as timedelta, tuple, set, bytes, type, or objects
    with a __dict__) into string or list representations suitable for JSON output.
    """
    safe_config = {}

    for key, value in current_app.config.items():
        if isinstance(value, timedelta):
            safe_config[key] = str(value)  # Convert timedelta to string
        elif isinstance(value, dict):
            safe_config[key] = value
        elif isinstance(value, list):
            safe_config[key] = value
        elif isinstance(value, tuple):
            safe_config[key] = list(value)  # Convert tuple to list for JSON serialization
        elif isinstance(value, set):
            safe_config[key] = list(value)  # Convert set to list for JSON serialization
        elif isinstance(value, bytes):
            safe_config[key] = value.decode("utf-8", errors="ignore")  # Convert bytes to string
        elif isinstance(value, type):
            safe_config[key] = str(value)  # Convert type to string
        elif hasattr(value, '__dict__'):
            safe_config[key] = str(value)  # Convert object to string representation
        elif isinstance(value, (int, float, str, bool, type(None))):
            safe_config[key] = value
        else:
            safe_config[key] = repr(value)  # Fallback: use repr() for other types

    return jsonify(safe_config), 200
