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
    emails = db.Column(db.String(100), nullable=False)
    phoneNumbers = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        try:
            firstName = request.form["firstName"].strip()
            lastName = request.form["lastName"].strip()
            emails = request.form["emails"].strip()
            phoneNumbers = request.form["phoneNumbers"].strip()
        except:
            return '400 Bad request'

        try:
            user = User(firstName=firstName, lastName=lastName,
                        emails=emails, phoneNumbers=phoneNumbers)
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except:
            return '500 Internal Server Error'
    else:
        return render_template('create.html')


@app.route("/delete/<id>", methods=["GET", "DELETE"])
def delete(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
    except:
        return '500 Internal Server Error'
    return redirect("/")

@app.route("/edit/<id>", methods=["GET", "PUT", "POST"])
def edit(id):
    user = User.query.get(id)
    if request.method in ("POST", "PUT"):
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

    else:
        return render_template('edit.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)
