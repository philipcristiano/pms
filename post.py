from jsonrequester import JsonRequester

requester = JsonRequester('http://localhost:5000')

doc = {
    'a': 'a',
    'b': 'b',
    'level': 'critical',
}

print requester.post('/record', doc)
