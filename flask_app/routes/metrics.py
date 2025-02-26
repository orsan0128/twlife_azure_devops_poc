"""
This module handles metrics for the application and integrates with Prometheus.
"""

import time  # 標準庫放前面
from flask import Blueprint, request
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

metrics_bp = Blueprint("metrics", __name__)

# Prometheus 指標
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)

ACTIVE_REQUESTS = Gauge(
    "active_http_requests",
    "Number of active HTTP requests",
)

APP_UPTIME = Gauge(
    "app_uptime_seconds",
    "Application uptime in seconds",
)

HTTP_ERROR_COUNT = Counter(
    "http_errors_total",
    "Total number of HTTP error responses",
    ["method", "endpoint", "status_code"],
)

REQUEST_SIZE = Histogram(
    "http_request_size_bytes",
    "Size of incoming HTTP requests",
    ["method", "endpoint"],
)

RESPONSE_SIZE = Histogram(
    "http_response_size_bytes",
    "Size of outgoing HTTP responses",
    ["method", "endpoint"],
)

# 記錄應用啟動時間
start_time = time.time()


@metrics_bp.before_app_request
def before_request():
    """請求進入時：計數並標記開始時間，記錄請求大小"""
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()
    request_size = int(request.headers.get("Content-Length", 0))  # 取得請求大小
    REQUEST_SIZE.labels(request.method, request.path).observe(request_size)


@metrics_bp.after_app_request
def after_request(response):
    """請求完成時：記錄處理時間、請求大小、回應大小，並減少活躍請求數"""
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.method, request.path).inc()
    ACTIVE_REQUESTS.dec()

    # 記錄回應大小
    response_size = int(response.headers.get("Content-Length", 0))
    RESPONSE_SIZE.labels(request.method, request.path).observe(response_size)

    # **記錄錯誤請求（只統計 4xx, 5xx）**
    if response.status_code >= 400:
        HTTP_ERROR_COUNT.labels(request.method, request.path, response.status_code).inc()

    return response


@metrics_bp.route("/metrics", methods=["GET"])
def prometheus_metrics():
    """
    提供 Flask 應用的 Prometheus 格式指標
    """
    APP_UPTIME.set(time.time() - start_time)  # 設定應用運行時間
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
