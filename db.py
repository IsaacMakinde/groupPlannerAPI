import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
sql_query = '''
CREATE TABLE IF NOT EXISTS events (
    id INT(11) NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL,
    host VARCHAR(255) NOT NULL,
    date VARCHAR(100) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(255),
    pricing DECIMAL(10, 2) NOT NULL,
    guests TEXT,
    PRIMARY KEY (id)
)
'''

clear_table = '''DELETE FROM events'''
clear_db = '''DROP TABLE events'''
cursor.execute(sql_query)
conn.close()
