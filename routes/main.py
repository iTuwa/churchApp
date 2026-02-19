from flask import Blueprint, render_template
from datetime import date

from models import Devotional, Event, Announcement


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    today = date.today()
    devotional = Devotional.query.filter_by(for_date=today).first()
    next_event = (
        Event.query.filter(Event.event_date >= today)
        .order_by(Event.event_date.asc())
        .first()
    )
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
    return render_template(
        "home.html",
        devotional=devotional,
        next_event=next_event,
        announcements=announcements,
    )
