import os
from flask import Flask, request, send_from_directory
from models import db
from endpoints import index_bp, create_bp, delete_bp, edit_bp
from flask import jsonify
from flask_validation import Validator
from utils import is_api_request
from flask_swagger_ui import get_swaggerui_blueprint

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

SWAGGER_URL = "/docs"
API_URL = "/docs/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Service"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/docs/swagger.json")
def specs():
    return send_from_directory(os.getcwd(), "swagger.json")


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
    app.run(debug=True)
