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
    title VARCHAR(150) UNIQUE NOT NULL,
    clerk_id VARCHAR(150) NOT NULL,
    host VARCHAR(150) NOT NULL,
    date DATETIME NOT NULL,
    venue VARCHAR(200) NOT NULL,
    place_id VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT(11),
    pricing DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (clerk_id) REFERENCES clerk_users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

'''

sql_query_users = '''
CREATE TABLE IF NOT EXISTS clerk_users (
    id VARCHAR(150) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(150) NOT NULL,
    role VARCHAR(100) NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
'''

sql_query__images = '''
CREATE TABLE IF NOT EXISTS images (
    id INT(11) NOT NULL AUTO_INCREMENT,
    event_id INT(11) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    clerk_id VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
'''

sql_query_categories = '''
CREATE TABLE IF NOT EXISTS categories (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
'''

sql_query_guests = ''' 
CREATE TABLE IF NOT EXISTS guests (
    id INT(11) NOT NULL AUTO_INCREMENT,
    clerk_id VARCHAR(150) NOT NULL,
    event_id INT(11) NOT NULL,
    guest_name VARCHAR(150),
    guest_email VARCHAR(150),
    guest_image_url VARCHAR(255),
    guest_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (clerk_id) REFERENCES clerk_users(id) ON DELETE CASCADE
);
'''

sql_insert_user = '''
INSERT INTO clerk_users (id, username, email, role) VALUES (%s, %s, %s, %s)
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
cursor.execute(sql_query_guests)
conn.close()
