import pytest
from app import models, create_app
from flask import Flask
from flask.testing import FlaskClient
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        models.db.create_all()
        yield app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


