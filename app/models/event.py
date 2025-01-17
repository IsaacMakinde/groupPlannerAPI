from app.config.db import db_connection

ACCEPTED_FIELDS = ['title', 'host', 'clerk_id', 'date', 'venue', 'place_id', 'description', 'category_id', 'pricing']
class Event:
    @staticmethod
    def get_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM events')
                return cursor.fetchall()
        return None

    @staticmethod
    def get_by_id(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
                return cursor.fetchone()
        return None

    @staticmethod
    def create(data):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO events (title, host, clerk_id, date, venue, place_id, description, category_id, pricing) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql, (
                    data['title'], data['host'], data['clerk_id'], data['date'], data['venue'], 
                    data['place_id'], data['description'], data['category_id'], data['pricing']
                ))
                conn.commit()

                created_event = {
                    "id" : cursor.lastrowid,
                    "title" : data['title'],
                    "host" : data['host'],
                    "clerk_id" : data['clerk_id'],
                    "date" : data['date'],
                    "venue" : data['venue'],
                    "place_id" : data['place_id'],
                    "description" : data['description'],
                    "category_id" : data['category_id'],
                    "pricing" : data['pricing'],
                }

                return created_event
        return None

    @staticmethod
    def update(data, event_id):
        conn = db_connection()
        print(data)
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE events SET title = %s, host = %s,  date = %s, venue = %s, place_id = %s, description = %s, category_id = %s, pricing = %s WHERE id = %s'''
                cursor.execute(sql, (
                    data['title'], data['host'], data['date'], data['venue'], 
                    data['place_id'], data['description'], data['category_id'], data['pricing'], event_id
                ))
                conn.commit()
                updated_event = {
                    "id" : event_id,
                    "title" : data['title'],
                    "host" : data['host'],
                    "clerk_id" : data['clerk_id'],
                    "date" : data['date'],
                    "venue" : data['venue'],
                    "place_id" : data['place_id'],
                    "description" : data['description'],
                    "category_id" : data['category_id'],
                    "pricing" : data['pricing'],
                }

                return updated_event
        return None

    @staticmethod
    def delete_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM events')
                conn.commit()
                return True
        return False

    @staticmethod
    def delete_by_id(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM events WHERE id = %s', (event_id,))
                conn.commit()
                return True
        return False

    @staticmethod
    def get_guests(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM guests WHERE event_id = %s', (event_id,))
                return cursor.fetchall()
        return None

    @staticmethod
    def get_guest(event_id, guest_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM guests WHERE event_id = %s AND id = %s', (event_id, guest_id))
                return cursor.fetchone()
        return None

    @staticmethod
    def add_guest(data, event_id):
        conn = db_connection()
        print("attempting to add guest")
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO guests (event_id, clerk_id, guest_name, guest_email, guest_image_url, guest_status) VALUES (%s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql, (event_id, data["clerk_id"], data['guest_name'], data['guest_email'], data['guest_image_url'], data['guest_status']))
                conn.commit()
                return {
                    "event_id" : event_id,
                    "clerk_id" : data["clerk_id"],
                    "guest_name" : data['guest_name'],
                    "guest_email" : data['guest_email'],
                    "guest_image_url" : data['guest_image_url'],
                    "guest_status" : data['guest_status']
                }
        return None

    @staticmethod
    def delete_guests(event_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM guests WHERE event_id = %s', (event_id,))
                conn.commit()
                return {"message": "Guests deleted"}
        return False

    @staticmethod
    def get_guest(event_id, guest_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM guests WHERE event_id = %s AND id = %s', (event_id, guest_id))
                return cursor.fetchone()
        return None

    @staticmethod
    def delete_guest(event_id, guest_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM guests WHERE event_id = %s AND id = %s', (event_id, guest_id))
                conn.commit()
                return True
        return False
