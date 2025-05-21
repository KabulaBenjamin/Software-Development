from flask import Blueprint, render_template

members_bp = Blueprint("members", __name__)

@members_bp.route('/')
def members_home():
    return render_template("members/home.html", title="Members Home")