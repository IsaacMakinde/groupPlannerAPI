from app.config.db import db_connection

class User:
    @staticmethod
    def get_all():
        conn = db_connection()
        if conn:
            print("Connected hit")
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM clerk_users')
                return cursor.fetchall()
        return None

    @staticmethod
    def create(data):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO clerk_users (id, username, email, role, image_url) VALUES (%s, %s, %s, %s, %s)'''
                cursor.execute(sql, (data['id'], data['username'], data['email'], data['role'], data['image_url']))
                conn.commit()

                created_user = {
                    "id" : data['id'], 
                    "username" : data['username'],
                    "email" : data['email'],
                    "role" : data['role'],
                    "image_url" : data['image_url']
                }

                return created_user
        return None

    def update(data, user_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE clerk_users SET username = %s, email = %s, role = %s, image_url = %s  WHERE id = %s'''
                print(data)
                cursor.execute(sql, (data['username'], data['email'], data['role'], data['image_url'], user_id))
                conn.commit()
                created_user = {
                    "id" : user_id, 
                    "username" : data['username'],
                    "email" : data['email'],
                    "role" : data['role'],
                    "image_url" : data['image_url']
                }
                return created_user
        return False
    
    @staticmethod
    def get_by_id(user_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM clerk_users WHERE id = %s', (user_id,))
                return cursor.fetchone()
        return None
    @staticmethod
    def get_by_cid(cid):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM clerk_users WHERE id = %s', (cid,))
                return cursor.fetchone()
        return None
    
    @staticmethod
    def delete_by_id(user_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM clerk_users WHERE id = %s', (user_id,))
                conn.commit()
                return "User deleted"
        return None

    @staticmethod
    def delete_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM clerk_users')
                conn.commit()
                return "All users deleted"
        return None
