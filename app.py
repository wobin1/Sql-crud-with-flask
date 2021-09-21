from flask import Flask, request
import psycopg2
import collections
import json

app = Flask(__name__)


def getconnection(database_name, user_name, user_password, db_host, db_port):
    conn = psycopg2.connect(
        database = database_name,
        user = user_name,
        password = user_password,
        host = db_host,
        port = db_port
    )

    return conn


@app.route('/')
def index():
    conn = getconnection('osm', 'beta', 'password', '127.0.0.1', '5432') 
    cursor = conn.cursor()
    cursor.execute("select * from person")
    rows = cursor.fetchall()

     
    data = []
    for row in rows:
        row_data = {"id": row[0], "name": row[1]}
        data.append(row_data)

    conn.close()
    return {"names":data}

 

@app.route("/osm_point")
def osm_point():
    conn = getconnection('osm', 'beta', 'password', '127.0.0.1', '5432') 
    cursor = conn.cursor()
    cursor.execute("select osm_id, name, place, ST_AsText(way) from planet_osm_point limit 10")
    rows = cursor.fetchall()

    data= []

    for row in rows:
        row_data = {"osm_id":row[0], "name":row[1], "place":row[2], "way":[3]}
        data.append(row_data)

    conn.close() 
    return {"points": data}


@app.route("/add_person", methods=["POST"])
def insert_person():
    conn = getconnection('osm', 'beta', 'password', '127.0.0.1', '5432') 
    cursor = conn.cursor()
    if request.method== "POST":
        data = json.loads(request.data,strict=False)
        people = data[0]['name']
        print(people)
        try:
            cursor.execute("INSERT INTO person (name) VALUES(%s)", (people,))
            conn.commit()
            conn.close()
        except:
            return "there was something wrong with updating your data"

    return "Success!!!"


@app.route("/person_detail/<id>", methods=["GET"])
def person_detail(id):
    
    conn = getconnection('osm', 'beta', 'password', '127.0.0.1', '5432') 
    cursor = conn.cursor()
    print(id)
    cursor.execute("select * from person where id=%s", id )
    rows = cursor.fetchall()

    data=[]

    for row in rows:
        row_data = {"id": row[0], "name": row[1]}
        data.append(row_data)
    return {"person": data}

@app.route("/update_person/<id>", methods=["PUT"])
def update_person(id):
    conn = getconnection('osm', 'beta', 'password', '127.0.0.1', '5432') 
    cursor = conn.cursor()
    if request.method=="PUT":
        data = json.loads(request.data, strict=False)
        person = data[0]['name']
        print(person)
        cursor.execute("UPDATE PERSON SET name = %s where id=%s", (person, id)  )
        conn.commit()
        conn.close()
    
    return "You have succesfully updated your record"






if __name__ == "__main__":
    app.run(debug=True)