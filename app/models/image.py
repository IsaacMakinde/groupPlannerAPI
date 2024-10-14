from app.config.db import db_connection

class Image:
    @staticmethod
    def get_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM images')
                return cursor.fetchall()
        return None

    @staticmethod
    def images_by_event(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM images WHERE event_id = %s', (event_id))
                conn.commit()
                return cursor.fetchall()
    
    @staticmethod
    def delete_by_event(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM images WHERE event_id = %s', (event_id,))
                conn.commit()
                return "Images deleted"
        return None

    @staticmethod
    def get_by_id(image_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM images WHERE id = %s', (image_id,))
                return cursor.fetchone()
        return None
    @staticmethod
    def create(data):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO images (event_id, image_url, description) VALUES (%s, %s, %s)'''
                cursor.execute(sql, (data['event_id'], data['image_url'], "to be added"))
                conn.commit()

                created_image = {
                    "id" : cursor.lastrowid,
                    "event_id" : data['event_id'],
                    "image_url" : data['image_url'],
                    "description" : "to be added"
                }
                return created_image
        return None

    @staticmethod
    def update(data, image_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE images SET event_id = %s, image_url = %s, description = %s WHERE id = %s'''
                cursor.execute(sql, (data['event_id'], data['image_url'], data['description'], image_id))
                conn.commit()
                return True
        return False
    
    @staticmethod
    def delete_by_id(image_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM images WHERE id = %s', (image_id,))
                conn.commit()
                return "Image deleted"
        return None

    @staticmethod
    def delete_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM images')
                conn.commit()
                return "All images deleted"
        return None