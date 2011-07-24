import json

from flask import Flask, request, jsonify, Response
from pymongo.objectid import ObjectId

from pms.connection import get_connection

app = Flask(__name__)

connection = get_connection()
db = connection.pms
events = db.events

@app.route('/record', methods=['POST'])
def record():
    data = json.loads(request.data)
    print events.insert(data, safe=True)
    return jsonify({'status':200})

@app.route('/list', methods=['GET'])
def listen():
    l = get_events()
    return jsonify({'events': l})

@app.route('/search', methods=['GET'])
def search():
    query = flatten(request.args)
    l = get_events(query)
    return jsonify({'events': l})

@app.route('/next/<oid>', methods=['GET'])
def next(oid):
    for event in events.find({'_id': {'$gt': ObjectId(oid)}}).sort('_id', 1):
        wrap_event(event)
        return jsonify(event)
    return jsonify({})

def get_events(query=None):
    l = []
    for event in events.find(query).sort('_id', -1):
        wrap_event(event)
        l.append(event)
    return l

def wrap_event(event):
    event['time'] = str(event['_id'].generation_time)
    event['_id'] = str(event['_id'])

def flatten(data):
    new_data = {}
    for key in data:
        new_data[key] = data[key]
    return new_data


if __name__ == "__main__":
    app.debug = True
    app.run()
