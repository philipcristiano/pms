import sys
import time

from jsonrequester import JsonRequester

host = sys.argv[1]

requester = JsonRequester(host)

def main():
    events = requester.get('/list')
    if len(events) > 0:
        last_id = events['events'][0]['_id']
    else:
        last_id = 24 * '0'

    while True:
        event = requester.get('/next/{0}'.format(last_id))
        if event:
            print event
            last_id = event['_id']
            print
        else:
            time.sleep(.5)

if __name__ == '__main__':
    main()
