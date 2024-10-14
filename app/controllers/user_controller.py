from quart import Blueprint, request, jsonify
from app.models.user import User

# Create a blueprint for users routes
users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET', 'POST', 'DELETE'])
def users():
    if request.method == 'GET':
        return jsonify(User.get_all()), 200
    elif request.method == 'POST':
        return jsonify(User.create(request.json)), 201
    elif request.method == 'DELETE':
        return jsonify({'message': User.delete_all()}), 200

def user(user_id):
    if request.method == 'GET':
        return jsonify(User.get_by_id(user_id)), 200
    
    elif request.method == 'PUT':
        return jsonify(User.update(request.json, user_id)), 200
    elif request.method == 'DELETE':
        return jsonify({'message': User.delete_by_id(user_id)}), 200
