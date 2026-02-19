from flask import Blueprint, render_template
from datetime import date

from models import Devotional


devotional_bp = Blueprint("devotional", __name__)


@devotional_bp.route("/today")
def today_devotional():
    today = date.today()
    devo = Devotional.query.filter_by(for_date=today).first()
    return render_template("devotional/today.html", devotional=devo, today=today)


@devotional_bp.route("/all")
def all_devotionals():
    devotionals = Devotional.query.order_by(Devotional.for_date.desc()).all()
    return render_template("devotional/all.html", devotionals=devotionals)


@devotional_bp.route("/prayer-notes")
def prayer_notes():
    return render_template("devotional/prayer_notes.html")
