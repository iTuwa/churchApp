from flask import Blueprint, render_template
from datetime import date

from models import Event


events_bp = Blueprint("events", __name__)


@events_bp.route("/")
@events_bp.route("/calendar")
def calendar():
    today = date.today()
    events = Event.query.filter(Event.event_date >= today).order_by(Event.event_date.asc()).all()
    return render_template("events/calendar.html", events=events)
