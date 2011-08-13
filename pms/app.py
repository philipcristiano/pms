import datetime
import json
import time

from flask import Flask, request, jsonify, Response, render_template
from pymongo.objectid import ObjectId

import aggregates
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

@app.route('/query')
def query():
    start = int(request.args.get('pms_js_time')) /1000
    print start
    start = datetime.datetime.utcfromtimestamp(start)
    #start -= datetime.timedelta(hours=4)
    end = start + datetime.timedelta(hours=1)
    print start

    start_id = ObjectId.from_datetime(start)
    end_id = ObjectId.from_datetime(end)
    args = flatten(request.args)
    del args['pms_js_time']
    query = {
        '_id': {
            '$gte': ObjectId.from_datetime(start),
            '$lte': ObjectId.from_datetime(end),
        }
    }
    query.update(args)
    l = []
    for event in events.find(query).sort('_id'):
        wrap_event(event)
        l.append(event)
    return jsonify(events=l)

@app.route('/')
def index():
    return render_template('graph.jinja2', config=config)

@app.route('/rollup/latest/<name>/<ly>/<hours>')
def last_data(name, ly, hours):
    data = {}
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(hours=int(hours))
    timetuple = start.timetuple()[:4]
    start = datetime.datetime(*timetuple)
    interval = datetime.timedelta(hours=1)

    minute_offset = (-(time.altzone if time.daylight else time.timezone)) / 60

    query = {
        'name': name,
        'date.year': {'$gte': start.year},
        'date.month': {'$gte': start.month},
        'date.day': {'$gte': start.day},
    }

    cursor = rollups.find(query).sort('_id', -1)
    label_map = {}
    for rollup in cursor:
        label = str(rollup['properties'])
        array = data.get(label, [])
        array.extend(aggregates.get_hourly_data_from_aggregate(rollup))
        data[label] = array
        label_map[label] = rollup['properties']

    empty_set = aggregates.generate_empty_data_set(start, now, interval)

    flot_data = []
    for label, label_data in data.items():
        data_list = aggregates.merge_data_into_empty_data_set(
            label_data,
            empty_set
        )
        local_data_list = map_dataset_to_local_time(data_list, minute_offset)
        js_data_list = map_data_set_to_javascript_times(local_data_list)
        flot_data.append({
            'label': label,
            'data': js_data_list,
            'pms_properties': label_map[label],
        })

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
            minute_value = int(rollup['data']['minute'].get(m, 0))

            minutely.append([to_epoch(dt)*1000, minute_value])

    return data

def map_data_set_to_javascript_times(data):
    """Takes a list of tuples and coverts the first element to a js timestamp returning a new list.

    Input:
        [(datetime1, datum1), (datetime2, datum2)]

    """
    new_data = []
    for (timestamp, datum) in data:
        js_timestamp = to_epoch(timestamp) * 1000
        new_data.append((js_timestamp, datum))
    return new_data


def map_dataset_to_local_time(data, minute_offset):
    """Takes a list of tuples and returns a list of tuples with the first
    element adjusted from GMT to the current TZ.

    """
    new_data = []
    for (timestamp, datum) in data:
        local_timestamp = timestamp + datetime.timedelta(minutes=minute_offset)
        new_data.append((local_timestamp, datum))
    return new_data

def to_epoch(dt):
    """Convert a datetime to second since epoch int"""

    return time.mktime(dt.timetuple())

if __name__ == "__main__":
    app.debug = True
    app.run()
