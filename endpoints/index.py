from flask import jsonify, request, redirect, render_template, Blueprint
from models import db, User, Email, PhoneNumber
from utils import is_api_request

index_bp = Blueprint('index', __name__)


def make_user_data(user, emails, phone_numbers):
    return {
        'id': user.id,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'emails': [str(email) for email in emails],
        'phone_numbers': [str(phone_number) for phone_number in phone_numbers]
    }


@index_bp.route("/")
def index():
    return redirect("/users")


@index_bp.route("/users")
def users():
    users = db.session.query(User).all()
    users_data = []
    for user in users:
        emails = db.session.query(Email).filter_by(user_id=user.id).all()
        phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()
        users_data.append(make_user_data(user, emails, phone_numbers))

    if is_api_request(request):
        return jsonify(users_data=users_data)

    return render_template('index.html', users_data=users_data)


@index_bp.route("/users/<user_id>", methods=["GET"])
def search_by_id(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify(status='Not Found'), 404

    emails = db.session.query(Email).filter_by(user_id=user.id).all()
    phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()

    user_data = make_user_data(user, emails, phone_numbers)
    return jsonify(user_data=user_data)


@index_bp.route("/users/filter")
def filtered_users_by_name():
    firstName = request.args.get('firstName', default="", type=str).title()
    lastName = request.args.get('lastName', default="", type=str).title()

    query = db.session.query(User)
    if firstName:
        query = query.filter(User.firstName == firstName)
    if lastName:
        query = query.filter(User.lastName == lastName)

    users = query.all()
    users_data = []
    for user in users:
        emails = db.session.query(Email).filter_by(user_id=user.id).all()
        phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()
        users_data.append(make_user_data(user, emails, phone_numbers))

    return jsonify(users_data=users_data)