from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    emails = db.relationship('Email', backref='user', lazy=True, cascade="all, delete-orphan")
    phoneNumbers = db.relationship('PhoneNumber', backref='user', lazy=True, cascade="all, delete-orphan")


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return str(self.mail)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return str(self.number)


with app.app_context():
    db.create_all()


@app.route("/")
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

    if request.headers.get("Accept") == "application/json":
        return jsonify(users_data=users_data)

    return render_template('index.html', users_data=users_data)


@app.route("/create", methods=['GET', 'POST'])
def create():
    is_api_request = request.headers.get("Accept") == "application/json" or request.is_json

    if request.method == "GET":
        if is_api_request:
            return jsonify(status="Method Not Allowed"), 405
        else:
            return render_template('create.html')

    if request.method == "POST":
        if is_api_request:
            data = request.json
            firstName = data.get("firstName", "").strip() or None
            lastName = data.get("lastName", "").strip() or None
            mail = data.get("mail", "").strip() or None
            number = data.get("number", "").strip() or None
        else:
            firstName = request.form.get("firstName", "").strip() or None
            lastName = request.form.get("lastName", "").strip() or None
            mail = request.form.get("mail", "").strip() or None
            number = request.form.get("number", "").strip() or None

        if firstName is None or lastName is None:
            if is_api_request:
                return jsonify(status="Bad request: firstName and lastName are required"), 400
            else:
                return 'Bad request: firstName and lastName are required', 400

        try:
            user = User(firstName=firstName, lastName=lastName)
            if mail:
                email = Email(mail=mail)
                user.emails.extend([email])

            if number:
                phone_number = PhoneNumber(number=number)
                user.phoneNumbers.extend([phone_number])

            db.session.add(user)
            db.session.commit()

            if is_api_request:
                return jsonify(status="Created"), 201
            else:
                return redirect("/")

        except Exception as e:
            if is_api_request:
                return jsonify(status=f'Internal Server Error: {e}'), 500
            else:
                return f'Internal Server Error: {e}', 500


@app.route("/delete/<user_id>", methods=["GET", "DELETE"])
def delete(user_id):
    is_api_request = request.headers.get("Accept") == "application/json" or request.is_json
    try:
        user = db.session.get(User, user_id)
        if user is None:
            if is_api_request:
                return jsonify(status='Not Found'), 404
            else:
                return 'Not Found', 404
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        if is_api_request:
            return jsonify(status=f'Internal Server Error: {e}'), 500
        else:
            return f'Internal Server Error: {e}', 500

    if is_api_request:
        return jsonify(status='Record deleted successfully'), 204
    else:
        return redirect("/")


@app.route("/edit/<user_id>", methods=["GET", "POST"])
def edit(user_id):
    is_api_request = request.headers.get("Accept") == "application/json" or request.is_json
    user = db.session.get(User, user_id)

    if user is None:
        if is_api_request:
            return jsonify(status='Not Found'), 404
        else:
            return 'Not Found', 404

    emails = db.session.query(Email).filter_by(user_id=user_id).all()
    phone_numbers = db.session.query(PhoneNumber).filter_by(user_id=user_id).all()

    if request.method == "GET":
        if is_api_request:
            return jsonify(status="Method Not Allowed"), 405
        else:
            return render_template('edit.html', user=user, emails=emails, phone_numbers=phone_numbers)


    if request.method == "POST":
        try:
            if is_api_request:
                data = request.json
                if "firstName" in data:
                    user.firstName = data.get("firstName").strip()
                if "lastName" in data:
                    user.lastName = data.get("lastName").strip()
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
                    user.firstName = request.form["firstName"].strip()
                    user.lastName = request.form["lastName"].strip()

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

            if is_api_request:
                return jsonify(status="Changes committed"), 200
            else:
                return redirect(request.url)

        except Exception as e:
            if is_api_request:
                return jsonify(status=f'Internal Server Error: {e}'), 500
            else:
                return f'Internal Server Error: {e}', 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)
