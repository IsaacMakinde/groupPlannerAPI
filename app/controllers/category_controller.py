from quart import Blueprint, request, jsonify
from app.models.category import Category

# Create a blueprint for categories routes
categories_bp = Blueprint('categories', __name__)

# Category routes
@categories_bp.route('/api/categories', methods=['GET', 'POST', 'DELETE'])
async def categories():
    if request.method == 'GET':
        return jsonify(Category.get_all()), 200
    elif request.method == 'POST':
        data = await request.json
        return jsonify(Category.create(data)), 201
    elif request.method == 'DELETE':
        return jsonify({'message': Category.delete_all()}), 200

@categories_bp.route('/api/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
async def category(category_id):
    if request.method == 'GET':
        return jsonify(Category.get_by_id(category_id)), 200
    elif request.method == 'PUT':
        data = await request.json
        return jsonify(Category.update(data, category_id)), 200
    elif request.method == 'DELETE':
        return jsonify({'message': Category.delete_by_id(category_id)}), 200