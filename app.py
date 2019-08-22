from flask import Flask, request, json, jsonify
import sqlite3
import datetime

app = Flask(__name__)


def set_up_db():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE data(id INTEGER PRIMARY KEY, data TEXT, timestamp DATETIME)''')
    db.commit()
    cursor.close()


def insert_data(data):
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO data(data, timestamp) VALUES(?,?)''',
                   (data, datetime.datetime.now().isoformat()))
    db.commit()
    cursor.close()


def get_data():
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data;")
    rows = cursor.fetchall()
    cursor.close()

    results = []
    for row in rows:
        print(row[1])
        results.append(json.loads(row[1]))

    return results


@app.route('/idt', methods=["POST"])
def post_data():
    data = request.get_json()
    insert_data(json.dumps(data))
    return jsonify(data), 202


@app.route('/splunk', methods=["GET"])
def get_data_for_splunk():
    data = {
        "data": get_data()}
    return jsonify(data)


set_up_db()


if __name__ == '__main__':
    app.run()
