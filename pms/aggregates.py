import datetime

def get_hourly_data_from_aggregate(aggregate):
    """Returns a list of datetime, value tuples"""
    data = []
    dt = datetime.datetime(
        aggregate['date']['year'],
        aggregate['date']['month'],
        aggregate['date']['day'],
    )

    for hour in aggregate['data']['hour']:
        hour_delta = datetime.timedelta(hours=int(hour))
        value_dt = dt + hour_delta
        value = aggregate['data']['hour'][hour]
        data.append((value_dt, value))
    return data

def generate_empty_data_set(start, stop, interval):
    """Generates (datetime, 0) tuples betwee start, stop, with interval
    """
    current = start
    items = []
    while current <= stop:
        items.append((current, 0))
        current += interval
    return items

def merge_data_into_empty_data_set(data, emptyset):
    """Merges the data into the dataset base on tuple[0]"
    Takes something like:
        [(1, 1), (3, 1)]
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    And returns
        [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]

    """
    data = sorted(data)

    new_data = []
    item = data.pop(0)
    for empty_tuple in emptyset:
        if item is not None:
            if item[0] == empty_tuple[0]:
                new_data.append(item)
                if len(data) > 0:
                    item = data.pop(0)
                else:
                    item = None
            else:
                new_data.append(empty_tuple)
        else:
            new_data.append(empty_tuple)
    return new_data


