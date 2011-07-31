from jsonrequester import JsonRequester

requester = JsonRequester('http://33.33.33.10')

doc = {
    'a': 'a',
    'b': 'b',
    'level': 'critical',
}

print requester.post('/record', doc)
