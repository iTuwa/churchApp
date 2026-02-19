import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

from models import db, Devotional, Event, Announcement, Testimony, Suggestion, Hymn, OrderOfService, AdminUser
from routes.main import main_bp
from routes.worship import worship_bp
from routes.devotional import devotional_bp
from routes.community import community_bp
from routes.events import events_bp
from routes.giving import giving_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(worship_bp, url_prefix="/worship")
    app.register_blueprint(devotional_bp, url_prefix="/devotional")
    app.register_blueprint(community_bp, url_prefix="/community")
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(giving_bp, url_prefix="/giving")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Flask 3 removed before_first_request; initialize the database eagerly
    # when the app is created instead of waiting for the first request.
    with app.app_context():
        db.create_all()
        seed_sample_data()

    return app


def seed_sample_data():
    if not AdminUser.query.first():
        admin = AdminUser(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    if not Devotional.query.first():
        devo = Devotional(
            title="Rest in God",
            content="Come to me, all you who are weary and burdened, and I will give you rest.",
            reading_reference="Matthew 11:28",
            for_date=date.today(),
        )
        db.session.add(devo)

    if not Event.query.first():
        event = Event(
            title="Sunday Worship Service",
            description="Join us for worship, word, and fellowship.",
            event_date=date.today(),
        )
        db.session.add(event)

    if not Announcement.query.first():
        ann = Announcement(
            title="Welcome to Our Church App",
            body="Stay connected with worship resources, devotionals, and community updates.",
        )
        db.session.add(ann)

    if not Hymn.query.first():
        hymn = Hymn(
            title="Amazing Grace",
            lyrics="Amazing grace! How sweet the sound that saved a wretch like me...",
        )
        db.session.add(hymn)

    if not OrderOfService.query.first():
        order = OrderOfService(
            name="Standard Sunday Service",
            items="Welcome,Opening Hymn,Prayer,Scripture Reading,Sermon,Offertory,Benediction",
        )
        db.session.add(order)

    db.session.commit()


app = create_app()


if __name__ == "__main__":
    # For local/dev runs; on Render you should use gunicorn "app:create_app()"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
