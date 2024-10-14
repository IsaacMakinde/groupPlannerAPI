from app.config.db import db_connection

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
                sql = '''INSERT INTO events (title, host, clerk_id, date, venue, place_id, description, category, pricing, guests) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(sql, (
                    data['title'], data['host'], data['clerk_id'], data['date'], data['venue'], 
                    data['place_id'], data['description'], data['category'], data['pricing'], data['guests']
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
                    "category" : data['category'],
                    "pricing" : data['pricing'],
                    "guests" : data['guests']
                }

                return created_event
        return None
    
    @staticmethod
    def update(data, event_id):
        conn = db_connection()
        print(data)
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE events SET title = %s, host = %s, clerk_id = %s, date = %s, venue = %s, place_id = %s, description = %s, category = %s, pricing = %s, guests = %s WHERE id = %s'''
                cursor.execute(sql, (
                    data['title'], data['host'], data['clerk_id'], data['date'], data['venue'], 
                    data['place_id'], data['description'], data['category'], data['pricing'], data['guests'], event_id
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
                    "category" : data['category'],
                    "pricing" : data['pricing'],
                    "guests" : data['guests']
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
