"""
This module contains the core Flask application setup,
including route definitions and configurations.
"""
import os
from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect  # 匯入 CSRFProtect
from flask_app.routes.home import home_bp
from flask_app.routes.version import version_bp
from flask_app.routes.health import health_bp
from flask_app.routes.routes import routes_bp
from flask_app.routes.status import status_bp
from flask_app.routes.metrics import metrics_bp  # 確保 metrics 被匯入
from flask_app.routes.config import config_bp

load_dotenv()

app = Flask(__name__)

app.config['TEST_STRING'] = 'test string'
app.config['TEST_INTEGER'] = 123
app.config['TEST_FLOAT'] = 3.14
app.config['TEST_BOOLEAN'] = True
app.config['TEST_LIST'] = [1, 2, 3]
app.config['TEST_DICT'] = {'key': 'value'}
app.config['TEST_TIMEDELTA'] = timedelta(days=1)
app.config['TEST_TUPLE'] = (1, 2, 3)
app.config['TEST_SET'] = {1, 2, 3}
app.config['TEST_BYTES'] = b'test bytes'

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("FLASK_SECRET_KEY 未設定！請在環境變數中設定安全的密鑰。")

app.config['SECRET_KEY'] = SECRET_KEY

# ✅ 啟用 CSRF 保護
csrf = CSRFProtect(app)

# 註冊 Blueprint
app.register_blueprint(home_bp)
app.register_blueprint(version_bp)
app.register_blueprint(health_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(status_bp)
app.register_blueprint(metrics_bp)  # 確保 Prometheus /metrics 可用
app.register_blueprint(config_bp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))  # 適應 Azure 預設環境變數
    app.run(host="0.0.0.0", port=port)
