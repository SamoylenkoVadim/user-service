from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

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


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    users_data = db.session.query(User, Email, PhoneNumber).join(Email).join(PhoneNumber).all()

    users = []
    for user_data in users_data:
        user = user_data[0]
        email = user_data[1]
        phone_number = user_data[2]

        users.append({
            'user': user,
            'emails': [email],
            'phone_numbers': [phone_number]
        })

    return render_template('index.html', users=users)


@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        try:
            firstName = request.form["firstName"].strip()
            lastName = request.form["lastName"].strip()
            mail = request.form["mail"].strip()
            number = request.form["number"].strip()
        except Exception as e:
            return f'Bad request: {e}', 400

        try:
            user = User(firstName=firstName, lastName=lastName)
            email = Email(mail=mail)
            phone_number = PhoneNumber(number=number)

            user.emails.extend([email])
            user.phoneNumbers.extend([phone_number])

            db.session.add(user)
            db.session.commit()

            return redirect("/")
        except Exception as e:
            return f'Internal Server Error: {e}', 500
    else:
        return render_template('create.html')


@app.route("/delete/<user_id>", methods=["GET", "DELETE"])
def delete(user_id):
    try:
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
    except Exception as e:
        return f'Internal Server Error: {e}', 500
    return redirect("/")


@app.route("/edit/<user_id>", methods=["GET", "PUT", "POST"])
def edit(user_id):
    user = db.session.get(User, user_id)
    if request.method in ("POST", "PUT"):
        try:
            SaveUserName = request.form.get("SaveUserName")
            SaveUserEmails = request.form.get("SaveUserEmails")
            SaveUserPhoneNumbers = request.form.get("SaveUserPhoneNumbers")

            if SaveUserName is not None:
                user.firstName = request.form["firstName"].strip()
                user.lastName = request.form["lastName"].strip()

            if SaveUserEmails is not None:
                emails = []
                for key, value in request.form.items():
                    if key.startswith('email_') or key.startswith('newEmail'):
                        if value.strip() != "":
                            emails.append(value.strip())
                user.emails = ','.join(emails)

            if SaveUserPhoneNumbers is not None:
                phoneNumbers = []
                for key, value in request.form.items():
                    if key.startswith('phoneNumber_') or key.startswith('newPhoneNumber'):
                        if value.strip() != "":
                            phoneNumbers.append(value.strip())
                user.phoneNumbers = ','.join(phoneNumbers)

            db.session.commit()
            return render_template('edit.html', user=user)
        except:
            return 'Internal Server Error', 500
    else:
        return render_template('edit.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
