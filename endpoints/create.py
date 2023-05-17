from models import User, Email, PhoneNumber, db
from flask import request, jsonify, render_template, redirect, Blueprint
from flask_validation import validate_common
from utils import is_api_request
create_bp = Blueprint('create', __name__)


@create_bp.route("/create", methods=['GET', 'POST'])
@validate_common({'firstName': str, 'lastName': str, 'mail': str, 'number': str})
def create():
    if request.method == "GET":
        return render_template('create.html')

    if request.method == "POST":
        if is_api_request(request):
            data = request.json
            firstName = data.get("firstName", "").strip().title() or None
            lastName = data.get("lastName", "").strip().title() or None
            mail = data.get("mail", "").strip() or None
            number = data.get("number", "").strip() or None
        else:
            firstName = request.form.get("firstName", "").strip().title() or None
            lastName = request.form.get("lastName", "").strip().title() or None
            mail = request.form.get("mail", "").strip() or None
            number = request.form.get("number", "").strip() or None

        if firstName is None or lastName is None:
            if is_api_request(request):
                return jsonify(status="Bad request: firstName and lastName are required"), 400
            else:
                return 'Bad request: firstName and lastName are required', 400

        user = User(firstName=firstName, lastName=lastName)
        if mail:
            email = Email(mail=mail)
            user.emails.extend([email])

        if number:
            phone_number = PhoneNumber(number=number)
            user.phoneNumbers.extend([phone_number])

        db.session.add(user)
        db.session.commit()

        if is_api_request(request):
            return jsonify(status="Created"), 201
        else:
            return redirect("/")
