from app import app
from models import User, db
from flask import url_for


def test_index_search_by_id_endpoint(test_app):
    with test_app.test_client() as client:
        user = User(firstName="Alex", lastName="Kutuzov")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            url = url_for("index.search_by_id", user_id=user.id)

        headers = {"Accept": "application/json"}
        response = client.get(url, headers=headers)

        assert response.status_code == 200
        data = response.json["user_data"]
        assert data["id"] == user.id
        assert data["firstName"] == user.firstName
        assert data["lastName"] == user.lastName


def test_index_search_by_id_endpoint_not_found(test_app):
    with test_app.test_client() as client:
        user = User(firstName="Alex", lastName="Kutuzov")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            url = url_for("index.search_by_id", user_id=100)

        headers = {"Accept": "application/json"}
        response = client.get(url, headers=headers)

        assert response.status_code == 404


def test_filtered_users_by_name(test_app):
    with test_app.test_client() as client:
        user1 = User(firstName="John", lastName="Doe")
        user2 = User(firstName="Jane", lastName="Smith")
        user3 = User(firstName="John", lastName="Smith")
        db.session.add_all([user1, user2, user3])
        db.session.commit()

        with test_app.test_request_context():
            url = url_for("index.filtered_users_by_name")
        query_params = {"firstName": "John", "lastName": "Smith"}
        response = client.get(url, query_string=query_params)

        assert response.status_code == 200
        data = response.json["users_data"]
        assert len(data) == 1
        assert data[0]["firstName"] == "John"
        assert data[0]["lastName"] == "Smith"
