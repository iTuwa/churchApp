from flask import Blueprint, render_template


giving_bp = Blueprint("giving", __name__)


@giving_bp.route("/")
def giving_home():
    # Bank details can be edited directly in this template or wired to the database later.
    return render_template("giving/giving.html")
