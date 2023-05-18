from app import app
from models import User, db
from flask import url_for


def test_delete_endpoint(test_app):
    with test_app.test_client() as client:
        user = User(firstName="John", lastName="Doe")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            url = url_for("delete.delete", user_id=user.id)

        headers = {"Accept": "application/json"}
        response = client.delete(url, headers=headers)

        assert response.status_code == 204
        assert db.session.get(User, user.id) is None


def test_delete_endpoint_wrong_user(test_app):
    with test_app.test_client() as client:
        user = User(firstName="John", lastName="Doe")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            url = url_for("delete.delete", user_id=100)

        headers = {"Accept": "application/json"}
        response = client.delete(url, headers=headers)

        assert response.status_code == 404