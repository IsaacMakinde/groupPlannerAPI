from app.config.db import db_connection

class User:
    @staticmethod
    def get_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM clerk_users')
                return cursor.fetchall()
        return None

    @staticmethod
    def create(data):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO clerk_users (auth_id, username, email, role) VALUES (%s, %s, %s, %s)'''
                cursor.execute(sql, (data['auth_id'], data['username'], data['email'], data['role']))
                conn.commit()

                created_user = {
                    "id" : cursor.lastrowid,
                    "auth_id" : data['auth_id'],
                    "username" : data['username'],
                    "email" : data['email'],
                    "role" : data['role']
                }

                return created_user
        return None

    def update(data, user_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE clerk_users SET auth_id = %s, username = %s, email = %s, role = %s WHERE id = %s'''
                cursor.execute(sql, (data['auth_id'], data['username'], data['email'], data['role'], user_id))
                conn.commit()
                return True
        return False
    
    @staticmethod
    def get_by_id(user_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM clerk_users WHERE id = %s', (user_id,))
                return cursor.fetchone()
        return None
    

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
