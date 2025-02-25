from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    """ 回傳首頁 """
    return render_template("index.html")
