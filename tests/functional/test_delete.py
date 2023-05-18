from app import app
from models import User, Email, PhoneNumber, db
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

        emails = db.session.query(Email).filter_by(user_id=user.id).all()
        phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()

        assert response.status_code == 204
        assert db.session.get(User, user.id) is None
        assert emails == []
        assert phone_numbers == []


def test_delete_endpoint_contacts_check(test_app):
    with test_app.test_client() as client:
        user = User(firstName="John", lastName="Doe")
        email = Email(mail="firstName@gmail.com")
        phone_number = PhoneNumber(number="+491674653487")
        user.emails.extend([email])
        user.phoneNumbers.extend([phone_number])

        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            url = url_for("delete.delete", user_id=user.id)

        headers = {"Accept": "application/json"}
        response = client.delete(url, headers=headers)

        emails = db.session.query(Email).filter_by(user_id=user.id).all()
        phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()

        assert response.status_code == 204
        assert db.session.get(User, user.id) is None
        assert emails == []
        assert phone_numbers == []


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