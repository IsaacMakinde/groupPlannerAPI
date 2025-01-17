from quart import Blueprint, request, jsonify
from app.models.user import User
import pymysql

# Create a blueprint for users routes
users_bp = Blueprint('users', __name__)


@users_bp.route('/api/users?cid=<string:cid>', methods=['GET', 'POST', 'DELETE'])
async def user_by_cid(cid):
    if request.method == 'GET':
        return jsonify(User.get_by_cid(cid)), 200
    elif request.method == 'POST':
        data = await request.json
        created_user = User.create(data)
        return jsonify(created_user), 201
    elif request.method == 'DELETE':
        return jsonify({'message': User.delete_by_cid(cid)}), 200
        
@users_bp.route('/api/users', methods=['GET', 'POST', 'DELETE'])
async def users():
    if request.method == 'GET':
        return jsonify(User.get_all()), 200
    elif request.method == 'POST':
        try:
            data = await request.json
            created_user = User.create(data)
            return jsonify(created_user), 201
        except Exception as e:
            print(str(e), "this is the error")
            
            if isinstance(e, pymysql.err.IntegrityError):
                return jsonify({'error': 'User already exists'}), 400
            else:
                return jsonify({'error': 'Something went wrong'}), 400
             

    elif request.method == 'DELETE':
        return jsonify({'message': User.delete_all()}), 200

@users_bp.route('/api/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
async def user(user_id):
    if request.method == 'GET':
        return jsonify(User.get_by_id(user_id)), 200
    elif request.method == 'PUT':
        data = await request.json  # Await request.json to get the parsed JSON data
        updated_user = User.update(data, user_id)
        return jsonify(updated_user), 200
    elif request.method == 'DELETE':
        return jsonify({'message': User.delete_by_id(user_id)}), 200


