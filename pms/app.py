import datetime
import json
import time

from flask import Flask, request, jsonify, Response, render_template
from pymongo.objectid import ObjectId

from pms.connection import get_connection
from pms.config import config

app = Flask(__name__)

connection = get_connection()
db = connection.pms
events = db.events
rollups = db.rollups

@app.route('/record', methods=['POST'])
def record():
    data = json.loads(request.data)
    _id = events.insert(data, safe=True)
    data['_id'] = _id
    generate_rollups(data)
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

@app.route('/')
def index():
    return render_template('graph.jinja2')

@app.route('/rollups/<year>/<month>/<day>/<name>')
def json_rollups(year, month, day, name):
    query = {
        'date': {
            'year': int(year),
            'month': int(month),
            'day': int(day),
        },
        'name': name,
    }
    cursor = rollups.find(query)

    data = []
    for rollup in cursor:
        data.append({
            #'properties': rollup['properties'],
            'data': rollup_data_to_array(rollup)['hourly'],
            'label': str(rollup['properties'])
        })
    return jsonify(response=data)

@app.route('/rollup/latest/<name>/<ly>/<hours>')
def last_data(name, ly, hours):
    now = datetime.datetime.utcnow()
    data = {}
    query = {'name': name}

    cursor = rollups.find(query).sort('_id', -1)

    for rollup in cursor:
        label = str(rollup['properties'])
        array = data.get(label, [])
        array.extend(rollup_data_to_array(rollup)['hourly'])
        data[label] = array

    flot_data = [{'label': k, 'data': sorted(data[k])} for k in data]

    return jsonify(response=flot_data)

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

def generate_rollups(event):
    """Try to create a rollup for the event"""
    t = event['_id'].generation_time
    for name, rollup_config in config['aggregation'].items():
        if type(rollup_config['properties']) != list:
            properties = [rollup_config['properties']]
        else:
            properties = rollup_config['properties']

        generate_rollup(event, name, properties)

def generate_rollup(event, name, properties):
    """Generate a single rollup for this event matching the properties"""
    event_time = event['_id'].generation_time
    doc = {
        'date':{
            'year': event_time.year,
            'month': event_time.month,
            'day': event_time.day,
        },
        'name': name,
        'properties': {},
    }
    for prop in properties:
        if not prop in event:
            print 'missing', prop
            return
        doc['properties'][prop] = event[prop]

    update = {
        '$inc' : {
            'data.total' : 1,
            'data.hour.{0.hour}'.format(event_time): 1,
            'data.minute.{0.hour}:{0.minute}'.format(event_time): 1,
        }
    }
    rollups.update(doc, update, upsert=True)

def rollup_data_to_array(rollup):
    hourly = []
    minutely = []
    data = {
        'hourly': hourly,
        'minutely': minutely,
    }
    date = datetime.datetime(
        rollup['date']['year'],
        rollup['date']['month'],
        rollup['date']['day'],
    ) - datetime.timedelta(hours=8)

    for h in range(24):
        t = datetime.timedelta(hours=h)
        h_str = str(h)
        dt = date + t
        hour_value = int(rollup['data']['hour'].get(h_str, 0))

        hourly.append([to_epoch(dt)*1000, hour_value])

        for m in range(60):
            t = datetime.timedelta(hours=h, minutes=m)
            m = '{0}:{1}'.format(h,m)
            dt = date + t
            print dt
            minute_value = int(rollup['data']['minute'].get(m, 0))

            minutely.append([to_epoch(dt)*1000, minute_value])

    return data

def to_epoch(dt):
    """Convert a datetime to second since epoch int"""

    return time.mktime(dt.timetuple())

if __name__ == "__main__":
    app.debug = True
    app.run()
