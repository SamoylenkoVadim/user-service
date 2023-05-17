from models import User, db
from flask import request, jsonify, redirect, Blueprint
from utils import is_api_request
delete_bp = Blueprint('delete', __name__)


@delete_bp.route("/delete/<user_id>", methods=["GET", "DELETE"])
def delete(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        if is_api_request(request):
            return jsonify(status='Not Found'), 404
        else:
            return 'Not Found', 404
    db.session.delete(user)
    db.session.commit()

    if is_api_request(request):
        return jsonify(status='Record deleted successfully'), 204
    else:
        return redirect("/")
