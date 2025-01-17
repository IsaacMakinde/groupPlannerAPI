from app.config.db import db_connection

class Category:
    @staticmethod
    def get_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM categories')
                return cursor.fetchall()
        return None
    
    @staticmethod
    def get_by_id(category_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
                return cursor.fetchone()
        return None
    
    @staticmethod
    def create(data):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO categories (name) VALUES (%s)'''
                cursor.execute(sql, (data['name'],))
                conn.commit()

                created_category = {
                    "id" : cursor.lastrowid,
                    "name" : data['name']
                }

                return created_category
        return None

    @staticmethod
    def update(data, category_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                sql = '''UPDATE categories SET name = %s WHERE id = %s'''
                cursor.execute(sql, (data['name'], category_id))
                conn.commit()
                created_category = {
                    "id" : category_id,
                    "name" : data['name']
                }
                return created_category
        return None

    @staticmethod
    def delete_by_id(category_id):
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
                conn.commit()
                return "Category deleted"
        return None

    @staticmethod
    def delete_all():
        conn = db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM categories')
                conn.commit()
                return "Categories deleted"
        return None
