from flask import Blueprint, render_template

from models import Hymn, OrderOfService


worship_bp = Blueprint("worship", __name__, template_folder="../templates")


@worship_bp.route("/")
def worship_home():
    return render_template("worship/index.html")


@worship_bp.route("/confession")
def confession():
    return render_template("worship/confession.html")


@worship_bp.route("/affirmation")
def affirmation():
    return render_template("worship/affirmation.html")


@worship_bp.route("/order")
def order_of_service():
    order = OrderOfService.query.order_by(OrderOfService.created_at.desc()).first()
    items = order.items.split(",") if order else []
    return render_template("worship/order.html", order=order, items=items)


@worship_bp.route("/hymns")
def hymns():
    hymns_list = Hymn.query.order_by(Hymn.title.asc()).all()
    return render_template("worship/hymns.html", hymns=hymns_list)
