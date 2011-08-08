from jsonrequester import JsonRequester
import random

requester = JsonRequester('http://localhost:5000')

for i in range(4):
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
    }
    print requester.post('/record', doc)

