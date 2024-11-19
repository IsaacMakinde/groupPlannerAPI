from quart import Blueprint, request, jsonify
from app.models.event import Event

# Create a blueprint for events routes
events_bp = Blueprint('events', __name__)

# Event routes
@events_bp.route('/api/events', methods=['GET', 'POST', 'DELETE'])
async def events():
    if request.method == 'GET':
        return jsonify( Event.get_all()), 200  # Await if `get_all` is async
    elif request.method == 'POST':
        data = await request.json  # Await `request.json`
        return jsonify(Event.create(data)), 201  # Remove `await` if `Event.create` is sync
    elif request.method == 'DELETE':
        return jsonify({'message': Event.delete_all()}), 200  # Await if async

@events_bp.route('/api/events/<string:event_id>', methods=['GET', 'PUT', 'DELETE'])
async def event(event_id):
    if request.method == 'GET':
        return jsonify(Event.get_by_id(event_id)), 200  # Await if async
    elif request.method == 'PUT':
        try:
            data = await request.json  # Await `request.json`
            return jsonify(Event.update(data, event_id)), 200  # Remove `await` if sync
        except Exception as e:
            print(str(e))
            return jsonify({'error': "Something went wrong"}), 400
            
    elif request.method == 'DELETE':
        return jsonify({'message': await Event.delete_by_id(event_id)}), 200  # Await if async
