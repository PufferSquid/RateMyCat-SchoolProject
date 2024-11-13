from tests.conftest import app, client
from app.models import db, User
import requests
import pytest

API_KEY : str = "live_M03wyBxpvJs4NwwVqhUWBGgqijLWLXtdX8QpqWtYfVQ0U4cp30HyRwn5tMyZdtmF"


def test_add_user(app):
    data = {
        "id" : 0,
        "username" : "Mike",
        "password" : "12345"
        }

    with app.app_context():
        db.session.add(User(data["id"], data["username"], data["password"]))
        db.session.commit()

        query : User = db.session.query(User).filter_by(username="Mike").first()

    assert query is not None
    assert query.id >= 0
    assert query.username == "Mike"
    assert query.password == "12345"


def test_duplicate_username(app):
    data = {
    "id" : 0,
    "username" : "Mike",
    "password" : "12345"
    }

    with app.app_context():
        with pytest.raises(Exception):
            db.session.add(User(data["id"], data["username"], data["password"]))
            db.session.add(User(1, data['username'], "other password"))
            db.session.commit()


def test_duplicate_id(app):
    data = {
    "id" : 0,
    "username" : "Mike",
    "password" : "12345"
    }

    with app.app_context():
        with pytest.raises(Exception):
            db.session.add(User(data["id"], data["username"], data["password"]))
            db.session.add(User(data["id"], "Jack", "other password"))
            db.session.commit()



def test_cat_api_returns_data(app, API_KEY):
    _id = "asf2"
    url = f"https://api.thecatapi.com/v1/votes/{_id}"




def is_url_working(url):
    pass













