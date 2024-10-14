from quart import Blueprint, request, jsonify
from app.models.event import Event

# Create a blueprint for events routes
events_bp = Blueprint('events', __name__)

# Event routes
@events_bp.route('/api/events', methods=['GET', 'POST', 'DELETE'])
def events():
    if request.method == 'GET':
        return jsonify(Event.get_all()), 200
    elif request.method == 'POST':
        return jsonify(Event.create(request.json)), 201
    elif request.method == 'DELETE':
        return jsonify({'message': Event.delete_all()}), 200

@events_bp.route('/api/events/<string:event_id>', methods=['GET','PUT', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        return jsonify(Event.get_by_id(event_id)), 200
    
    elif request.method == 'PUT':
        return jsonify(Event.update(request.json, event_id)), 200
    elif request.method == 'DELETE':
        return jsonify({'message': Event.delete_by_id(event_id)}), 200
