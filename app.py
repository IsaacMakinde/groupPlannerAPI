import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()
ACCEPTEDFIELDS = ['title', 'host', 'date', 'venue', 'description', 'category', 'pricing', 'guests']


def db_connection():
    conn = None
    try :
        conn = pymysql.connect(
    host= os.getenv('MYSQL_HOST'),
    database= os.getenv('MYSQL_DATABASE'),
    user= os.getenv('MYSQL_USER'),
    password= os.getenv('MYSQL_PASSWORD'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
    except pymysql.Error as e:
        print(e)
    return conn
@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.json
        return jsonify({'you sent': data}), 201
    else:
        return jsonify({'message': 'Welcome to the API'})
    

@app.route('/api/events', methods=['GET', 'POST', 'DELETE'])
def getAllEvents():


    conn = db_connection()
    cursor = conn.cursor()

    # POST    
    if request.method == 'POST': 
        new_title = request.json['title']
        new_host = request.json['host']
        new_date = request.json['date']
        new_venue = request.json['venue']
        new_description = request.json['description']
        new_category = request.json['category']
        new_pricing = request.json['pricing']
        new_guests = request.json['guests']
        
        ## add data to a database

        if not all([new_title, new_host, new_date, new_venue, new_description, new_category, new_pricing, new_guests]):
            return jsonify({'message': 'Missing data',
                            "data" : request.json}), 400
        
        try :
            # convert date string to date object

            date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400


        try:
            print(request.json)
            sql = '''INSERT INTO events (title, host, date, venue, description, category, pricing, guests) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (new_title, new_host, new_date, new_venue, new_description, new_category, new_pricing, new_guests))
            conn.commit() 
            new_event = {
                'id': cursor.lastrowid,
                'title': new_title,
                'host': new_host,
                'date': new_date,
                'venue': new_venue,
                'description': new_description,
                'category': new_category,
                'pricing': new_pricing,
                'guests': new_guests
            }
            return jsonify(new_event), 201
        except pymysql.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                return jsonify({'message': 'Event already exists'}), 409
            else:
                return jsonify({'message': 'Something went wrong'}), 500
    # GET
        ## return a list of events
    elif request.method == 'GET':
        cursor.execute('SELECT * FROM events')
        events = [
            dict(id=int(row['id']), 
                  title=row['title'],
                  host=row['host'], 
                  date=row['date'], 
                  venue=row['venue'], 
                  description=row['description'], 
                  category=row['category'], 
                  pricing=float(row['pricing']), 
                  guests=row['guests']) for row in cursor.fetchall()
        ]
        if events is not None:
            return jsonify(events), 200
        else: 
            "Nothing Found", 404
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM events')
        conn.commit()
        return jsonify({'message': 'All events have been deleted'}), 200
    

@app.route('/api/events/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def singleEvent(id):

    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM events WHERE id=%s', (id,))
        event = cursor.fetchone()
        if event is not None:
            return jsonify({'id': int(event['id']),
                            'title': event['title'],
                            'host': event['host'],
                            'date': event['date'],
                            'venue': event['venue'],
                            'description': event['description'],
                            'category': event['category'], 
                            'pricing': float(event['pricing']), 
                            'guests': event['guests']}), 200
        else:
            return jsonify({'message': 'Event not found'}), 404
    
    elif request.method == 'PUT':
        sql = '''UPDATE events SET'''
        fields = request.json.keys()
        params = tuple(request.json.values())

        try :
            if len(fields) == 0:
                return jsonify({'message': 'No data to update'}), 400
            
            else :
                for field in fields:
                    if field not in ACCEPTEDFIELDS:
                        return jsonify({'message': f'{field} is not a valid field'}), 400
            
            for field in fields:
                if field == 'date':
                    try:
                        date_obj = datetime.strptime(request.json[field], '%Y-%m-%d')
                    except ValueError:
                        return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
                    
                if field == 'pricing':
                    try:
                        float(request.json[field])
                    except ValueError:
                        return jsonify({'message': 'Pricing must be a number'}), 400
                elif type(request.json[field]) != str:
                    return jsonify({'message': f'Invalid data type for {field}'}), 400
                
            params += (id,)
        
            for field in fields:
                sql += f" {field} =%s,"
            sql = sql[:-1] + " WHERE id = %s"    

            cursor.execute(sql, params)
            conn.commit()
            sql = '''SELECT * FROM events WHERE id = %s'''
            cursor.execute(sql, (id,))
            updated_event = cursor.fetchone()
            updated_event['pricing'] = float(updated_event['pricing'])
            return jsonify(updated_event), 200
        except pymysql.Error as e:
            print(e)
            return jsonify({'message': 'Something went wrong'}), 500

          
    
    elif request.method == 'DELETE':
        ## delete data from a database
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM events WHERE id=%s', (id,))
        conn.commit()
        return jsonify({'message': 'The event has been deleted'}), 200
if __name__ == '__main__':
    app.run(debug=True)
