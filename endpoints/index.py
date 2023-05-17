from flask import jsonify, request, render_template, Blueprint
from models import db, User, Email, PhoneNumber
from utils import is_api_request

index_bp = Blueprint('index', __name__)


@index_bp.route("/")
def index():
    users = db.session.query(User).all()
    users_data = []
    for user in users:
        emails = db.session.query(Email).filter_by(user_id=user.id).all()
        phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user.id).all()
        users_data.append({
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'emails': [str(email) for email in emails],
            'phone_numbers': [str(phone_number) for phone_number in phone_numbers],
        })

    if is_api_request(request):
        return jsonify(users_data=users_data)

    return render_template('index.html', users_data=users_data)