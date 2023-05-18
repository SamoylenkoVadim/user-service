from flask import url_for
from models import User, db


def test_edit_endpoint(test_app):
    with test_app.test_client() as client:
        headers = {"Accept": "application/json"}

        user = User(firstName="John", lastName="Doe")
        db.session.add(user)
        db.session.commit()

        with test_app.test_request_context():
            url = url_for("edit.edit", user_id=user.id)
        response = client.get(url)

        assert response.status_code == 200
        assert "User Service" in response.data.decode()


def test_edit_endpoint_post(test_app):
    with test_app.test_client() as client:
        headers = {"Accept": "application/json"}

        user = User(firstName="John", lastName="Doe")
        db.session.add(user)
        db.session.commit()

        with test_app.test_request_context():
            url = url_for("edit.edit", user_id=user.id)
        client.post(url, json={"firstName": "Jane", "lastName": "Smith"}, headers=headers)

        updated_user = db.session.get(User, user.id)

        assert updated_user.firstName == "Jane"
        assert updated_user.lastName == "Smith"