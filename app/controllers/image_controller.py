from app.models.image import Image
from quart import Blueprint, request, jsonify
# from firebase_admin import storage
import asyncio
import uuid

images_bp = Blueprint('images', __name__)


# This route will be used to get all images and delete all images
@images_bp.route('/api/images', methods=['GET', 'DELETE'])
async def images():
    """
    ---
    get:
        description: Get a list of all images
        responses:
            200:
            description: A list of all images
    delete:
        description: Delete all images
        responses:
            200:
            description: All images deleted successfully
    """
    if request.method == 'GET':
        return jsonify(await Image.get_all()), 200
    elif request.method == 'DELETE':
        return jsonify({'message': await Image.delete_all()}), 200


# This route will be used to upload aa image to Firebase Storage and save the URL in the database
# @images_bp.route('/api/images/upload', methods=['POST'])
# async def upload_file():
#     """

#     ---
#     post:
#         description: Upload an image to Firebase Storage
#         requestBody:
#             content:
#                 multipart/form-data:
#                     schema:
#                         type: object
#                         properties:
#                             file:
#                                 type: string
#                                 format: binary
#                             event_id:
#                                 type: string
#         responses:
#             200:
#                 description: File uploaded successfully
#             400:
#                 description: No file provided
#             500:
#                 description: An error occurred
#     """

#     # Await to get the file and event_id from the request in Quart
#     file = (await request.files).get('file')
#     event_id = (await request.form).get('event_id')

#     if file:        
#         # Define the Firebase Storage bucket
#         bucket = storage.bucket('planner-426320.appspot.com')
#         print(bucket)
#         # Create a blob (file object in Firebase)
#         blob = bucket.blob(f'images/{uuid.uuid4()}_{file.filename}')
#         print("check", blob)
#         # Upload the file to Firebase Storage using an executor for non-blocking behavior
#         loop = asyncio.get_event_loop()
#         await loop.run_in_executor(None, blob.upload_from_file, file, file.content_type)
#         print("check2", blob)
        
#         # Make the file publicly accessible (optional)
#         blob.make_public()
#         firebase_url = blob.public_url

#         data = {
#             "event_id": event_id,
#             "image_url": firebase_url
#         }
#         print("data", data)
        
#         # Assuming Image.create is synchronous, you might also want to run it in an executor
#         try:
#             await loop.run_in_executor(None, Image.create, data)
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#         return jsonify({"message": "File uploaded successfully", "url": firebase_url}), 200
#     else:
#         return jsonify({"error": "No file provided"}), 400

# This route will be used to get all images by event_id and delete all images by event_id
@images_bp.route('/api/images/event/<string:event_id>', methods=['GET', 'DELETE'])
async def images_by_event(event_id):

    """
    ---
    get:
        description: Get a list of all images by event_id
        responses:
            200:
            description: A list of all images by event_id
    delete:
        description: Delete all images by event_id
        responses:
            200:
            description: All images by event_id deleted successfully
    """

    if request.method == 'GET':
        return jsonify(Image.images_by_event(event_id)), 200
    elif request.method == 'DELETE':
        return jsonify({'message': Image.delete_by_event(event_id)}), 200


# This route will be used to get all images by image_id, update by image_id and delete all images by image_id
@images_bp.route('/api/images/<string:image_id>', methods=['GET','PUT', 'DELETE'])
async def image(image_id):
    if request.method == 'GET':
        return jsonify(await Image.get_by_id(image_id)), 200 
    elif request.method == 'PUT':
        return jsonify(await Image.update(request.json, image_id)), 200
    elif request.method == 'DELETE':
        return jsonify({'message': await Image.delete_by_id(image_id)}), 200
