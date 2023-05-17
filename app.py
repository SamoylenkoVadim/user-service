from flask import Flask, request
from models import db
from endpoints.index import index_bp
from endpoints.create import create_bp
from endpoints.delete import delete_bp
from endpoints.edit import edit_bp
from flask import jsonify
from flask_validation import Validator
from utils import is_api_request

app = Flask(__name__)
Validator(app)
app.register_blueprint(index_bp)
app.register_blueprint(create_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(edit_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()


@app.errorhandler(400)
def handle_bad_request(e):
    if is_api_request(request):
        return jsonify(status=f'Error: {e}'), 400
    else:
        return f'Error: {e}', 400


@app.errorhandler(Exception)
def all_exception_handler(error):
    if is_api_request(request):
        return jsonify(status=f'Internal Server Error: {error}'), 500
    else:
        return f'Internal Server Error: {error}', 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
