"""
This module handles configuration for the application.
"""

from flask import Blueprint, current_app

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
        if isinstance(value, (int, float, str, bool, type(None))):
            safe_config[key] = value
        elif isinstance(value, (dict, list)):
            safe_config[key] = value
        else:
            safe_config[key] = repr(value)  # Fallback: use repr() for other types

    return safe_config
