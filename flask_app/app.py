"""
This module contains the core Flask application setup,
including route definitions and configurations.
"""
import os
from flask import Flask
from flask_app.routes.home import home_bp
from flask_app.routes.version import version_bp
from flask_app.routes.health import health_bp
from flask_app.routes.routes import routes_bp
from flask_app.routes.status import status_bp
from flask_app.routes.metrics import metrics_bp
from flask_app.routes.config import config_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(version_bp)
app.register_blueprint(health_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(status_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(config_bp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
