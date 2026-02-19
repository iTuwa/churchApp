from datetime import date

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from models import db, Devotional, Event, Announcement, Testimony, Suggestion, AdminUser


admin_bp = Blueprint("admin", __name__)


def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("admin.login"))
        return view_func(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_id"] = user.id
            flash("Logged in successfully.")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid credentials.")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    session.pop("admin_id", None)
    flash("Logged out.")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    suggestions = Suggestion.query.order_by(Suggestion.created_at.desc()).limit(5).all()
    pending_testimonies = Testimony.query.filter_by(is_approved=False).order_by(Testimony.created_at.desc()).all()
    return render_template(
        "admin/dashboard.html",
        suggestions=suggestions,
        pending_testimonies=pending_testimonies,
    )


@admin_bp.route("/devotionals", methods=["GET", "POST"])
@login_required
def manage_devotionals():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        ref = request.form.get("reading_reference")
        for_date_str = request.form.get("for_date")
        for_date_val = date.fromisoformat(for_date_str) if for_date_str else date.today()
        if title and content:
            devo = Devotional(title=title, content=content, reading_reference=ref, for_date=for_date_val)
            db.session.add(devo)
            db.session.commit()
            flash("Devotional saved.")
        return redirect(url_for("admin.manage_devotionals"))

    devotionals = Devotional.query.order_by(Devotional.for_date.desc()).all()
    return render_template("admin/devotionals.html", devotionals=devotionals)


@admin_bp.route("/devotionals/<int:devotional_id>/delete", methods=["POST"])
@login_required
def delete_devotional(devotional_id: int):
    devo = Devotional.query.get_or_404(devotional_id)
    db.session.delete(devo)
    db.session.commit()
    flash("Devotional removed.")
    return redirect(url_for("admin.manage_devotionals"))


@admin_bp.route("/events", methods=["GET", "POST"])
@login_required
def manage_events():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date_str = request.form.get("event_date")
        event_date_val = date.fromisoformat(date_str) if date_str else date.today()
        if title and description:
            event = Event(title=title, description=description, event_date=event_date_val)
            db.session.add(event)
            db.session.commit()
            flash("Event saved.")
        return redirect(url_for("admin.manage_events"))

    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template("admin/events.html", events=events)


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id: int):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event removed.")
    return redirect(url_for("admin.manage_events"))


@admin_bp.route("/announcements", methods=["GET", "POST"])
@login_required
def manage_announcements():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        if title and body:
            ann = Announcement(title=title, body=body)
            db.session.add(ann)
            db.session.commit()
            flash("Announcement saved.")
        return redirect(url_for("admin.manage_announcements"))

    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("admin/announcements.html", announcements=announcements)


@admin_bp.route("/announcements/<int:announcement_id>/delete", methods=["POST"])
@login_required
def delete_announcement(announcement_id: int):
    ann = Announcement.query.get_or_404(announcement_id)
    db.session.delete(ann)
    db.session.commit()
    flash("Announcement removed.")
    return redirect(url_for("admin.manage_announcements"))


@admin_bp.route("/testimonies/<int:testimony_id>/approve", methods=["POST"])
@login_required
def approve_testimony(testimony_id: int):
    testimony = Testimony.query.get_or_404(testimony_id)
    testimony.is_approved = True
    db.session.commit()
    flash("Testimony approved.")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/suggestions")
@login_required
def view_suggestions():
    suggestions = Suggestion.query.order_by(Suggestion.created_at.desc()).all()
    return render_template("admin/suggestions.html", suggestions=suggestions)


@admin_bp.route("/suggestions/<int:suggestion_id>/delete", methods=["POST"])
@login_required
def delete_suggestion(suggestion_id: int):
    suggestion = Suggestion.query.get_or_404(suggestion_id)
    db.session.delete(suggestion)
    db.session.commit()
    flash("Suggestion removed.")
    return redirect(url_for("admin.view_suggestions"))
