from flask import Blueprint, jsonify, current_app

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/routes", methods=["GET"])
def list_routes():
    """回傳目前所有的 API 路由"""
    routes = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint != "static":  # 過濾靜態文件路由
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "url": str(rule)
            })

    return jsonify({"available_routes": routes}), 200
