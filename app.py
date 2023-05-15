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
    phoneNumbers = db.Column(db.String(30), nullable=False)

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
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            emails = request.form["emails"]
            phoneNumbers = request.form["phoneNumbers"]
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

if __name__ == "__main__":
    app.run(debug=True)