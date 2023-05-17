from models import User, Email, PhoneNumber, db
from flask import request, jsonify, render_template, redirect, Blueprint
from flask_validation import validate_with_jsonschema
from utils import is_api_request
edit_bp = Blueprint('edit', __name__)

validation_schema = {
    "type": "object",
    "properties": {
        "firstName": {"type": "string", "nullable": True},
        "lastName": {"type": "string", "nullable": True},
        "emails": {"type": "array", "items": {"type": "string", "nullable": True}},
        "phone_numbers": {"type": "array", "items": {"type": "string", "nullable": True}}
    },
    "required": []
}


@edit_bp.route("/edit/<user_id>", methods=["GET", "POST"])
@validate_with_jsonschema(validation_schema)
def edit(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        if is_api_request(request):
            return jsonify(status='Not Found'), 404
        else:
            return 'Not Found', 404

    emails = db.session.query(Email).filter_by(user_id=user_id).all()
    phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user_id).all()

    if request.method == "GET":
        return render_template('edit.html', user=user, emails=emails, phone_numbers=phone_numbers)

    if request.method == "POST":
        if is_api_request(request):
            data = request.json
            if "firstName" in data:
                user.firstName = data.get("firstName").strip() or user.firstName
            if "lastName" in data:
                user.lastName = data.get("lastName").strip() or user.lastName
            if "emails" in data:
                db.session.query(Email).filter_by(user_id=user_id).delete()
                for email in emails:
                    db.session.expunge(email)
                for email in data.get("emails"):
                    email = Email(mail=email.strip())
                    user.emails.extend([email])
            if "phone_numbers" in data:
                db.session.query(PhoneNumber).filter_by(user_id=user_id).delete()
                for phone_number in phone_numbers:
                    db.session.expunge(phone_number)
                for phone_number in data.get("phone_numbers"):
                    number = PhoneNumber(number=phone_number.strip())
                    user.phoneNumbers.extend([number])
        else:

            save_user_name_button = request.form.get("SaveUserName")
            save_user_emails_button = request.form.get("SaveUserEmails")
            save_user_phone_numbers_button = request.form.get("SaveUserPhoneNumbers")

            if save_user_name_button is not None:
                user.firstName = request.form["firstName"].strip() or user.firstName
                user.lastName = request.form["lastName"].strip() or user.lastName

            if save_user_emails_button is not None:
                db.session.query(Email).filter_by(user_id=user_id).delete()
                for email in emails:
                    db.session.expunge(email)

                for key, value in request.form.items():
                    if key.startswith('email_') or key.startswith('newEmail'):
                        if value.strip() != "":
                            email = Email(mail=value.strip())
                            user.emails.extend([email])

            if save_user_phone_numbers_button is not None:
                db.session.query(PhoneNumber).filter_by(user_id=user_id).delete()

                for phone_number in phone_numbers:
                    db.session.expunge(phone_number)

                for key, value in request.form.items():
                    if key.startswith('phoneNumber_') or key.startswith('newPhoneNumber'):
                        if value.strip() != "":
                            number = PhoneNumber(number=value.strip())
                            user.phoneNumbers.extend([number])
        db.session.commit()

        if is_api_request(request):
            return jsonify(status="Changes committed"), 200
        else:
            return redirect(request.url)
