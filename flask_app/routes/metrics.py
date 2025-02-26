"""
This module handles metrics for the application.
"""

import time  # 標準庫放前面

from flask import Blueprint, jsonify

metrics_bp = Blueprint("metrics", __name__)

# 模擬 Flask 監控數據，將計數器附加到 blueprint 上
metrics_bp.request_count = 0
start_time = time.time()


@metrics_bp.route("/metrics", methods=["GET"])
def app_metrics():
    """
    提供 Flask 應用的基礎指標，供 Prometheus 監控

    這個函數會更新請求計數器、計算運行時間，並以 JSON 格式返回指標資訊。
    """
    # 更新 blueprint 上的請求計數器，避免使用 global
    metrics_bp.request_count += 1
    uptime = round(time.time() - start_time, 2)

    return jsonify({
        "requests_served": metrics_bp.request_count,
        "uptime_seconds": uptime,
        "http_status": 200
    }), 200
