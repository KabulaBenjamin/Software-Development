from flask import Blueprint, render_template

subscribers_bp = Blueprint("subscribers", __name__)

@subscribers_bp.route('/')
def subscribers_home():
    return render_template("subscribers/home.html", title="Subscribers Home")