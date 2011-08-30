from jsonrequester import JsonRequester
import random

requester = JsonRequester('http://localhost:5000')

for i in range(2):
    rand = random.random()
    if rand < .2:
        level = 'critical'
    elif rand < .5:
        level = 'error'
    else:
        level = 'warning'

    doc = {
        'a': 'a',
        'b': 'b',
        'level': level,
        'host': str(i),
        'nested': {
            'level1': {
                'level2': 'HA!',
            },
            'Something' : 'blah',
        }
    }
    print requester.post('/record', doc)

