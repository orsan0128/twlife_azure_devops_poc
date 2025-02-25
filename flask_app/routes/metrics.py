from flask import Blueprint, jsonify
import time

metrics_bp = Blueprint("metrics", __name__)

# 模擬 Flask 監控數據
request_count = 0
start_time = time.time()


@metrics_bp.route("/metrics", methods=["GET"])
def app_metrics():
    """提供 Flask 應用的基礎指標，供 Prometheus 監控"""
    global request_count
    request_count += 1
    uptime = round(time.time() - start_time, 2)

    return jsonify({
        "requests_served": request_count,
        "uptime_seconds": uptime,
        "http_status": 200
    }), 200
