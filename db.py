import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    port=int(os.getenv('MYSQL_PORT')),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
sql_query = '''
CREATE TABLE IF NOT EXISTS events (
    id INT(11) NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL,
    clerk_id INT(11) NOT NULL,
    host VARCHAR(255) NOT NULL,
    date VARCHAR(100) NOT NULL,
    venue VARCHAR(400) NOT NULL,
    place_id VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(255),
    pricing DECIMAL(10, 2) NOT NULL,
    guests TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (clerk_id) REFERENCES clerk_users(id) ON DELETE CASCADE
)
'''

sql_query_users = '''
CREATE TABLE IF NOT EXISTS clerk_users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    auth_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
)
'''

sql_query_insert_image = '''
CREATE TABLE IF NOT EXISTS images (
    id INT(11) NOT NULL AUTO_INCREMENT,
    event_id INT(11) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    description TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
)
'''

sql_insert_user = '''
INSERT INTO clerk_users (auth_id, username, email, role) VALUES (%s, %s, %s, %s)
'''
sql_insert_event = '''
INSERT INTO events (title, clerk_id, host, date, venue, place_id, description, category, pricing, guests, clerk_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

sql_insert_images = '''
INSERT INTO images (event_id, image_url, description) VALUES (%s, %s, %s)
'''

sql_drop_table = '''DROP TABLE events'''
clear_table = '''DELETE FROM events'''
clear_db = '''DROP TABLE events'''
cursor.execute(sql_query_insert_image)
conn.close()
