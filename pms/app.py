import json

from flask import Flask, request, jsonify, Response

from pms.connection import get_connection

app = Flask(__name__)

connection = get_connection()
db = connection.pms
events = db.events

@app.route('/record', methods=['POST'])
def record():
    data = json.loads(request.data)
    print events.insert(data)
    return jsonify({'status':200})

@app.route('/list', methods=['GET'])
def listen():
    l = []
    for event in events.find().sort('_id', -1):
        event['time'] = str(event['_id'].generation_time)
        event['_id'] = str(event['_id'])
        l.append(event)
    return jsonify({'events': l})


if __name__ == "__main__":
    app.debug = True
    app.run()
