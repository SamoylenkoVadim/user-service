from flask import url_for
from models import User


def test_create_endpoint_get(test_app):
    with test_app.test_client() as client:
        headers = {"Accept": "application/json"}

        with test_app.test_request_context():
            url = url_for("create.create")
        response = client.get(url, headers=headers)

        assert response.status_code == 200
        assert 'User Service' in response.data.decode()


def test_create_endpoint_post(test_app):
    with test_app.test_client() as client:
        headers = {"Accept": "application/json"}

        with test_app.test_request_context():
            url = url_for("create.create")
        response = client.get(url, headers=headers)

        assert response.status_code == 200
        assert 'User Service' in response.data.decode()

        data = {
            "firstName": "John",
            "lastName": "Doe",
            "mail": "john.doe@example.com",
            "number": "1234567890"
        }
        response = client.post(url, json=data, headers=headers)

        assert response.status_code == 201
        assert response.json["status"] == "Created"

        user = User.query.filter_by(firstName="John", lastName="Doe").first()
        assert user is not None
        assert len(user.emails) == 1
        assert len(user.phoneNumbers) == 1
        assert user.emails[0].mail == "john.doe@example.com"
        assert user.phoneNumbers[0].number == "1234567890"
