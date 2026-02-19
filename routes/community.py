from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import db, Suggestion, Testimony


community_bp = Blueprint("community", __name__)


@community_bp.route("/suggestions", methods=["GET", "POST"])
def suggestions():
    if request.method == "POST":
        content = request.form.get("content")
        is_anonymous = bool(request.form.get("anonymous"))
        contact = request.form.get("contact") if not is_anonymous else None
        if content:
            suggestion = Suggestion(content=content, is_anonymous=is_anonymous, contact=contact)
            db.session.add(suggestion)
            db.session.commit()
            flash("Thank you for your suggestion.")
        return redirect(url_for("community.suggestions"))

    return render_template("community/suggestions.html")


@community_bp.route("/testimonies")
def testimonies():
    testimonies_list = Testimony.query.filter_by(is_approved=True).order_by(Testimony.created_at.desc()).all()
    return render_template("community/testimonies.html", testimonies=testimonies_list)


@community_bp.route("/testimonies/submit", methods=["GET", "POST"])
def submit_testimony():
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")
        if content:
            testimony = Testimony(name=name, content=content)
            db.session.add(testimony)
            db.session.commit()
            flash("Thank you. Your testimony has been submitted for review.")
            return redirect(url_for("community.testimonies"))
    return render_template("community/submit_testimony.html")
