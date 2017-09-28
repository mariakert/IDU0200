from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import os.path
import json

app = Flask(__name__)

if not(os.path.exists('databases/database.db')):
    conn = sql.connect('databases/database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE animals( id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, species TEXT NOT NULL )')
    conn.execute('CREATE UNIQUE INDEX animals_name_uindex ON animals (name)')
    print("Table animals created successfully")

    conn.execute('CREATE TABLE sightings( id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, location TEXT NOT NULL, '
                 'sight_date TEXT NOT NULL, time TEXT NOT NULL )')
    print("Table sightings created successfully")

    conn.close()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/addAnimal', methods=['POST'])
def addAnimal():
    try:
        data = request.json
        print(data)
        json_data = data['animal']
        animal_name = json_data['animalName']
        animal_species = json_data['species']

        con = sql.connect("databases/database.db")

        cur = con.cursor()
        cur.execute('INSERT INTO animals (name, species) VALUES (?, ?)', (animal_name, animal_species))
        con.commit()
        con.close()

        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/addSighting', methods=['POST'])
def addSighting():
    try:
        data = request.json
        json_data = data['sighting']
        name = json_data['name']
        location = json_data['location']
        sight_date = json_data['sight_date']
        time = json_data['time']

        con = sql.connect("databases/database.db")

        cur = con.cursor()
        cur.execute('INSERT INTO sightings (name, location, sight_date, time) VALUES (?, ?, ?, ?)',
                    (name, location, sight_date, time))
        con.commit()
        con.close()

        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        #print(data)
        json_data = data['search']
        query_type = json_data['type']
        query = json_data['query']
        #print("data: " + query_type + " " + query)

        con = sql.connect("databases/database.db")

        cur = con.cursor()

        if query_type == 'name':
            cur.execute('SELECT animals.*, sightings.* FROM animals '
                        'LEFT JOIN sightings ON animals.name = sightings.name WHERE animals.name=?', (query, ))
        elif query_type == 'species':
            cur.execute('SELECT animals.*, sightings.* FROM animals '
                        'LEFT JOIN sightings ON animals.name = sightings.name WHERE animals.species=?', (query, ))
        else:
            cur.execute('SELECT animals.*, sightings.* FROM animals '
                        'LEFT JOIN sightings ON animals.name = sightings.name WHERE sightings.location=?', (query,))
        rows = cur.fetchall()
        con.close()

        print(query_type)
        if query_type == 'species':
            return json.dumps(filterRows(rows))

        return json.dumps(rows)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/deleteSighting', methods=['POST'])
def deleteSighting():
    try:
        data = request.json
        print(data)
        animal_id = data['animal']
        sighting_id = data['sighting']

        con = sql.connect("databases/database.db")

        cur = con.cursor()

        cur.execute('DELETE FROM animals WHERE id=(?)', (animal_id,))
        if not(sighting_id is None):
            cur.execute('DELETE FROM sightings WHERE id=(?)', (sighting_id,))
        con.commit()
        con.close()

        return jsonify(status='OK', message='deleted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/updateSighting', methods=['POST'])
def updateSighting():
    try:
        data = request.json
        animal = data['animal']
        sighting = data['sighting']
        animal_id = animal['id']
        species = animal['species']
        sighting_id = sighting['id']
        location = sighting['location']
        sight_date = sighting['sight_date']
        time = sighting['time']

        con = sql.connect("databases/database.db")

        cur = con.cursor()
        cur.execute('UPDATE animals SET species=? WHERE id=?',
                    (species, animal_id))
        cur.execute('UPDATE sightings SET location=?, sight_date=?, time=? WHERE id=?',
                    (location, sight_date, time, sighting_id))
        con.commit()
        con.close()

        return jsonify(status='OK', message='edited successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


def filterRows(rows):
    rows = sorted(rows, key=lambda cur_row: cur_row[1])
    current_animal = None
    current_name = None
    ret_rows = []
    for i in range(0, len(rows)):
        print(json.dumps(rows[i]))
        row = rows[i]
        if current_animal is None:
            current_animal = row
            current_name = row[1]

        if i == len(rows) - 1:
            ret_rows.append(current_animal)
            ret_rows.append(row)
        elif not(current_name == row[1]):
            ret_rows.append(current_animal)
            current_animal = row
            current_name = row[1]
        elif current_name == row[1]:
            current_animal = getMoreRecentSighting(row, current_animal)
            current_name = current_animal[1]

    return ret_rows


def getMoreRecentSighting(row1, row2):
    if row1[6] is None and row2[6] is None:
        return row1
    elif row1[6] is None:
        return row2
    elif row2[6] is None:
        return row1

    date1 = "" + row1[6]
    date1 = date1.split(" ")
    time1 = "" + row1[7]
    time1 = time1.split(":")
    date2 = "" + row2[6]
    date2 = date2.split(" ")
    time2 = "" + row2[7]
    time2 = time2.split(":")

    if int(date1[2]) > int(date2[2]):
        return row1
    elif int(date2[2]) > int(date1[2]):
        return row2

    if convertMonth(date1[1]) > convertMonth(date2[1]):
        return row1
    elif convertMonth(date2[1]) > convertMonth(date1[1]):
        return row2

    if int(date1[0]) > int(date2[0]):
        return row1
    elif int(date2[0]) > int(date1[0]):
        return row2

    if int(time1[0]) > int(time2[0]):
        return row1
    elif int(time2[0]) > int(time1[0]):
        return row2

    if int(time1[1]) > int(time2[1]):
        return row1
    elif int(time2[1]) > int(time1[1]):
        return row2

    return row1


def convertMonth(month):
    if month == "Jan":
        return 1
    if month == "Feb":
        return 2
    if month == "Mar":
        return 3
    if month == "Apr":
        return 4
    if month == "May":
        return 5
    if month == "Jun":
        return 6
    if month == "Jul":
        return 7
    if month == "Aug":
        return 8
    if month == "Sep":
        return 9
    if month == "Oct":
        return 10
    if month == "Nov":
        return 11
    if month == "Dec":
        return 12


if __name__ == '__main__':
    app.run()
