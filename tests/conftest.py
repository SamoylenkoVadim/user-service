import pytest
from app import app
from models import db


@pytest.fixture
def test_app():
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()