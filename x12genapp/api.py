from flask import Blueprint

api_blueprint = Blueprint('api_bp', __name__)


@api_blueprint.route('/x12', methods=['POST'])
def post_x12():
    return {'message': 'hello'}
